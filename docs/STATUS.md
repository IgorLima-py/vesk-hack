# Status

> **Este documento ganha de todos os outros.** Se qualquer outro doc do projeto contradisser o
> que está aqui, este vale.

Escrito pelo `/tchau` no fim de cada sessão, lido pelo `/oi` na abertura da seguinte. Quem lê é
sempre alguém **sem nenhum contexto**. Este repositório é público: nada aqui leva segredo, dado
pessoal ou número de cliente.

`[V]` marca o que a sessão que escreveu conferiu por comando ou leitura; `[?]` marca o que veio de
antes ou foi só dito.

## Onde estamos

05/11/2026: o repositório nasceu com a licença PolyForm Noncommercial 1.0.0 [V], o README de esqueleto, as regras
(`CLAUDE.md`), o que o regulamento pede (`docs/hackathon.md`), o que a Meta e o TikTok dão por anúncio
(`docs/fontes.md`) e o roadmap de C1 a C13 (`docs/ROADMAP.md`), escritos na sessão que decidiu o hack. Nenhum código
ainda.

09/11/2026: nenhuma fatia tinha começado, e a fila em sequência já não cabia até 28/11. Por decisão do Igor, a fila
virou ondas (bloco 2 do `docs/ROADMAP.md`), e uma sessão orquestradora (a seção O) abre as fatias em paralelo, cada
uma no seu worktree. O ponteiro está no orquestrador. As regras de quem anda em paralelo estão no `CLAUDE.md`. Ainda
nenhum código. A mudança foi escrita de fora, numa sessão do outro repositório, e não teve `/tchau` daqui.

09/11/2026, C3 (sessão própria, worktree `c3-exemplos-contrato`): fechou. Ela entregou:
- **O gerador** (`exemplos/sintetico.py`): planos de cor lisa com cortes em segundos conhecidos, «VESK» em magenta
  `[255, 0, 255]` a partir de `marca_em`, e a frase «Vesk. The creative autopilot.» falada no mesmo segundo, com
  «Watch this.» antes, em 0,5 s, quando cabe. A voz vem do filtro `flite` do `ffmpeg`, sem rede; a fonte está em
  `exemplos/README.md`. O `gabarito.json` fica ao lado do mp4.
- **A suíte** (`exemplos/suite.py`): 24 vídeos, com 9 valores distintos de `marca_em`; 2 vídeos não têm marca.
- **O contrato** (`contrato/motor.md` e `contrato/motor.schema.json`, versão 1.0.0), com as escolhas do Igor nesta
  sessão:
  - JSON com linhas tipadas e pedido síncrono;
  - as 35 medidas do `xt` com nomes neutros onde havia nome de modelo;
  - o manifesto só com as versões das 13 camadas;
  - a fala por palavra e o texto na tela por quadro, como linhas do `eventos.csv`, que é o que a C6 precisa;
  - os erros 401, 413, 415 e 422.
- **Os exemplos:** `contrato/exemplos/resposta-ok.json`, coerente com o `E1`, e as 5 respostas ruins.
- **Os testes:** `tests/motor_falso.py`, com as 3 adulterações, e os testes `test_sintetico_gabarito`,
  `test_mesma_semente_mesmo_video`, `test_contrato_schema_valido`, `test_motor_falso_pega_cada_adulteracao` e
  `test_contrato.py`, que pula sem `MOTOR_URL`.
- **O `requirements-dev.txt`**, com `pytest`, `jsonschema`, `Pillow` e `requests`.

O que foi conferido:
- [?] O vermelho do começo: `python -m exemplos.sintetico --help` deu `No module named 'exemplos'`, sai 1 (rodado
  nesta sessão, antes do código).
- [V] Os 10 itens do `verificar:` passaram na Karen:
  - os cortes do `ffmpeg` são iguais ao gabarito no vídeo do `verificar:` e nos 24 da suíte;
  - o magenta dá 0 em 6,5 s e 12.101 pixels em 7,5 s, e 0 nos dois com `--sem-marca`;
  - o sha256 é igual com a mesma semente e muda com outra;
  - das respostas ruins, 5 de 5 são recusadas;
  - contra o motor falso, o honesto passa 5 de 5 sem `SKIPPED`, e cada adulteração sai 1;
  - sem `MOTOR_URL`, aparece `SKIPPED` com o motivo;
  - o `git grep` do `$PROIBIDO` sai 1.
- [V] A segunda opinião (Opus) teve dois achados:
  - **Consertado:** a seção «para quem implementa» e a frase do tempo medido na GPU local descreviam o projeto
    privado. As duas saíram do git e foram para a pasta de notas das sessões (`c3-para-o-motor-na-nuvem.md`).
  - **Descartado:** o achado de que o 422 e os limites de 120 s e de 1 a 60 caracteres passam do `sai:`. Eles
    estavam no plano que o Igor aprovou.

## Próximo passo imediato

O orquestrador (Opus, esforço high, na Karen) abre a onda 1: a C1 (os anúncios, com o Igor), a C2 (a vitrine e o
rascunho) e a C3 (os exemplos com gabarito e o contrato do motor), cada uma na sua sessão.

Com a C3 na `main`, abrem duas frentes:
- a C5, que só espera o vídeo `A` da C1;
- o motor na nuvem, no outro repositório, que segue o `contrato/` e o que a nota `c3-para-o-motor-na-nuvem.md`
  pede.

## Pendências

- [V] O repositório no GitHub (`IgorLima-py/vesk-hack`) foi criado público em 06/11/2026, e o C0 sobe nele no `/tchau`
  da sessão que o escreveu. A configuração (`.gitignore`, `.gitattributes`, `.claude/settings.json`) e o cabeçalho do
  `docs/DESVIOS.md` foram escritos do zero no evento, sem copiar modelo de antes dele (6.2 do regulamento).
- O motor na nuvem é feito no repositório do motor, de 07 a 10/11. A C6 confere se ele subiu com o `curl` da
  dependência.
- O domínio `hack.vesklab.com` (C2), a conta do Modal e a do Resend são do Igor.
- O arquivo das palavras proibidas (`vesk-hack-videos/proibido.txt`, fora do git) existe só na máquina que escreveu
  este repositório. Em outra, o `test -s` do bloco 3 barra a fatia até o arquivo ser copiado de lá.
- Bateria: o `python -m pytest -q` não acha teste (`no tests ran`, sai 5), porque ainda não há código. A trava do
  playbook barrou o primeiro push do C0, e ele subiu no segundo, com este registro. A C2 põe os testes no push.
- [V] A bateria da C3 na Karen, pela trava, ficou em 9 testes: 4 passaram, 0 falharam e 5 foram pulados (os 5 de
  contrato, porque não há `MOTOR_URL` na Karen). O teste de contrato nunca rodou contra o motor real, só contra o
  motor falso.
- Os testes do sintético **falham** sem um `ffmpeg` com o filtro `flite`. O build «full» do gyan.dev tem o filtro, e
  o «essentials» não tem. Antes de rodar a bateria em outra máquina, confira: `ffmpeg -filters | grep flite`.
- O CI da C2 precisa de três coisas para os testes da C3 passarem: `apt-get install ffmpeg`, `runs-on: ubuntu-24.04`
  fixo e `pip install -r requirements-dev.txt`. A nota para a C2 está na pasta de notas das sessões
  (`c3-para-c2-ci.md`).
- [?] O `flite` do Ubuntu 24.04 foi visto pela dependência `libflite1` do `libavfilter9`; não rodou num runner. O
  `ubuntu-latest` passa para o 26.04 em novembro de 2026, e esse não foi conferido.
- Os sha256 dos sintéticos valem na mesma máquina e na mesma versão do `ffmpeg`. Em outra, o vídeo muda, e o gabarito
  continua certo.
- [?] O esforço desta sessão não foi conferido (o hook não leu `CLAUDE_EFFORT`). O modelo foi Opus, como a tabela
  pede.

## O que foi tentado e não funcionou

- Nada ainda.
