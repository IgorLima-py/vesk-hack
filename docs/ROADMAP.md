# Roadmap

Quem escreve é o `/360`; quem lê é o `/tchau` (para resolver o perfil da próxima fatia) e o Igor. Este roadmap nasceu
em 05/11/2026, na sessão que decidiu o hack, já numerado do C1 (bloco 5).

---

## 1. Tabela de perfis

| Perfil | Modelo | Esforço | Quando |
|---|---|---|---|
| `leve`    | haiku  | low    | ler, resumir, exportar |
| `ajuste`  | sonnet | low    | corrigir texto, renomear, uma conta só |
| `padrao`  | sonnet | medium | fatia mecânica, tela, worker, chamada de rede |
| `dificil` | opus   | high   | schema, serviço de fundo, quebrar arquivo |
| `replan`  | opus   | xhigh  | replanejar, pesquisar frente nova, decidir escopo |
| `criativo` | opus  | xhigh  | o vídeo, o pitch e a página que vende |

**Regra de correção:** consertar o que uma fatia entregou errado usa **o modelo daquela fatia e
um nível de esforço acima**. Quem errou não foi o modelo, foi o orçamento de pensar.

---

## 2. A fila

Estado: ✅ feito · 🚧 em obras · ⬜ não começou · 🔴 travado

O prazo é 30/11/2026 às 23h59, e o alvo de submissão é 28/11. O anúncio vem primeiro porque é o que mais demora: a
curva só junta dado com o anúncio rodando, e o teste A/B leva dias para dar resultado.

**Em ondas, desde 09/11 (decisão do Igor):** em 09/11 nenhuma fatia tinha começado, e a fila em sequência já estava
atrasada. Desde então, as fatias andam em paralelo, tocadas pelo orquestrador (a seção «O», no bloco 3). **A regra é
esta:** uma fatia abre assim que a dependência dela passa por comando e nenhuma fatia aberta mexe nos mesmos arquivos.
As ondas abaixo são o calendário que essa regra dá; não são portões.

| Onda | Quando | Fatias juntas | Por que juntas |
|---|---|---|---|
| 1 | 09–12/11 | C1v, C1, C2, C3 | nenhuma depende de outra, salvo a C1, que espera os vídeos da C1v (desde 11/11); os arquivos não se cruzam (`anuncios/`; `docs/anuncios.md`; `site/` e `.github/`; `exemplos/`, `contrato/` e `tests/`) |
| 2 | 11–14/11 | C4, C5; no repositório do motor, a nuvem | a C4 espera o export da C1; a C5 precisa do `E1` da C3 e do vídeo `A` da C1v; a nuvem do motor precisa da C3 e do `A` |
| 3 | 14–16/11 | C6 | espera o motor no ar |
| 4 | 16–19/11 | C7, C8 | as duas só dependem da C6 (e a C8 da C4 e da C5) |
| 5 | 19–22/11 | C9, C11 | o Igor junta as pessoas da C11 desde 15/11 |
| 6 | 22–25/11 | C10, C12 | a C9 e a C12 mexem as duas no Worker e no backend, e por isso ficam em ondas diferentes |
| 7 | 25–28/11 | C13 | submissão até 30/11 às 23h59 |

**Ordem de corte:** se faltar tempo, cai a C10, depois a C11. A C12 e a C13 não caem.

**Quem anda em paralelo** roda em worktree próprio, não mexe no `docs/PROXIMO.md`, commita nomeando os caminhos e
junta na `main` no próprio `/tchau` (`CLAUDE.md`). O ponteiro fica no orquestrador.

| # | Chat | Perfil | Forma | Estado | Máquina | Depende de | Paralelo com | O que muda no dia seguinte |
|---|---|---|---|---|---|---|---|---|
| — | O — O orquestrador das ondas | `dificil` | sessao | 🚧 | Karen | — | todas | As fatias abrem sozinhas assim que a dependência passa, cada uma no seu worktree, e o Igor sabe a cada momento o que roda e o que espera a mão dele |
| 1v | C1v — Os anúncios montados por código | `criativo` | sessao | 🚧 | Karen | — | C2, C3 | Os dois anúncios da Vesk existem em mp4, com rosto e voz de gente e o resto composto por código, e cada um traz o gabarito do segundo da marca, dos cortes e da fala |
| 1 | C1 — Os anúncios no ar | `padrao` | sessao | ⬜ | qualquer | C1v | C2, C3 | Dois anúncios da Vesk rodam na Meta com o teto do Igor, a curva real começa a juntar, e o segundo da marca de cada um está marcado à mão |
| 2 | C2 — A vitrine e o rascunho | `padrao` | sessao | ⬜ | qualquer | — | C1, C3 | O repositório é público com README e licença, a página está no ar nos dois idiomas, os testes rodam a cada push, e o rascunho foi enviado |
| 3 | C3 — Os exemplos com gabarito e o contrato do motor | `dificil` | sessao | ✅ | qualquer | — (os testes rodam local; o push os roda depois que a C2 juntar) | C1, C2 | Qualquer sessão gera um vídeo com a marca, os cortes e a fala em segundos conhecidos, e o motor tem um contrato escrito que um teste confere |
| 4 | C4 — O relatório do Gerenciador | `dificil` | sessao | ⬜ | qualquer | C1 (o export real) | C5 | O export do Gerenciador de Anúncios vira a curva do laudo, só com os pontos que a Meta deu, sem login e sem OAuth |
| 5 | C5 — A variante e o 1º teste A/B | `dificil` | sessao | ⬜ | qualquer | C3; o vídeo `A` da C1v (o passo do teste A/B na Meta espera a C1) | C4 | Um anúncio vira uma variante de uma mudança só, provada pixel a pixel, o tamanho de amostra sai da fórmula, e o 1º teste A/B está rodando |
| 6 | C6 — O laudo que cruza | `dificil` | sessao | ⬜ | qualquer | C3, C4; o motor no ar | — | Um vídeo e uma curva viram o laudo que diz o que estava na tela e na fala em cada queda, sem interpolar |
| 7 | C7 — A precisão medida | `dificil` | sessao | ⬜ | qualquer | C6 | C8 | O README diz quanto o motor acerta por camada, com n e intervalo, medido contra o gabarito |
| 8 | C8 — A página com envio e o e-mail | `dificil` | sessao | ⬜ | qualquer | C4, C5, C6 | C7 | Qualquer pessoa sobe o vídeo e o export do anúncio dela e recebe o laudo, a variante e o plano do teste na tela, e no e-mail se quiser, sem mão |
| 9 | C9 — O piloto automático na conta da Vesk | `dificil` | sessao | ⬜ | qualquer | C8; a campanha da C1 com curva | C11 | Anúncio novo da Vesk vira laudo sozinho, com a curva por segundo puxada da Insights API, na caixa do Igor |
| 10 | C10 — O teste montado sozinho | `dificil` | sessao | ⬜ | qualquer | C5, C9 | C12 | A variante sobe como teste A/B pausado na conta da Vesk, o Igor aperta publicar, e o resultado do teste volta como laudo |
| 11 | C11 — Usuários reais | `dificil` | sessao | ⬜ | qualquer | C8 | C9 | Pessoas de fora usaram o add-on com os anúncios delas, e o projeto tem laudos reais e depoimentos autorizados |
| 12 | C12 — A demo aguenta o júri | `dificil` | sessao | ⬜ | qualquer | C8; a C9 juntada (as duas mexem no Worker) | C10 | A demo recusa o que não deve processar, aguenta carga sem erro 5xx, tem teto de gasto e um vigia de 30/11 a 02/12 |
| 13 | C13 — O vídeo e a submissão | `criativo` | sessao | ⬜ | qualquer | C12 | — | O projeto está submetido, com o vídeo de até 3 min, o README final e a demo funcionando inteira |

---

## 3. Uma seção por fatia

Valem para todas as fatias:
- `HACK=C:/Users/Usuario/Desktop/Side-Projects/vesk-hack` é este repositório, e `VIDEOS=C:/Users/Usuario/Desktop/Side-Projects/vesk-hack-videos`
  é a pasta fora do git com os vídeos, os exports e as autorizações;
- `SITE=https://hack.vesklab.com`;
- `E1` é o vídeo sintético que `python -m exemplos.sintetico --marca-em 4 --semente 1 --saida <mp4>` gera (C3), com
  o `gabarito.json` ao lado;
- `A` e `B` são os dois anúncios da Vesk (C1), em `$VIDEOS/a.mp4` e `$VIDEOS/b.mp4`, com o segundo da marca marcado à
  mão em `docs/anuncios.md`;
- o motor é chamado em `$MOTOR_URL`, com os cabeçalhos `Modal-Key` e `Modal-Secret` vindos de `$MOTOR_KEY` e
  `$MOTOR_SECRET`, só pelo ambiente;
- `PROIBIDO=$VIDEOS/proibido.txt` é o arquivo, fora do git, com a palavra proibida e o que nunca pode vazar para cá,
  uma expressão por linha. Ele não entra no git porque a lista, escrita aqui, já seria o vazamento. Letra acentuada vai
  em alternância (`(ã|Ã|a)`), nunca em colchete: o `git grep` do Windows lê o colchete byte a byte e deixa a palavra
  passar (medido em 05/11/2026, com a palavra plantada num repositório de teste). Em toda fatia,
  `test -s $PROIBIDO` sai 0, e `git -C $HACK grep -niE -f $PROIBIDO $(git -C $HACK rev-list --all)` não imprime nada e
  sai `1` (sai `128` quando o arquivo falta, e isso não conta como passar);
- dependência de fora deste repositório se confere por comando, antes do `falha antes:`. Se ela falhar, a fatia não
  começa.

### O — O orquestrador das ondas

`dificil` · opus · high · forma: sessao · máquina: Karen · plan mode: não · contexto: limpo antes

**persona:** chefe de obra que abre cada frente assim que o terreno deixa, nunca faz o trabalho de uma frente por ela, e diz ao dono, numa tabela, o que roda e o que espera a mão dele.
**por que existe:** em 09/11 nenhuma fatia tinha começado, e a fila em sequência não cabia até 28/11. O maestro do
playbook não serve aqui: ele recusa repositório público, ainda tem furos abertos e toca uma fatia por vez.
**entra:** a fila e a regra das ondas (bloco 2); as seções deste bloco; o `CLAUDE.md`; o `git log origin/main`.
**a cada volta** (na abertura, quando uma sessão filha para, e quando o Igor pergunta):
1. `git fetch -q` e a fila de `origin/main`: o que está ✅, o que roda (as sessões ligadas a ele) e o que espera.
2. Para cada fatia ⬜ cuja dependência passa (a fatia de que ela depende está ✅ em `origin/main`, e a linha
   `dependência:` da seção, se houver, passa por comando) e que não mexe nos arquivos de uma fatia aberta, ele abre
   uma sessão nova: contexto limpo, worktree próprio, o modelo e o esforço da tabela de perfis, plan mode quando a
   seção pede, o nome `c<N>` e o título da fila. O pedido é o prompt de abertura da seção, mais as regras de quem anda
   em paralelo do `CLAUDE.md`, mais a frase «o ponteiro aponta o orquestrador; o seu perfil é o da sua seção, e o
   aviso do hook sobre isso é esperado». No Linear, a tarefa espelho vai para In Progress.
3. Responde ao Igor com uma tabela: a fatia, o estado (rodando, esperando o Igor, juntada na `main`), o que espera a
   mão dele (plano a aprovar, vídeo a gravar, conta a criar, segredo a pôr) e o que abre em seguida.

**o que ele nunca faz:** o trabalho de uma fatia; aprovar plano, responder pergunta ou decidir no lugar do Igor; juntar
o ramo de uma filha na `main` (quem junta é o `/tchau` dela); mexer na fila. A pergunta que uma filha faz a ele vai ao
Igor com as palavras dela.
**limites:**
- a C13 pede esforço `xhigh`, acima do dele: ele a abre em `high` e pede ao Igor que suba o esforço dela no app;
- depois de vários avisos seguidos de filhas sem o Igor falar no meio, o app segura os avisos até o Igor falar, e a
  tabela diz isso;
- passando de 200k de contexto, ele fecha com `/tchau`, o ponteiro continua nele, e o Igor abre outro orquestrador;
- o motor na nuvem é do repositório do motor: o orquestrador só confere, pela `dependência:` da C6, se ele subiu.

**sai:** a cada volta, a tabela; no fim, todas as fatias ✅ ou cortadas pela ordem de corte.
**verificar:**
- `git log origin/main --since=2026-11-09 --format=%s | grep -oE "^C[0-9]+" | sort -u | wc -l` imprime pelo menos `2` (duas fatias juntaram na `main` desde as ondas);
- `git log origin/main --since=2026-11-09 --format=%s -- docs/PROXIMO.md | grep -vcE "^O:"` imprime `0` (só o orquestrador mexe no ponteiro).
**falha antes:** `git log origin/main --since=2026-11-09 --format=%s | grep -cE "^C[0-9]+:"` imprime `0` hoje.
**prompt de abertura:**

> Você é o orquestrador das ondas do vesk-hack. Leia a seção O, a fila e a regra das ondas (bloco 2) e o `CLAUDE.md`. A cada volta: `git fetch`, veja o que está ✅ em `origin/main` e o que roda nas sessões ligadas a você, abra cada fatia cuja dependência passa e que não cruza arquivo com uma aberta, e me dê a tabela do que roda e do que espera a minha mão. Você nunca faz o trabalho de uma fatia, nunca aprova plano nem decide por mim, e nunca junta ramo na `main`. Comece pela onda 1: C1, C2 e C3.

### C1v — Os anúncios montados por código

`criativo` · opus · xhigh · forma: sessao · máquina: Karen · plan mode: sim · contexto: limpo antes

**persona:** diretor de criação que monta por código dois anúncios de verdade, sem rosto nem voz de pessoa real: motion no visual do site, voz sintética de licença comercial, e cada coisa num segundo que o gabarito conhece.
**por que existe:** em 11/11, a pesquisa dos jeitos de fazer vídeo (a skill global `video`, em
`~/.claude/skills/video/SKILL.md`, fora deste git, com a fonte de cada linha) recomendou o híbrido montado por código.
Gravado à mão, o vídeo não dá o segundo exato nem a prova da variante. A IA generativa não refaz o mesmo vídeo, e os
modelos saem do ar: a API do Sora 2 em 24/09/2026 e o Veo 3.1 Preview em 22/10/2026.
**entra:**
- a skill `video`, `docs/hackathon.md` (a 6.4 permite IA, e a 6.2 trata de código) e o `CLAUDE.md`;
- o gerador da C3 (`exemplos/sintetico.py`), que dá o formato do gabarito;
- a marca da Vesk: o wordmark no visual do site (`site/public/style.css`);
- o roteiro em inglês, para o público dos EUA, a partir da fala em `$VIDEOS/voz/fala.txt`;
- sem rosto nem voz de pessoa real. A voz vem do Kokoro-82M `af_heart` (Apache-2.0), gerado local, e o arquivo vira
  bruto com sha256;
- o plano aprovado pelo Igor em 11/11, gravado no `docs/STATUS.md`, com o roteiro, a parte comum em Python e a prova
  dos motores. As decisões estão no bloco 5.
**sai:**
- `anuncios/`, escrito do zero no evento (6.2):
  - o projeto do motor que a prova dos motores escolher, com um componente só. Remotion, HyperFrames, Revideo e
    FrameFields desenham a mesma `linha_do_tempo.json` e são medidos pelos mesmos comandos, e o Igor escolhe. A tabela da prova
    vai para a skill global `video`. O Remotion é grátis para empresa de até 3 pessoas
    (https://github.com/remotion-dev/remotion/blob/main/LICENSE.md);
  - a voz, o som (com o logo sonoro gerado no `ffmpeg`, na cartela da marca) e o gabarito saem do Python, a partir
    da mesma linha do tempo;
  - os parâmetros de cada anúncio em `anuncios/a.json` e `anuncios/b.json`;
  - a legenda queimada, feita do bruto pelo faster-whisper e pelo filtro `subtitles` do `ffmpeg`;
- `anuncios/roteiro.md`, com:
  - o roteiro dos dois, segundo a segundo;
  - o comando que renderiza um anúncio;
  - o sha256 de cada bruto;
  - a linha `- A e B diferem em: <chaves>`;
  - como o navegador do render cumpre a regra do `--mute-audio`;
- `$VIDEOS/a.mp4` e `$VIDEOS/b.mp4`, em 1080x1920 (9:16), de 15 a 30 s, com áudio e legenda queimada; a marca entra
  em segundos diferentes nos dois, para o laudo ter o que comparar;
- ao lado de cada mp4, `$VIDEOS/a.gabarito.json` e `$VIDEOS/b.gabarito.json`, nas chaves do gabarito da C3 (`duracao`,
  `fps`, `largura`, `altura`, `marca_em`, `cortes`, `fala`, `texto`, `video_sha256`);
- os brutos em `$VIDEOS/brutos/`, fora do git.
**verificar:**
- `ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0` imprime `1080,1920` em `$VIDEOS/a.mp4` e em `$VIDEOS/b.mp4`, a duração dos dois fica entre `15` e `30`, e o `ffprobe` dos streams mostra `audio` nos dois;
- o comando de `anuncios/roteiro.md`, rodado duas vezes para o `A` na Karen, dá dois mp4 com o mesmo `ffmpeg -v error -i <mp4> -map 0 -f framemd5 -` (vídeo e áudio, quadro a quadro);
- um `python -c` lê os dois gabaritos: o `marca_em` é maior que 0, menor que a `duracao` e diferente entre A e B, e o `video_sha256` de cada um é o sha256 do mp4 ao lado;
- um `python -c` compara `anuncios/a.json` e `anuncios/b.json`: as chaves que diferem são exatamente as da linha `- A e B diferem em:` de `anuncios/roteiro.md`;
- `git ls-files | grep -ciE "\.(mp4|mov|wav|m4a|mp3)$"` imprime `0`, e o `git grep` do `$PROIBIDO` em todas as revisões não imprime nada;
- `python -m pytest -q` sai 0.
**falha antes:** `ls anuncios/` falha e `ls $VIDEOS/*.mp4` não acha nada hoje.
**prompt de abertura:**

> Você é diretor de criação e vai montar por código os dois anúncios da Vesk, sem rosto nem voz de pessoa real. Comece rodando o `falha antes:` da C1v. Leia a seção C1v, o plano aprovado em 11/11 (no `docs/STATUS.md`), a skill `video`, `docs/hackathon.md` e o `CLAUDE.md`. Faça a parte comum em Python, a prova dos três motores com as mesmas medidas, leve a tabela ao Igor para ele escolher, e monte A e B no vencedor, com a legenda queimada e o gabarito ao lado de cada mp4. Pronto quando os comandos do `verificar:` da C1v passarem.

### C1 — Os anúncios no ar

`padrao` · sonnet · medium · forma: sessao · máquina: qualquer · plan mode: não · contexto: limpo antes

**persona:** produtor de anúncio que põe no ar os dois vídeos curtos da C1v, com o teto do Igor e o dado da curva já correndo.
**dependência:** a C1v está ✅ na fila, e `ls $VIDEOS/a.mp4 $VIDEOS/b.mp4 $VIDEOS/a.gabarito.json $VIDEOS/b.gabarito.json` acha os quatro.
**entra:** `docs/fontes.md` (a curva por segundo da Meta e os pontos de 25 a 100%); `docs/hackathon.md`; os vídeos `A`
e `B` e o roteiro da C1v (`anuncios/roteiro.md`); o teto de gasto, que o Igor fixa. O Igor cria a campanha na conta
da Vesk, marca o segundo da marca assistindo, antes de abrir o gabarito, e aperta publicar; a sessão escreve a lista
de passos e a conferência.
**sai:**
- os dois anúncios da C1v, `A` e `B`, no ar como saíram do render (`$VIDEOS/a.mp4` e `$VIDEOS/b.mp4`, fora do git);
- `docs/anuncios.md`, com:
  - o caminho do roteiro de cada um (`anuncios/roteiro.md`);
  - `- segundo da marca: A = <s>` e `- segundo da marca: B = <s>`, marcados à mão pelo Igor;
  - `- sha256: A = <hash>` e `- sha256: B = <hash>`;
  - `- nome no Gerenciador: A = <nome>` e `- nome no Gerenciador: B = <nome>`, como aparecem no export;
  - `- campanha no ar desde 2026-11-DD, teto de R$ <N>`;
- o primeiro export do Gerenciador, com as colunas de vídeo, em `$VIDEOS/export-meta-<data>.csv`, depois de os dois
  anúncios terem impressão;
- o print do Gerenciador com os dois anúncios ativos, em `$VIDEOS`, tirado pelo Igor.
**verificar:**
- `ffprobe -v error -show_entries format=duration -of csv=p=0 $VIDEOS/a.mp4` e o mesmo para `b.mp4` imprimem um número entre `15` e `30`, e `ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0` imprime `audio` nos dois;
- um `python -c` calcula o sha256 de `a.mp4` e de `b.mp4`: os dois são diferentes entre si e iguais aos de `docs/anuncios.md` e ao `video_sha256` dos gabaritos da C1v; o segundo da marca de cada um é maior que 0, menor que a duração do vídeo, e os dois são diferentes;
- o segundo da marca marcado à mão bate com o `marca_em` do gabarito da C1v, com ±1 s, em `A` e em `B`;
- `grep -cE "^- segundo da marca: (A|B) = [0-9]+$" docs/anuncios.md` e `grep -cE "^- nome no Gerenciador: (A|B) = .+$" docs/anuncios.md` imprimem `2` cada;
- `grep -cE "^- campanha no ar desde 2026-11-[0-3][0-9], teto de R\\$ [0-9]+" docs/anuncios.md` imprime `1`;
- um `python -c` lê o export mais novo em `$VIDEOS/export-meta-*.csv` com o módulo `csv` e exige: a coluna de impressões («Impressões» ou «Impressions») e pelo menos uma coluna de reprodução de vídeo no cabeçalho; uma linha para cada nome no Gerenciador de `A` e de `B`, com impressões maiores que 0 e pelo menos uma coluna de reprodução maior que 0; e o início do relatório («Início dos relatórios» ou «Reporting starts») não anterior à data da campanha;
- o print do Gerenciador com os dois anúncios ativos está em `$VIDEOS`, e o `file` o reconhece como PNG ou JPEG com pelo menos 20 KB (é a confirmação do Igor: sem o acesso de leitura da Marketing API, nenhum comando prova a origem do export).
**falha antes:** `docs/anuncios.md` não existe hoje.
**prompt de abertura:**

> Você é produtor de anúncio e vai pôr no ar os dois vídeos curtos da Vesk que a C1v montou, com o teto do Igor. Comece rodando a `dependência:` e o `falha antes:` da C1. Leia a seção C1, `docs/fontes.md`, `docs/hackathon.md` e `anuncios/roteiro.md`. Escreva com o Igor a lista de passos da campanha na Meta. Quem cria a campanha, marca o segundo da marca assistindo (antes de abrir o gabarito) e aperta publicar é o Igor. Depois que os dois tiverem impressão, peça o export com as colunas de vídeo e confira. Pronto quando os comandos do `verificar:` da C1 passarem.

### C2 — A vitrine e o rascunho

`padrao` · sonnet · medium · forma: sessao · máquina: qualquer · plan mode: não · contexto: limpo antes

**persona:** quem monta a vitrine técnica de um hackathon: repositório limpo, README que se lê em um minuto, página no ar, testes rodando e rascunho enviado.
**entra:** `docs/hackathon.md` (o rascunho pede trilha, repositório público com README, vídeo de até 3 min e página em
HTTPS); o README e a `LICENSE` que já existem; a marca da Vesk (o Igor traz); o domínio `vesklab.com`, no Cloudflare
do Igor.
**sai:**
- a página em `$SITE` por um Worker deste repositório (`site/`, com o `wrangler.toml` ou o `wrangler.jsonc`), em
  inglês em `/` («creative autopilot») e em português em `/pt` («piloto automático do criativo»), sem formulário, com
  o que o add-on faz e o estado do projeto;
- `.github/workflows/testes.yml`, que roda `python -m pytest -q` a cada push, sem `|| true` nem `continue-on-error`, e
  um teste que diz o que evita;
- o roteiro e os slides do vídeo do rascunho;
- o rascunho enviado pelo Igor na trilha Logística & automação, registrado em `docs/hackathon.md` com
  `- rascunho enviado em 2026-11-DD HH:MM, print em <caminho em $VIDEOS>`.
**verificar:**
- `gh repo view IgorLima-py/vesk-hack --json visibility,createdAt -q '[.visibility,(.createdAt>="2026-11-05T00:00:00Z")]|@tsv'` imprime `PUBLIC` e `true`, separados por tab;
- `grep -c "PolyForm Noncommercial License 1.0.0" LICENSE` e `grep -c "polyformproject.org" LICENSE` imprimem `1` cada;
- `git log --format=%cI | sort | head -1 | awk '{print ($0>="2026-11-05T00:00:00Z")}'` imprime `1`;
- `git ls-files | grep -ciE "\.dev\.vars|(^|/)\.env"` imprime `0`, e o `git grep` do `$PROIBIDO` em todas as revisões não imprime nada;
- a página: `site/wrangler.toml` ou `site/wrangler.jsonc` existe; `curl -s -o /dev/null -w "%{http_code}" $SITE/` e o mesmo em `$SITE/pt` imprimem `200`; `curl -s $SITE/ | grep -c '<html lang="en"'` e `curl -s $SITE/pt | grep -c '<html lang="pt-BR"'` imprimem `1`; `/` traz «creative autopilot» e `/pt` traz «piloto automático do criativo»; cada corpo tem pelo menos 1.500 bytes, e os dois são diferentes (`cmp` sai 1);
- nas duas páginas servidas, `grep -c "<form"` e `grep -ciE -f $PROIBIDO` imprimem `0`;
- os testes no push: `grep -c "pytest -q" .github/workflows/testes.yml` imprime pelo menos `1`, e `grep -cE "\|\| *true|continue-on-error" .github/workflows/testes.yml` imprime `0`; `gh run list -R IgorLima-py/vesk-hack --workflow testes.yml --limit 1 --json conclusion,headSha -q '.[0]|[.conclusion,.headSha]|@tsv'` imprime `success` e o mesmo sha de `git rev-parse origin/main`;
- `grep -cE "^- rascunho enviado em 2026-11-[0-3][0-9] [0-2][0-9]:[0-5][0-9], print em " docs/hackathon.md` imprime `1`, e o `file` reconhece o print como PNG ou JPEG com pelo menos 20 KB (é a confirmação do Igor de que viu o rascunho enviado).
**falha antes:** `curl -s -o /dev/null -w "%{http_code}" $SITE/` não imprime `200` hoje, e `.github/workflows/testes.yml` não existe.
**prompt de abertura:**

> Você monta a vitrine técnica do hack. Comece rodando o `falha antes:` da C2. Leia a seção C2, `docs/hackathon.md`, o README e o `CLAUDE.md` (tudo aqui é público). Ponha a página no ar por um Worker, em inglês e português, sem formulário; ligue os testes no push; escreva com o Igor o roteiro e os slides do vídeo do rascunho. Quem envia o rascunho é o Igor. Pronto quando os comandos do `verificar:` da C2 passarem.

### C3 — Os exemplos com gabarito e o contrato do motor

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de teste que fabrica vídeos com a resposta conhecida e escreve o contrato que o motor tem de cumprir.
**entra:** a seção «How it works» do README; o que o motor devolve por vídeo, que o Igor descreve na abertura (o
`eventos.csv` com os eventos por segundo, o `xt.csv` com a linha do tempo por segundo, o `manifesto.json` com as 13
camadas e as versões); `docs/fontes.md`.
**sai:**
- `python -m exemplos.sintetico --marca-em <s> --semente <n> --saida <mp4> [--duracao <d>] [--sem-fala] [--sem-marca]`: um vídeo
  com cortes em segundos conhecidos, o texto «VESK» na tela numa cor pura de RGB fixo e a palavra «Vesk» na voz, a
  partir do segundo `s`, e o `gabarito.json` ao lado (`marca_em`, `cortes`, `fala`, `texto`, `cor_do_texto`,
  `duracao`, `semente`). A voz vem de um TTS que roda sem rede no Windows e no runner do CI; a C3 escolhe e escreve a
  fonte;
- `python -m exemplos.suite --saida <pasta>`: os sintéticos da C7, pelo menos 20, variando o segundo da marca, a
  duração, a fala e os cortes, um `gabarito.json` por vídeo. O piso de 20 tem conta: com 20 acertos em 20, o limite
  de baixo do intervalo de Wilson de 95% fica em cerca de 84% (conta: 20 ÷ (20 + 1,96²));
- `contrato/motor.md` e `contrato/motor.schema.json`: o pedido (o vídeo e o nome da marca), a resposta (os três
  arquivos e o `request_id`, todos obrigatórios, e o `manifesto.camadas` com exatamente 13 itens), os erros (`401`,
  `413`, `415`), a rota de saúde (`GET /saude`, que a C6 chama) e a versão do contrato;
- `contrato/exemplos/resposta-ok.json` e cinco `resposta-ruim-*.json` (sem `request_id`, sem `eventos.csv`, com 12
  camadas, com o segundo como texto, com campo a mais);
- `tests/motor_falso.py`: um servidor local que cumpre o contrato, com `--adulterar sem_request_id`,
  `--adulterar 200_sem_token` e `--adulterar 401_com_token` para provar que o teste de contrato pega cada falha;
- `tests/test_contrato.py`: com `MOTOR_URL` e o token no ambiente, manda o `E1` e confere a resposta, o `401` sem
  token e a rota de saúde; sem eles, pula e diz o motivo;
- os testes `test_sintetico_gabarito`, `test_mesma_semente_mesmo_video` e `test_contrato_schema_valido`, este último
  validando a resposta boa e rejeitando as cinco ruins.
**verificar:**
- `python -m pytest -q` sai 0, e `python -m pytest -q -k "test_sintetico_gabarito or test_mesma_semente_mesmo_video or test_contrato_schema_valido"` imprime `3 passed`;
- `python -m exemplos.sintetico --marca-em 7 --semente 9 --saida <scratch>/x.mp4` sai 0; o `ffprobe` mostra um stream de vídeo e um de áudio, e o `gabarito.json` diz `marca_em: 7`;
- os cortes, conferidos fora de `exemplos/`: `ffmpeg -i <scratch>/x.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null -` lista os tempos de troca de cena, e um `python -c` os acha iguais aos `cortes` do gabarito, com ±0,1 s;
- o texto, conferido fora de `exemplos/`: um `python -c` extrai pelo `ffmpeg` o quadro de `marca_em - 0,5` s e o de `marca_em + 0,5` s em RGB cru e conta os pixels da `cor_do_texto`: `0` no primeiro e pelo menos `500` no segundo; com `--sem-marca`, `0` nos dois;
- rodar duas vezes com `--semente 9` dá o mesmo sha256, e com `--semente 10` dá outro;
- `python -m exemplos.suite --saida <scratch>/suite` sai 0, e um `python -c` conta pelo menos 20 `gabarito.json` e pelo menos 5 valores distintos de `marca_em`;
- um `python -c` fora de `tests/` valida `contrato/exemplos/resposta-ok.json` contra o schema com o `jsonschema` e vê cada `resposta-ruim-*.json` ser rejeitada (5 de 5);
- com o `tests/motor_falso.py` de pé e a `MOTOR_URL` apontando para ele, `python -m pytest tests/test_contrato.py -q -rs` passa sem `SKIPPED`; com cada um dos três `--adulterar`, o mesmo comando sai diferente de 0;
- `python -m pytest tests/test_contrato.py -q -rs`, sem `MOTOR_URL`, imprime `SKIPPED` com `MOTOR_URL` no motivo.
**falha antes:** `python -m exemplos.sintetico --help` dá `No module named exemplos` hoje.
**prompt de abertura:**

> Você é engenheiro de teste e vai fabricar vídeos com a resposta conhecida e escrever o contrato do motor. Comece rodando o `falha antes:` da C3. Leia a seção C3, o README e `docs/fontes.md`, e peça ao Igor o formato do que o motor devolve. Escreva o gerador sintético, a suíte, o contrato com o schema e o teste de contrato que pula sem a URL. Os cortes e o texto se conferem fora de `exemplos/`, pelo `ffmpeg`. Pronto quando os comandos do `verificar:` da C3 passarem.

### C4 — O relatório do Gerenciador

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de integração que lê o arquivo que o gestor já tem e não inventa o ponto que a plataforma não deu.
**dependência:** antes de tudo, `ls $VIDEOS/export-meta-*.csv` acha pelo menos um arquivo (o export da C1). Se não,
pare.
**entra:** `docs/fontes.md` (que o export traga as colunas de vídeo: não achei na doc); o export real da campanha da
C1, em `$VIDEOS/export-meta-*.csv`, aberto antes de escrever código; `docs/anuncios.md`.
**sai:**
- antes do código, nesta seção, a linha `colunas de vídeo da Meta: <lista>`, copiada do cabeçalho do export real, na
  ordem do arquivo;
- `python -m importar ler --arquivo <csv> --anuncio <nome> --saida <curva.json>`: reconhece o export da Meta em
  português e em inglês e grava a curva só com os pontos que estão no arquivo (de 25 a 100%, o tempo médio e os
  segundos, se a coluna existir), marcada «dado da plataforma». Célula vazia vira ponto ausente, nunca 0; coluna de
  vídeo que ele não conhece faz sair diferente de 0, com o nome dela na mensagem;
- `tests/fixtures/meta-export-pt.csv` e `meta-export-en.csv`, com o cabeçalho real e os números trocados por
  sintéticos;
- o TikTok entra só com um export real dele. A C4 escreve no bloco 5 a linha `Export do TikTok`: `respondida`, com o
  fixture e o teste, se houver export real; `fora`, com «sem export real para conferir», se não houver;
- os testes `test_le_export_meta_pt`, `test_le_export_meta_en`, `test_sem_interpolar` e
  `test_coluna_desconhecida_falha_alto`.
**verificar:**
- `python -m pytest -q` sai 0, e `python -m pytest -q -k "test_le_export_meta_pt or test_le_export_meta_en or test_sem_interpolar or test_coluna_desconhecida_falha_alto"` imprime `4 passed`;
- com o export real mais novo da C1, `python -m importar ler --arquivo <export> --anuncio <nome de A> --saida <scratch>/curva.json` sai 0. Um `python -c` fora de `importar/` usa a lista literal da linha `colunas de vídeo da Meta:` desta seção, lê a linha do `A` com o módulo `csv` e acha no `curva.json` exatamente esses pontos, na mesma ordem e com os mesmos valores;
- sem interpolar, no export real: numa cópia no scratch com o valor de uma coluna de vídeo apagado na linha do `A`, o `curva.json` tem um ponto a menos e nenhum valor que não esteja no arquivo;
- coluna desconhecida: com o cabeçalho de uma coluna de vídeo trocado por `X_desconhecida`, `importar ler` sai diferente de 0 e a mensagem de erro contém `X_desconhecida`; o mesmo com o fixture em inglês;
- `grep -cE "^2026-11-[0-3][0-9] \| (respondida|fora) +\| Export do TikTok \|" docs/ROADMAP.md` imprime `1`. Se a linha for `respondida`, `tests/fixtures/tiktok-export*.csv` não está vazio e `python -m pytest -q -k test_le_export_tiktok` imprime `1 passed`; se for `fora`, ela traz «sem export real para conferir».
**falha antes:** `python -m importar --help` dá `No module named importar` hoje.
**prompt de abertura:**

> Você é engenheiro de integração e vai ler o export do Gerenciador sem inventar ponto. Comece rodando o `falha antes:` da C4. Leia a seção C4 e `docs/fontes.md`, e abra o export real da campanha da C1 antes de escrever código. Escreva o `importar` para o export da Meta em português e em inglês, com os fixtures sintéticos, e decida o TikTok pelo export real. Pronto quando os comandos do `verificar:` da C4 passarem.

### C5 — A variante e o 1º teste A/B

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** cientista de marketing que muda uma coisa só no vídeo, prova que só ela mudou, e calcula quanto teste precisa antes de prometer resultado.
**entra:** o `E1` e o gerador da C3; o anúncio `A` da C1v, com o `marca_em` de `$VIDEOS/a.gabarito.json` (e, quando a
C1 fechar, o segundo marcado à mão de `docs/anuncios.md`); a fórmula do teste de duas proporções, escrita do zero com
a fonte; o teto do Igor para o teste. A C5 abre quando a C1v fecha. O passo do teste A/B na Meta, que escreve em
`docs/anuncios.md`, espera a C1 ✅, porque o arquivo é da C1 e o teste precisa da campanha.
**sai:**
- `python -m variante gerar --video <mp4> --marca-em <s> --mudanca marca_no_inicio --saida <pasta>`: pelo `ffmpeg`,
  põe o quadro da marca no 1º segundo. A variante sai sem perda (fora do trecho, cada quadro decodificado é igual ao
  do original), e a mesma entrada dá o mesmo arquivo, byte a byte. O `certificado.json` aponta o original e declara o
  trecho mudado, com o hash de cada quadro fora dele;
- `python -m variante conferir <pasta>`;
- `python -m teste poder --p1 <taxa> --p2 <taxa> --alfa 0.05 --poder 0.8`: o n por braço, com a fórmula e a fonte;
  com `p1` igual a `p2`, sai diferente de 0 e diz que não há efeito a detectar;
- a variante do `A` em `$VIDEOS/variante-a/` (o `variante.mp4` e o certificado), fora do git;
- o 1º teste A/B na Meta, montado à mão pelo Igor no Gerenciador: o `A` contra a variante do `A`, com o teto dele,
  registrado em `docs/anuncios.md` como `- teste A/B no ar desde 2026-11-DD, teto de R$ <N>, variante sha256 <hash>`;
- o `statsmodels` no `requirements-dev.txt`;
- os testes `test_variante_uma_mudanca`, `test_certificado_pega_mudanca_fora` e `test_certificado_pega_copia`.
**verificar:**
- `python -m pytest -q` sai 0, e `python -m pytest -q -k "test_variante_uma_mudanca or test_certificado_pega_mudanca_fora or test_certificado_pega_copia"` imprime `3 passed`;
- com o `E1`, um `python -c` independente decodifica pelo `ffmpeg` os quadros do original e da variante e confere: fora do trecho, todo quadro é idêntico (a variante sai sem perda); o quadro da variante em 0,5 s é idêntico ao do original no segundo da marca e diferente do quadro do original em 0,5 s; os dois mp4 têm a mesma duração e resolução; o trecho do certificado começa no segundo 0;
- `variante gerar` rodada duas vezes com a mesma entrada dá o mesmo sha256;
- controles negativos: com um quadro fora do trecho alterado à mão, `variante conferir` sai diferente de 0; com uma cópia idêntica do original e um certificado que diz que houve mudança, também;
- `python -m teste poder` com os pares (0.30, 0.33), (0.10, 0.12) e (0.50, 0.55) imprime, para cada um, o mesmo n por braço, arredondado para cima, que o `statsmodels` (`NormalIndPower` com `proportion_effectsize`) calcula num `python -c` do `verificar:`; com `--p1 0.05 --p2 0.05`, sai diferente de 0 com a mensagem de que não há efeito a detectar;
- `grep -cE "^- teste A/B no ar desde 2026-11-[0-3][0-9], teto de R\\$ [0-9]+, variante sha256 [0-9a-f]{64}$" docs/anuncios.md` imprime `1`; o sha256 de `$VIDEOS/variante-a/variante.mp4` é o dessa linha, e `python -m variante conferir $VIDEOS/variante-a` sai 0, com o certificado apontando para `$VIDEOS/a.mp4` e para o segundo da marca de `docs/anuncios.md`.
**falha antes:** `python -m variante --help` dá `No module named variante` hoje.
**prompt de abertura:**

> Você é cientista de marketing e vai mudar uma coisa só no vídeo, provar que só ela mudou e dizer quanto teste precisa. Comece rodando o `falha antes:` da C5. Leia a seção C5. Escreva a variante pelo `ffmpeg` com o certificado de pixel, a conferência que pega mudança fora do trecho e cópia disfarçada, e a calculadora de poder com a fórmula e a fonte. Gere a variante do anúncio `A` e ajude o Igor a montar o 1º teste A/B no Gerenciador, com o teto dele; quem publica é ele. Pronto quando os comandos do `verificar:` da C5 passarem.

### C6 — O laudo que cruza

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** analista de criativo que separa o fato medido, e mostrado, da hipótese, e que nunca interpola a curva que a plataforma não deu.
**dependência:** antes de tudo, `curl -s -o /dev/null -w "%{http_code}" -H "Modal-Key: $MOTOR_KEY" -H "Modal-Secret: $MOTOR_SECRET" $MOTOR_URL/saude` imprime `200`. Se não, o motor ainda não subiu: pare.
**entra:** o contrato da C3; o `importar` da C4; `docs/fontes.md`; `docs/anuncios.md`; a linguagem do `CLAUDE.md`.
**sai:**
- `python -m laudo gerar --video <mp4> --marca <nome> --curva <curva.json> --saida <pasta> [--exemplo <pasta>]`, que
  chama o motor e grava o `laudo.json` e a página do laudo em inglês e em português, com:
  - o `marca.segundo` e a `tira`: os quadros de 0 até a marca, com a fala e o texto de cada segundo;
  - o `tempo_medio`, marcado «dado da plataforma»;
  - o `saem_antes`, só nos pontos dados;
  - as `quedas`: os trechos de maior perda entre dois pontos que a plataforma deu, sem ponto inventado. Com a curva
    por segundo (a Insights API, na C9), cada trecho tem 1 s; com os pontos de 25 a 100% do export do Gerenciador,
    vai de um ponto ao seguinte (num vídeo de 20 s, de 25% a 50% é dos 5 aos 10 s). Para cada trecho, o que estava
    na tela e na fala, segundo a segundo, lido da resposta do motor;
  - a receita como hipótese («a prova é o teste»);
- `python -m laudo conferir <laudo.json> --motor <pasta> --curva <curva.json>`, que sai diferente de 0 quando uma
  queda não bate com os segundos da resposta do motor, ou começa ou termina fora de um ponto dado;
- `laudo/exemplo/`: a resposta do motor para o `E1`, gravada pela própria API, com o `request_id` e o sha256; o
  `--exemplo` roda sem chave a partir dela. Sem `--exemplo` e com o token recusado, o `gerar` sai diferente de 0 e
  diz o `401`;
- os laudos dos anúncios `A` e `B`, com a curva do export real, no scratch;
- os testes `test_segundo_da_marca`, `test_meta_sem_interpolar`, `test_queda_cruza_segundo`, `test_tira_de_quadros`,
  `test_exemplo_sem_chave` e `test_laudo_sem_vazamento`.
**verificar:**
- `python -m pytest -q` sai 0 sem `skipped`, e `python -m pytest -q -k "test_segundo_da_marca or test_meta_sem_interpolar or test_queda_cruza_segundo or test_tira_de_quadros or test_exemplo_sem_chave or test_laudo_sem_vazamento"` imprime `6 passed`; numa cópia no scratch em que o `gerar` soma 3 ao `marca.segundo`, `test_segundo_da_marca` fica vermelho;
- a origem do exemplo: chamar o motor de novo, ao vivo, com o `E1` devolve os mesmos eventos por segundo de `laudo/exemplo/eventos.csv` (um `python -c` compara), com outro `request_id`; com `MOTOR_SECRET=errado` no ambiente, `laudo gerar` sem `--exemplo` sai diferente de 0 e a mensagem diz `401`;
- entrada que o exemplo não tem: um sintético novo, `--marca-em 7 --semente 2`, dá no laudo ao vivo `marca.segundo` igual a `7`, com ±1 s; o mesmo com `--sem-marca` dá o laudo sem `marca.segundo`;
- quedas independentes: com a curva por segundo `[100,90,88,60,59,40]`, escrita à mão aqui, `gerar --exemplo laudo/exemplo` grava `quedas` nos trechos `2–3` e `4–5` (em segundos), nessa ordem, e um `python -c` fora de `laudo/` refaz as diferenças e confere;
- o cruzamento: para cada queda, um `python -c` lê o `eventos.csv` de `laudo/exemplo/` e confere que o texto e a fala de `quedas[i]` são os dos segundos do trecho. Controle negativo: com o trecho da queda deslocado 1 s no `laudo.json`, `laudo conferir` sai diferente de 0;
- Meta: `gerar` com uma curva de 3 pontos (25, 50 e 95%) de um vídeo de 20 s, escrita à mão aqui, grava só esses 3 pontos, e as `quedas` só usam os trechos `5–10` e `10–19`;
- a `tira` tem `floor(marca.segundo)+1` quadros; cada um existe no disco e o `ffprobe` o abre com a resolução do vídeo, e o quadro do segundo da marca é diferente do quadro do segundo 0 (sha256 dos pixels);
- com o motor no ar, `gerar` do anúncio `A`, com a curva do export real lida pelo `importar` da C4, sai 0; o `marca.segundo` fica a ±1 s do marcado à mão em `docs/anuncios.md`; e o laudo tem pelo menos uma queda, com o início e o fim de cada uma vindos de pontos que estão no export (o percentual vezes a duração, ou o segundo);
- `git ls-files laudo/exemplo` lista o `eventos.csv`, o `xt.csv` e o `manifesto.json` (o `.gitignore` barra `*.csv` fora das exceções);
- o `git grep` do `$PROIBIDO` em todas as revisões não imprime nada.
**falha antes:** `python -m laudo --help` dá `No module named laudo` hoje.
**prompt de abertura:**

> Você é analista de criativo e vai fazer o laudo que cruza o vídeo com a curva, com o fato separado da hipótese. Confira primeiro a dependência (o motor no ar) e depois rode o `falha antes:` da C6. Leia a seção C6, o contrato da C3, o `importar` da C4, `docs/fontes.md` e `docs/anuncios.md`. Grave a resposta do motor para o `E1` pela API, escreva o `laudo` sem interpolar a Meta e mostre o segundo da marca na tira de quadros. Pronto quando os comandos do `verificar:` da C6 passarem.

### C7 — A precisão medida

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** cientista que mede o próprio instrumento antes de mostrá-lo, com n, intervalo e controle negativo.
**dependência:** a mesma da C6 (o motor no ar).
**entra:** a suíte da C3; o `laudo` da C6; os anúncios `A` e `B`, com o segundo da marca de `docs/anuncios.md`.
**sai:**
- `python -m precisao medir --suite <pasta> --saida docs/precisao.md`: para cada vídeo da suíte e para `A` e `B`,
  chama o motor e compara com o gabarito, por camada: o segundo da marca (±1 s), os cortes (±1 s), a fala com a marca
  e o texto na tela por segundo. Sem o token no ambiente, sai diferente de 0. Grava:
  - cada resposta crua do motor em `precisao/respostas/<request_id>.json`;
  - `precisao/resultados.csv`, uma linha por vídeo e camada, com o esperado, o obtido, o `request_id` e o sha256 da
    resposta crua;
  - a tabela em `docs/precisao.md`, com n, a taxa de acerto e o intervalo de Wilson de 95%, com a fórmula e a fonte;
- o README com a tabela, ou o link para ela, na seção «How it works».
**verificar:**
- `grep -cE "^\| (marca|cortes|fala|texto) \| [0-9]+ \| [0-9]+([.,][0-9]+)?% \| " docs/precisao.md` imprime `4`;
- o n da linha `marca` é o número de `gabarito.json` na suíte mais 2, e `precisao/resultados.csv` tem linhas de `A` e de `B`;
- cada linha de `precisao/resultados.csv` traz o `request_id` e o sha256 da resposta crua guardada em `precisao/respostas/<request_id>.json`; um `python -c` fora de `precisao/` confere os sha256 e recalcula o `obtido` de cada linha a partir da resposta crua;
- sem o token no ambiente, `python -m precisao medir` sai diferente de 0;
- o intervalo de cada camada bate, com ±0,001, com o `proportion_confint(k, n, method="wilson")` do `statsmodels`, num `python -c` do `verificar:`;
- controle negativo, rodando o motor de novo: numa cópia da suíte em que o `marca_em` de um gabarito soma 3, `python -m precisao medir --suite <cópia> --saida <scratch>/p.md` dá uma taxa menor na linha `marca`, e o `obtido` desse vídeo é igual ao do `resultados.csv` original;
- `git ls-files precisao` lista o `resultados.csv` e as respostas cruas de `precisao/respostas/`;
- `grep -c "precisao" README.md` imprime pelo menos `1`.
**falha antes:** `docs/precisao.md` não existe e `python -m precisao --help` dá `No module named precisao` hoje.
**prompt de abertura:**

> Você é cientista e vai medir o motor antes de mostrá-lo. Confira primeiro a dependência (o motor no ar) e depois rode o `falha antes:` da C7. Leia a seção C7, a suíte da C3 e o laudo da C6. Meça por camada contra o gabarito, com n e intervalo de Wilson, e grave o resultado cru que permite recalcular. Pronto quando os comandos do `verificar:` da C7 passarem.

### C8 — A página com envio e o e-mail

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de automação que faz o trabalho do gestor de tráfego rodar sem mão, do vídeo enviado ao laudo na caixa de entrada.
**dependência:** a mesma da C6 (o motor no ar).
**entra:** a página da C2; o `importar` da C4; a `variante` e o `teste poder` da C5; o `laudo` da C6; o `CLAUDE.md` (o vídeo apagado depois do laudo, a
variante que some no prazo, o e-mail que não guardamos e os 30 dias do Resend, o Resend só para o laudo pedido); a conta do Resend, com um domínio de envio próprio
para o laudo (o Igor cria).
**sai:**
- `backend/`, o app no Modal (CPU e `ffmpeg`):
  - `POST /api/laudo`, com o vídeo, o nome da marca, a curva (o export do Gerenciador ou a curva em JSON) e o e-mail
    opcional, devolve um id;
  - `GET /api/laudo/<id>` devolve o laudo quando fica pronto, e `GET /api/saude` devolve `ok`;
  - chama o motor com o token, monta o laudo da C6 com o `motor_request_id`, manda o laudo pelo Resend se houver
    e-mail, e depois apaga o vídeo, o export e o e-mail, também quando o pedido falha. O e-mail nunca vai para o log;
  - no mesmo pedido, gera a variante de uma mudança só, pela `variante` da C5, e o plano do teste, pelo `teste poder`
    (a taxa de base tirada da curva, o efeito mínimo escrito no código com a origem), e devolve os dois junto do
    laudo: a variante para baixar, com o certificado, e o `plano.n_por_braco`;
  - o laudo e a variante somem depois de um prazo escrito no código, com a origem do número; depois dele, o `GET` dá
    `404` ou `410`;
- o Worker serve a página e repassa para o backend com o segredo, que nunca chega ao navegador. A página, nos dois
  idiomas, tem o envio, o progresso, o laudo, os exemplos pré-calculados (o `E1` e o `A`) sempre no ar, e o aviso de
  que o vídeo é apagado, de em quanto tempo o laudo e a variante somem e de que o Resend guarda o envio por 30 dias,
  num elemento com `id="aviso-apagado"`;
- `python -m e2e enviar --video <mp4> --marca <nome> --curva <arquivo> [--email <endereço>]`, contra o site no ar.
**verificar:**
- `curl -s $SITE/api/saude` imprime `ok`;
- pelo `curl`, sem o `e2e`: com um sintético novo, gerado na hora (`--marca-em` sorteado entre 3 e 9, `--semente` tirada do relógio), o `POST /api/laudo` e o `GET` até ficar pronto devolvem um laudo com o `marca.segundo` igual ao do `gabarito.json`, com ±1 s, o sha256 do vídeo enviado e um `motor_request_id`; um `python -c` confere. `python -m e2e enviar`, com outro sintético novo, também sai 0;
- o mesmo vídeo com outra curva devolve outras `quedas`;
- a variante e o plano: o `e2e enviar` baixa a variante e o certificado numa pasta, e `python -m variante conferir <pasta>` sai 0 contra o vídeo enviado; o `plano.n_por_braco` do laudo é igual ao que `python -m teste poder` dá com as taxas que o próprio laudo declara; depois do prazo, o link da variante dá `404` ou `410`;
- com o fixture `tests/fixtures/meta-export-en.csv` como curva, o laudo traz só os pontos do fixture;
- `curl -s -o /dev/null -w "%{http_code}" -X POST $SITE/api/laudo -F video=@<um .txt>` imprime um `4xx`;
- `--email delivered@resend.dev` (o endereço de teste da doc do Resend, conferido na abertura) devolve um id de mensagem, e `GET https://api.resend.com/emails/<id>` dá `last_event` igual a `delivered`; depois, o log do backend exportado pelo `modal app logs` não contém `delivered@resend.dev`;
- o apagamento: o backend não guarda vídeo, export nem e-mail fora do contêiner do pedido. Se ele usa volume do Modal, `modal volume ls <volume>` não lista nada com o id do pedido depois do laudo, nem depois de um pedido que falhou (curva inválida);
- `curl -s $SITE/ | grep -c 'id="aviso-apagado"'` e o mesmo em `$SITE/pt` imprimem `1`, e o aviso diz em quanto tempo o laudo e a variante somem e que o Resend guarda o envio por 30 dias; depois desse tempo, `GET /api/laudo/<id>` dá `404` ou `410`;
- nenhum segredo na página servida: o HTML de `/` e de `/pt` e os scripts que ele carrega não contêm `Modal-Secret`, `re_` seguido de 20 caracteres ou `EAA` seguido de 40;
- `git grep -nE "re_[A-Za-z0-9_]{20,}|EAA[A-Za-z0-9]{40,}|ak-[A-Za-z0-9]{20,}|Modal-Secret: *[A-Za-z0-9]"` não imprime nada.
**falha antes:** `curl -s -o /dev/null -w "%{http_code}" $SITE/api/saude` não imprime `200` hoje.
**prompt de abertura:**

> Você é engenheiro de automação e vai fazer o add-on rodar sem mão, do envio ao e-mail. Confira primeiro a dependência (o motor no ar) e depois rode o `falha antes:` da C8. Leia a seção C8, o `CLAUDE.md`, a página da C2, o `importar` da C4 e o `laudo` da C6. Escreva o backend no Modal e o repasse no Worker, com os segredos fora do git, e o `e2e` contra o site no ar. Pronto quando os comandos do `verificar:` da C8 passarem.

### C9 — O piloto automático na conta da Vesk

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de integração que puxa o dado oficial e não inventa o que a API não deu.
**entra:** a C8; a campanha da C1, com curva; `docs/fontes.md` (o `video_play_curve_actions` e o tempo médio; o acesso
para a conta própria); o token da conta da Vesk, gerado pelo Igor e posto só nos segredos.
**sai:**
- `conector/meta.py`: acha os anúncios de vídeo da conta da Vesk, puxa a curva pela Insights API e devolve só os
  pontos dados; campo que a API não devolveu fica ausente, nunca vira 0;
- um gatilho agendado do Worker que acha anúncio novo, chama o backend e manda o laudo ao Igor pelo Resend, com o id
  do anúncio no corpo. É o laudo que o Igor pediu ao ligar o gatilho, e o e-mail dele mora só nos segredos do Worker. Ele não repete: anúncio que já tem laudo não ganha outro, e cada disparo escreve no log
  `<N> laudos novos`.
**verificar:**
- `python -m pytest -q` sai 0, e `python -m pytest -q tests/test_conector_meta.py` roda pelo menos um teste em que um campo que a API não devolveu continua ausente no resultado, sem virar 0;
- para o anúncio `A`, quem verifica roda na hora um `curl` na Insights API (`video_play_curve_actions`, com o token do ambiente) e um `python -c` compara o número de pontos e cada valor com a curva do laudo de `GET /api/laudo/<id>`: diferença zero;
- o gatilho roda sozinho: o `wrangler tail`, aberto antes do horário agendado, mostra o disparo agendado e uma resposta `200` de `graph.facebook.com` depois de aberto; o disparo seguinte registra `0 laudos novos`;
- o e-mail que chegou ao Igor tem id do Resend com `last_event` `delivered`, e o corpo devolvido pelo `GET https://api.resend.com/emails/<id>` contém o id do anúncio;
- `git grep -nE "EAA[A-Za-z0-9]{40,}"` não imprime nada.
**falha antes:** `python -m conector.meta --help` dá `No module named conector` hoje.
**prompt de abertura:**

> Você é engenheiro de integração e vai fazer anúncio novo da Vesk virar laudo sozinho. Comece rodando o `falha antes:` da C9. Leia a seção C9, `docs/fontes.md` e a C8. Escreva o conector da Insights API e o gatilho do Worker, com o token só nos segredos. Pronto quando os comandos do `verificar:` da C9 passarem.

### C10 — O teste montado sozinho

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de automação que monta o teste sem gastar um centavo sem o sim do dono, e lê o resultado sem enfeitar.
**entra:** a C5 (a variante e o 1º teste, montado à mão); a C9 (o token e o conector); o `CLAUDE.md` (código daqui
cria anúncio só pausado). **Primeiro passo:** achar na doc oficial da Meta se a Marketing API deixa criar o teste A/B
na conta própria com o acesso que o app tem, e escrever a frase e a URL em `docs/fontes.md`. Se não deixar, a C10
escreve no bloco 5 `2026-11-DD | fora | Teste A/B pela API | «<a frase da doc>» (<a URL>) | —`, e o ponteiro segue.
**sai:**
- `python -m teste montar --anuncio <id> --variante <pasta> --teto <R$>`: sobe a variante e cria o teste A/B na conta
  da Vesk, **pausado**, e imprime os ids que criou; quem publica é o Igor. A palavra `ACTIVE` não aparece no código
  de `teste/`;
- `python -m teste ler --estudo <id>`: lê o resultado de um teste (o 1º, da C5, e o montado aqui) e grava no laudo a
  diferença, o intervalo e se o teste teve poder, pela calculadora da C5;
- os testes `test_monta_pausado`, `test_nunca_ativa` e `test_le_resultado_sem_inventar`, contra um servidor falso da
  Graph API.
**verificar:**
- se a doc deixa:
  - `python -m pytest -q` sai 0, `python -m pytest -q -k "test_monta_pausado or test_nunca_ativa or test_le_resultado_sem_inventar"` imprime `3 passed`, e `git grep -c "ACTIVE" -- teste/` imprime `0`;
  - `teste montar` contra a conta da Vesk sai 0 e imprime os ids que criou; um `curl` independente na Graph API em cada um deles mostra `effective_status` igual a `PAUSED`, e o anúncio da variante está entre eles;
  - `python -m teste ler --estudo <o 1º teste>` sai 0; para cada braço, as impressões, o alcance e o gasto são iguais aos de um `curl` independente na Insights API, e o `teve_poder` do laudo é o que um `python -c` com o `statsmodels` recalcula;
- se a doc não deixa: `grep -cE "^2026-11-[0-3][0-9] \| fora +\| Teste A/B pela API \| «.{20,}» \(https://developers\.facebook\.com/[^ )]+\)" docs/ROADMAP.md` imprime `1`, e `grep -F` da mesma frase e da mesma URL em `docs/fontes.md` acha as duas na mesma linha, com a data da leitura.
**falha antes:** `python -m teste montar --help` sai diferente de 0 hoje, porque o `teste` da C5 só tem o `poder`.
**prompt de abertura:**

> Você é engenheiro de automação e vai montar o teste A/B sozinho, sem publicar. Comece rodando o `falha antes:` da C10, e depois ache na doc oficial da Meta se a API deixa criar o teste na conta própria. Leia a seção C10, a C5 e a C9. Monte só pausado; quem publica é o Igor. Leia o resultado do 1º teste sem enfeitar. Pronto quando os comandos do `verificar:` da C10 passarem.

### C11 — Usuários reais

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** quem leva o produto a pessoas de verdade, pede consentimento antes de tudo, e conta só o que aconteceu.
**entra:** a C8 (a página no ar); o `CLAUDE.md` (mensagem em nome do Igor só com o sim dele; nada de dado pessoal no
git); `docs/hackathon.md` (dado e usuário reais pontuam mais, e pagamento real também). **Primeiro passo:** o Igor
decide quem convidar, como, quantos laudos são o alvo, se há pagamento real e se convidar conhecido no Brasil conta
como prospecção (a da Vesk é só nos EUA, pelo `CLAUDE.md`), e isso vai ao bloco 5. O alvo é de
pelo menos 3 laudos (piso da sessão de 05/11, para o alvo não virar 0 ou 1); o Igor só sobe.
**sai:**
- no bloco 5: `2026-11-DD | respondida | Usuários reais | <quem, como, alvo de N laudos, pagamento ou não, convite no Brasil é prospecção ou não> (decisão do
  Igor em 2026-11-DD) | C11`, numa linha só;
- `docs/usuarios.md`: uma linha por pessoa, com um id opaco (`u01`, `u02`...), a data, o `request_id` do laudo e se
  o depoimento foi autorizado; o texto do depoimento só com autorização, e o nome só se a autorização cobrir o nome.
  Nenhum e-mail, telefone ou `@usuário`;
- as autorizações em `$VIDEOS/autorizacoes/`, fora do git, uma por pessoa, com o id opaco no nome do arquivo e a linha
  `nome: sim` ou `nome: não`;
- os depoimentos autorizados na página e no README.
**verificar:**
- `grep -cE "^2026-11-[0-3][0-9] \| respondida \| Usuários reais \| .*alvo de ([3-9]|[1-9][0-9]+) laudos.*\(decisão do Igor em 2026-11-[0-3][0-9]\)" docs/ROADMAP.md` imprime `1`. O piso de 3 é decisão desta sessão (05/11), para o alvo não virar 0 ou 1; o Igor só sobe;
- um `python -c` conta os `request_id` distintos de `docs/usuarios.md` e acha pelo menos o alvo; nenhum é igual a um id de `laudo/exemplo/`, de `precisao/respostas/` ou dos testes;
- cada `request_id` aparece no log do backend, exportado na sessão pelo `modal app logs`, com data depois do fechamento da C8;
- cada linha com depoimento autorizado tem um arquivo não vazio em `$VIDEOS/autorizacoes/` com o id opaco no nome; nome de pessoa só aparece onde esse arquivo traz `nome: sim`;
- um `python -c` tira a coluna do `request_id` de `docs/usuarios.md` e procura no resto: e-mail, telefone (10 ou mais dígitos seguidos, aceitando espaço, traço e parênteses entre eles) e `@usuário`. Não acha nada.
**falha antes:** `docs/usuarios.md` não existe, e a linha «Usuários reais» não está no bloco 5 hoje.
**prompt de abertura:**

> Você leva o produto a pessoas de verdade. Comece rodando o `falha antes:` da C11. Leia a seção C11, o `CLAUDE.md` e `docs/hackathon.md`. Traga ao Igor a decisão de quem convidar, como e se há pagamento, e escreva a linha no bloco 5; quem convida e manda mensagem é ele. Registre cada laudo com id opaco e só o depoimento autorizado. Pronto quando os comandos do `verificar:` da C11 passarem.

### C12 — A demo aguenta o júri

`dificil` · opus · high · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** engenheiro de confiabilidade que trata a página pública como alvo: recusa cedo, nunca cai com 5xx, e avisa antes de alguém reclamar.
**entra:** a C8; o tempo frio e o quente do motor na nuvem, que o Igor traz da medição do repositório do motor; o
custo do Modal (o crédito de US$ 30 por mês); `docs/hackathon.md` (a demo precisa funcionar de 30/11 a 02/12).
**sai:**
- limites no Worker e no backend: o tamanho e a duração máximos do vídeo, cada um com a origem do número no comentário
  ao lado; a taxa por IP, cujo `429` leva o cabeçalho `x-limite: ip`; o número de pedidos simultâneos; um teto de
  gasto por dia. O vídeo fora do limite recebe `413` ou `422` antes de chamar o motor;
- `python -m e2e carga --n <pedidos> --paralelo <n> --suite <pasta>`, que manda sintéticos da suíte ao site, confere
  cada laudo contra o gabarito e imprime quantos deram `200`, `429` e `5xx`, e o p95 do tempo;
- `.github/workflows/vigia.yml`, que chama `$SITE/api/saude` de 30 em 30 minutos, aceita `workflow_dispatch` com a
  entrada `site`, e abre uma issue com o rótulo `vigia` quando falha;
- `docs/demo.md`, com:
  - `- p95 aceito: <N> s (conta: ...)`, a partir dos tempos frio e quente do motor;
  - a decisão de deixar o motor quente ou frio de 30/11 a 02/12, o custo e a conta, na linha
    `- quente de 30/11 a 02/12: <sim|não>, custo de US$ <N> (conta: ...)`, que não passa do crédito de US$ 30 do
    Modal.
**verificar:**
- `python -m e2e carga --n 20 --paralelo 20 --suite <pasta da suíte da C3>`, com sintéticos de 20 a 60 s, sai 0 e imprime `200: 20  429: 0  5xx: 0` e o p95; cada `200` traz o `marca.segundo` do gabarito do vídeo, com ±1 s, e o p95 fica abaixo do teto da linha `- p95 aceito: <N> s (conta: ...)` de `docs/demo.md`;
- 30 pedidos do mesmo IP em 60 s recebem pelo menos um `429` com o cabeçalho `x-limite: ip`;
- um sintético de 180 s e um arquivo maior que o limite recebem `413` ou `422` com o texto do limite, e o log do backend exportado não mostra chamada ao motor para esses dois pedidos;
- o vigia avisa de verdade: `gh workflow run vigia.yml -f site=https://invalido.vesklab.com` abre uma issue com o rótulo `vigia` (`gh issue list --label vigia` acha); depois, a última rodada agendada contra o site real dá `success`;
- `grep -cE "^- quente de 30/11 a 02/12: (sim|não), custo de US\\$ [0-9]+([.,][0-9]+)? \(conta: .+\)" docs/demo.md` imprime `1`, e um `python -c` confere que esse custo não passa de US$ 30 (o crédito mensal do Modal).
**falha antes:** `python -m e2e carga --help` sai diferente de 0 hoje, porque o `e2e` da C8 só tem o `enviar`, e `.github/workflows/vigia.yml` não existe.
**prompt de abertura:**

> Você é engenheiro de confiabilidade e vai preparar a página para o júri. Comece rodando o `falha antes:` da C12. Leia a seção C12, a C8 e os tempos do motor na nuvem que o Igor traz. Ponha os limites com a origem de cada número, o teste de carga, o vigia e a decisão de quente ou frio com o custo. Pronto quando os comandos do `verificar:` da C12 passarem.

### C13 — O vídeo e a submissão

`criativo` · opus · xhigh · forma: sessao · máquina: qualquer · plan mode: sim · contexto: limpo antes

**persona:** quem conta em 3 minutos, em inglês, por que o trabalho do gestor de tráfego agora roda sozinho, e mostra a demo funcionando.
**entra:** da C1 à C12; `docs/hackathon.md` (vídeo de até 3 min com demo, os 4 critérios, a final presencial);
`docs/precisao.md`; `docs/usuarios.md`; a marca da Vesk; a skill global `video` (o mapa dos jeitos de fazer vídeo, em
`~/.claude/skills/video/SKILL.md`) e o pipeline de legenda da C1v (`anuncios/`), que serve à legenda em português. O
vídeo de demo, com gravação de tela e áudio, não entrou na pesquisa de 11/11: a C13 confere esse pedaço antes de
gravar.
`VIDEO=C:/Users/Usuario/Desktop/Side-Projects/vesk-hack-videos/final.mp4` fica fora do git, e o README cita a URL
publicada.
**sai:**
- o roteiro e o vídeo em inglês, com legenda em português, gravado pelo Igor, com a demo rodando;
- o README final, com `## Track`, `## Run locally` (o modo de exemplo, sem chave, que grava o laudo do `E1`) e
  `## License`, e a URL do vídeo;
- a submissão pelo Igor até 30/11 às 23h59 (alvo 28/11), registrada em `docs/hackathon.md` como
  `- submetido em 2026-11-DD HH:MM, print em <caminho em $VIDEOS>`;
- `docs/final.md`: a solução da final presencial desenhada, sem construir.
**verificar:**
- `ffprobe -v error -show_entries format=duration -of csv=p=0 $VIDEO` imprime um número entre `120` e `180`, e o `ffprobe` dos streams mostra vídeo e áudio;
- `grep -cE "^## (Track|Run locally|License)" README.md` imprime `3`. Num clone novo no scratch, o comando de `## Run locally`, rodado com `env -i PATH="$PATH"`, sai 0 e grava o laudo do `E1` com o `marca.segundo` do gabarito, com ±1 s (um `python -c` confere);
- a URL do vídeo no README termina em `200` no `curl -sIL`;
- no dia da submissão, o `e2e enviar` da C8, com um sintético novo, passa contra o site no ar;
- `grep -cE "^- submetido em 2026-11-[0-3][0-9] [0-2][0-9]:[0-5][0-9], print em " docs/hackathon.md` imprime `1`, com data e hora até 30/11 às 23h59; o `file` reconhece o print como PNG ou JPEG com pelo menos 50 KB;
- o `git grep` do `$PROIBIDO` em todas as revisões não imprime nada; e, num clone no scratch com um commit que planta uma palavra proibida, o mesmo comando a acha (o controle positivo).
**falha antes:** o `grep` da submissão imprime `0` hoje, e `$VIDEO` não existe.
**prompt de abertura:**

> Você conta em 3 minutos, em inglês, por que o trabalho do gestor de tráfego agora roda sozinho. Comece rodando o `falha antes:` da C13. Leia a seção C13, `docs/hackathon.md`, `docs/precisao.md` e `docs/usuarios.md`. Escreva o roteiro com a demo, o README final com o modo de exemplo sem chave, e desenhe a final presencial. Quem grava e submete é o Igor. Pronto quando os comandos do `verificar:` da C13 passarem.

---

## 4. Tabela de escape

Para quando o trabalho **não** é uma fatia, que é a maioria dos dias.

| O que se vai pedir | Perfil |
|---|---|
| mudar texto, cor, tamanho, uma palavra | `ajuste` |
| mudar o comportamento de algo que já funciona | `padrao` |
| um bug que se **consegue** reproduzir | `padrao` |
| um bug que aparece **às vezes** | `dificil` |
| **não sei descrever o problema direito** | `dificil` |

A regra em uma linha: *«às vezes» e «não sei por quê» pedem mais esforço; o resto não.*

---

## 5. Decisões da entrevista

Uma linha por decisão, só acrescentada, nunca reescrita. Quando duas linhas tratam da mesma coisa, vale a mais nova.

```
2026-11-05 | respondida | Trilha | Logística & automação; o tema: «Projetos que movem bens, informação ou trabalho de forma mais eficiente.» (fonte: https://hackbrasil.com/regulamento) | todas as fatias
2026-11-05 | respondida | O que é | o piloto automático do criativo: puxa o vídeo e a curva, o motor lê cada segundo, cruza os dois e entrega o laudo, a variante e o plano do teste | todas as fatias
2026-11-05 | respondida | O motor | um serviço privado, chamado por API com token; o júri lê e testa este código, e o motor é serviço externo, como a organização aceitou por escrito, desde que a demo funcione inteira | C3, C6
2026-11-05 | respondida | Onde roda | a página num Worker; o backend e o motor no Modal, escalando a zero; sem login, banco, OAuth ou painel | C2, C8
2026-11-05 | respondida | Licença | PolyForm Noncommercial 1.0.0 | C2
2026-11-05 | respondida | E-mail | o Resend envia só o laudo pedido, para o e-mail digitado, que nós não guardamos (o Resend guarda o envio por 30 dias, e a tela diz isso); nunca prospecção | C8
2026-11-05 | respondida | Teto de horas | sem teto; o limite é 30/11 às 23h59 | —
2026-11-05 | respondida | Time e idioma | o Igor sozinho, com o Claude de par; o vídeo em inglês com legenda em português; a página nos dois | C2, C13
2026-11-05 | respondida | Anúncios | campanha pequena da Vesk na Meta, com o teto do Igor, desde a C1; o 1º teste A/B por volta de 10/11, montado à mão | C1, C5
2026-11-05 | respondida | Exemplos | vídeos sintéticos com gabarito por construção, e os anúncios da Vesk com o segundo da marca marcado à mão | C3, C7
2026-11-05 | respondida | Ordem de corte | se faltar tempo, cai a C10, depois a C11; a C12 e a C13 não caem | o calendário
2026-11-05 | fora       | Dado de terceiros fora de API oficial | nenhum vídeo, curva ou número coletado de site de terceiros entra aqui | —
2026-11-05 | fora       | Perfil, concorrente, séries temporais, TikTok pela API, laudo escrito por IA, WhatsApp ou Slack | ficam fora do hack | —
2026-11-05 | aberta     | Usuários reais | quem convidar, como, o alvo e se há pagamento real: decisão do Igor | C11
2026-11-05 | aberta     | Teste A/B pela API | se a Marketing API deixa criar o teste na conta própria com o acesso do app | C10
2026-11-05 | respondida | E-mail do piloto automático | o laudo dos anúncios da própria conta da Vesk vai para o Igor, que o pediu ao ligar o gatilho; o e-mail dele mora só nos segredos | C9
2026-11-05 | respondida | A demo entrega as três coisas | a página devolve o laudo, a variante e o plano do teste, não só o laudo | C8
2026-11-05 | respondida | Palavras proibidas | moram num arquivo fora do git, porque a lista escrita aqui já seria o vazamento | todas as fatias
2026-11-05 | respondida | Queda sem a curva por segundo | com os pontos de 25 a 100% do export, a queda é o trecho entre dois pontos dados, nunca um segundo interpolado | C6
2026-11-09 | respondida | Ondas e orquestrador | a fila anda em paralelo, em ondas, tocada por uma sessão orquestradora que abre cada fatia no seu worktree; o maestro do playbook fica fora (recusa repositório público e toca uma fatia por vez); a cota acabar mais rápido está aceita (decisão do Igor em 2026-11-09) | todas as fatias
2026-11-11 | respondida | Os vídeos A e B | montados por código (rosto e voz gravados pelo Igor no celular; texto, marca e legenda compostos no Remotion), com o gabarito ao lado de cada mp4, numa fatia nova, a C1v, antes da C1; a C5 passa a esperar o vídeo `A` da C1v; o mapa dos jeitos de fazer vídeo mora na skill global `video`, fora deste git (decisão do Igor em 2026-11-11) | C1v, C1, C5, C13
2026-11-11 | respondida | Os vídeos A e B, de novo | sem rosto nem voz do Igor nem de pessoa real (vale sobre a linha anterior); inglês, público EUA; a marca é o wordmark do visual do site; A e B diferem só na posição da cartela da marca (perto de 14 s e perto de 3 s), numa chave só, `ordem`; imagem em motion por código; voz Kokoro `af_heart` e logo sonoro gerado no `ffmpeg`, sem trilha; o motor sai de uma prova com Remotion, HyperFrames e Revideo, medidos pelos mesmos comandos, e o Igor escolhe; o que a prova ensinar vai para a skill `video`, para todos os repositórios (decisão do Igor em 2026-11-11) | C1v, C1, C5, C13
2026-11-11 | respondida | Os motores da prova | quatro frentes: Remotion, HyperFrames, Revideo e FrameFields (vale sobre a lista da linha anterior), depois da `/pesquisa` completa, com a varredura do GitHub, o conferente e o conferidor; o FrameFields entra porque não usa navegador e promete o mesmo quadro, e o Revideo fica para a prova medir se renderiza no Windows (decisão do Igor em 2026-11-11) | C1v
```
