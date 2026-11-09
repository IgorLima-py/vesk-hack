# Contrato do motor — versão 1.0.0

O motor é um serviço privado que lê cada segundo de um vídeo. Este repositório só conhece a API dele, descrita aqui.
A URL e as credenciais vêm do ambiente:
- `MOTOR_URL`: a base, sem barra no fim;
- `MOTOR_KEY` e `MOTOR_SECRET`: vão nos cabeçalhos `Modal-Key` e `Modal-Secret`.

O schema da resposta está em `motor.schema.json` (JSON Schema 2020-12). Os exemplos estão em `exemplos/`: uma
resposta boa, ilustrativa e coerente com o `E1`, e cinco ruins que o schema tem de recusar. O teste é
`tests/test_contrato.py`.

## Autenticação

Toda rota exige `Modal-Key` e `Modal-Secret`. Sem eles, ou com um valor errado, a resposta é `401`. Quem responde o
`401` é o proxy do Modal, antes do motor, então o contrato fixa só o código, não o corpo.

## `GET /saude`

`200`, com `{"ok": true, "versao_contrato": "1.0.0"}` (`$defs/saude` no schema). A C6 chama esta rota antes de
começar.

## `POST /analisar`

O pedido vai em `multipart/form-data`, com dois campos:

| Campo | Tipo | Regra |
|---|---|---|
| `video` | arquivo | mp4 ou mov (o arquivo tem `ftyp` nos bytes 4 a 8), até 100 MB e até 120 s |
| `marca` | texto | o nome da marca, de 1 a 60 caracteres; o motor procura esse nome na fala e no texto da tela |

O pedido é **síncrono**: a resposta vem no mesmo pedido. Se o Modal redirecionar (`303`), o cliente segue o
redirecionamento. O cliente espera até 300 s. Medido numa GPU local, o motor levou de 6 a 45 s para um vídeo de 15 a
30 s, e a nuvem pode levar mais no primeiro pedido.

### Resposta `200`

```json
{
  "versao_contrato": "1.0.0",
  "request_id": "<texto único por pedido>",
  "video_sha256": "<sha256 do vídeo recebido>",
  "duracao": 15.0,
  "arquivos": {
    "eventos.csv": [ {"evento": "...", "valor": "...", "t": 4, "pts": 4.0, "fim": null, "camada": "fala"} ],
    "xt.csv": [ {"t": 0, "cortes.principal": 0, "...": "..."} ],
    "manifesto.json": {"versao_motor": "<sha256>", "camadas": [ {"nome": "cortes", "versao": "<sha256>"} ]}
  }
}
```

Os cinco campos de cima e os três arquivos são obrigatórios. Nenhum campo fora do schema é aceito, em nenhum nível.
Cada arquivo vem em linhas tipadas: o segundo é número, nunca texto. O cliente grava o `.csv` a partir das linhas,
com as colunas na ordem deste documento.

#### `eventos.csv`

Uma linha por evento, com as colunas `evento, valor, t, pts, fim, camada`:

| Coluna | Tipo | O que é |
|---|---|---|
| `evento` | texto, de uma lista fechada | o tipo do evento, nas tabelas abaixo |
| `valor` | texto ou `null` | o que foi achado; o significado depende do evento |
| `t` | inteiro ou `null` | o segundo, `floor(pts)`; `null` quando o evento não aconteceu |
| `pts` | número ou `null` | o instante, em segundos; `null` quando o evento não aconteceu |
| `fim` | número ou `null` | o fim, em segundos, só para `palavra`; `null` nos outros eventos |
| `camada` | texto | a camada de onde o evento vem, ou várias unidas por `+` (`logotipo+fala+texto`) |

Os eventos-resumo vêm uma vez por vídeo:

| `evento` | `valor` |
|---|---|
| `primeira_marca` | onde a marca apareceu primeiro: `logotipo`, `fala`, `texto` ou `ausente` |
| `primeira_marca_falada` | o trecho falado que casou com a marca, `ausente` ou `sem_nome_da_marca` |
| `primeira_marca_escrita` | o trecho escrito na tela que casou com a marca, `ausente` ou `sem_nome_da_marca` |
| `primeiro_logotipo` | `null`; o `pts` diz quando o logotipo apareceu |
| `logotipo_parado_abertura` | `sim` ou `nao` (um logotipo parado no 1º segundo); pode faltar |
| `primeiro_cta` | `<tipo>: <frase>` da primeira chamada para ação, ou `ausente` |
| `primeiro_texto` | `null`; o `pts` diz quando apareceu o primeiro texto na tela |
| `texto_durante_fala` | a fração da fala com texto na tela, com 3 casas, ou `sem_fala` |
| `legenda` | a fração da fala com legenda, com 3 casas, ou `sem_fala` |
| `ultimo_quadro` | `null`; o `pts` é o do último quadro |

A fala e o texto na tela vêm segundo a segundo, e é por eles que o laudo diz o que estava na tela e na fala em cada
queda (C6):

| `evento` | Uma linha por | `valor` | `pts` e `fim` | `camada` |
|---|---|---|---|---|
| `palavra` | palavra falada | a palavra, como foi transcrita | o início e o fim dela | `fala` |
| `texto_na_tela` | quadro lido | os textos lidos no quadro, de cima para baixo e da esquerda para a direita, unidos por ` \| `; `""` quando o quadro não tem texto | o instante do quadro, com `fim` igual a `null` | `texto` |

As linhas de `palavra` vêm em ordem de `pts`, e as de `texto_na_tela` também.

#### `xt.csv`

Uma linha por segundo, de `t = 0` até `floor(pts do último quadro)`, sem pular segundo e em ordem. Cada linha tem `t`
(inteiro) e exatamente estas 35 medidas, na ordem:

```
cortes.principal, cortes.alternativo, complexidade.bordas, complexidade.png_bpp, movimento.diferenca,
cor.luminancia, cor.saturacao, cor.colorido, rostos.n_principal, rostos.n_alternativo, rostos.area_maior,
expressao.emocao, expressao.valencia, expressao.excitacao, logotipo.escore, logotipo.centro_x, logotipo.centro_y,
logotipo.area, embedding.novidade, energia.rms_db, energia.pico_db, fala.palavras, fala.prob, fala.idioma,
segmentos.fala, segmentos.musica, segmentos.ruido, segmentos.sem_energia, sons.fala, sons.canto, sons.musica,
texto.caixas, texto.caracteres, texto.area, texto.confianca
```

- `cortes.principal`, `cortes.alternativo` e `fala.palavras` são somas no segundo: o número de cortes por dois
  detectores e o número de palavras que começam no segundo. Nunca são `null`; `0` quer dizer que nada aconteceu.
- `expressao.emocao` e `fala.idioma` são texto: a emoção mais frequente no segundo e o código do idioma falado.
- As outras são números, agregados no segundo (média ou máximo). Valem `null` quando o segundo não tem dado.

#### `manifesto.json`

- `versao_motor` é o sha256 do código do motor.
- `camadas` tem **exatamente 13** itens `{nome, versao}`, um para cada camada: `cortes`, `complexidade`,
  `movimento`, `cor`, `rostos`, `expressao`, `logotipo`, `embedding`, `energia`, `fala`, `segmentos`, `sons` e
  `texto`.
- A `versao` de cada camada é o sha256 do que define o resultado dela. Se a versão mudar, o resultado pode mudar.

### Erros

| Código | Quando | Corpo |
|---|---|---|
| `401` | sem `Modal-Key`/`Modal-Secret`, ou com valor errado | o do proxy (não fixado) |
| `413` | vídeo acima de 100 MB | `{"erro": "video_grande_demais", "mensagem": "..."}` |
| `415` | o arquivo não é mp4 nem mov | `{"erro": "tipo_nao_suportado", "mensagem": "..."}` |
| `422` | falta `video` ou `marca`, a marca é vazia ou passa de 60 caracteres, ou o vídeo passa de 120 s | `{"erro": "pedido_invalido", "mensagem": "..."}` |

Os corpos seguem `$defs/erro` no schema.

## O que o schema não alcança

O teste de contrato confere estas regras à parte:
- o `t` do `xt.csv` começa em 0 e sobe de 1 em 1;
- as linhas de `palavra` vêm em ordem de `pts`;
- o `video_sha256` é o do arquivo enviado.

O `request_id` muda a cada pedido. O teste de contrato não confere isso, porque precisaria chamar o motor duas
vezes a cada bateria; quem confere é a C6, ao chamar o motor de novo.

## Para quem implementa o motor na nuvem

- Renomear as quatro medidas que levam nome de modelo para `cortes.principal`, `cortes.alternativo`,
  `rostos.n_principal` e `rostos.n_alternativo`. O nome do modelo não sai na resposta.
- Tirar do `xt.csv` as colunas que identificam a rodada e o vídeo. O `request_id` faz esse papel.
- Juntar ao `eventos.csv` uma linha `palavra` por palavra transcrita e uma linha `texto_na_tela` por quadro lido.
- Calcular a `versao` de cada camada e a `versao_motor`. Não mandar limiares, máquina, tempos ou caminhos.
- Apagar o vídeo depois de responder.

## Versão

A versão segue o semver. Campo novo e opcional sobe a versão menor. Campo que sai ou muda de tipo sobe a maior. O
schema fixa `versao_contrato` com `const`, então uma resposta de outra versão falha o teste até o contrato daqui ser
atualizado.
