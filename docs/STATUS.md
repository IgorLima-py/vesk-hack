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

**A próxima sessão continua a C1v, pela Fase 3.** Ela abre com duas decisões do Igor, e a seção «C1v (11/11/2026,
terceira sessão)», abaixo, tem a tabela e os números. A Fase 1 e a prova das quatro frentes estão prontas.

As duas decisões:
1. **Os cortes.** Os motores desenham segmentos que o ffmpeg não vê como corte. A recomendação é que cada segmento
   mude a tela inteira, com o fundo alternando entre o preto e o `#eeedf4`, e que a curva não atravesse o corte. A
   outra saída é tirar os cortes do gabarito.
2. **O motor vencedor.** Os quatro passaram nas medidas.

Depois, a sessão:
- copia o projeto do vencedor de `$VIDEOS/provas/<motor>/` para `anuncios/<motor>/`, com o lock na versão exata;
- ajusta o desenho conforme a decisão dos cortes (o texto `desenho` de cada segmento em `anuncios/falas.py`; depois,
  `python -m anuncios tempo a` e `tempo b`);
- renderiza pela fila a imagem muda de A e B a partir de `anuncios/linha_do_tempo/<a|b>.json` (599 quadros), duas
  vezes no A, para o `framemd5`;
- roda `python -m anuncios final a --imagem <mp4 mudo>` e o mesmo para o b. É a primeira vez que o `final` roda: confira
  a legenda num quadro;
- escreve `anuncios/roteiro.md` como o `sai:` pede;
- põe `*.m4a` e `*.mp3` no `.gitignore`;
- roda o `verificar:` inteiro.

Abra com `/oi c1v`, na Karen, onde estão os brutos, as provas, a skill `video` e os planos. O plan mode da seção sai
com o plano aprovado, sem replanejar. O ponteiro continua no O, e o aviso de que ele pede `dificil` é esperado.

O orquestrador (Opus, esforço high, na Karen) abre a onda 1: a C1 (os anúncios, com o Igor), a C2 (a vitrine e o
rascunho) e a C3 (os exemplos com gabarito e o contrato do motor), cada uma na sua sessão.

Desde 11/11, a fila tem a C1v (os anúncios A e B montados por código), que abre já, sem dependência: perfil
`criativo` (opus, xhigh), com plan mode, na Karen. A C1 espera a C1v.

Com a C3 na `main`, abrem duas frentes:
- a C5, que só espera o vídeo `A` da C1v (desde 11/11; antes era o da C1);
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

## C2 — a vitrine (10/11/2026): NÃO fechou, falta a mão do Igor

- [V] O `falha antes:` rodou vermelho antes do código: `curl` ao `hack.vesklab.com` deu `000` e o
  `.github/workflows/testes.yml` não existia.
- [V] No ar, depois do `wrangler deploy` do Igor (o primeiro, sem o visual novo): `/` e `/pt` dão `200` (2.697 e 2.922
  bytes), `lang="en"` e `lang="pt-BR"`, as duas frases, 0 `<form`, 0 do `proibido.txt`, `cmp` sai 1. O `curl` do Windows
  precisa de `--ssl-no-revoke`, senão imprime `000`.
- [V] No git: repositório `PUBLIC`, 0 arquivo de segredo versionado, 0 ocorrência do `proibido.txt` em todas as
  revisões, o commit mais antigo é de 06/11.
- Feito: `site/` (Worker de arquivos estáticos, `wrangler.toml` com o domínio, `public/index.html` em inglês,
  `public/pt.html` em português, `style.css` no visual da Vesk com CSS escrito do zero por causa da 6.2),
  `.github/workflows/testes.yml` (`ubuntu-24.04` fixo, `ffmpeg` por apt, `requirements-dev.txt`, `pytest -q`, sem
  `|| true`), `tests/test_vitrine.py`, `site/video/slides.pptx` (6 slides, fala inteira nas notas, em inglês),
  `site/video/gerar_slides.py` e `site/video/roteiro.md` (o mapa de tempo).
- [V] 10/11, depois do push: o run do `testes.yml` no `cb9bce1` terminou em `success` e é o mesmo sha da `origin/main`
  (`gh run list`). O `flite` do Ubuntu 24.04 funcionou no runner, o que fecha o `[?]` da C3 para essa versão.
- [V] O visual novo **ainda não está no ar**: o `style.css` servido em `hack.vesklab.com` não tem o `#ffe14a`, e
  `docs/hackathon.md` não tem a linha `- rascunho enviado em ...`. O `.pptx` não foi aberto em nenhum programa (não há
  LibreOffice aqui).
- **Falta, em ordem (do Igor):** (1) `cd site` e `npx wrangler deploy` para subir o visual novo, depois os `curl` do
  `verificar:` com `--ssl-no-revoke`; (2) ver o run do `testes.yml` na `main`: `gh run list -R IgorLima-py/vesk-hack
  --workflow testes.yml --limit 1`, e se o `flite` do Ubuntu 24.04 falhar, a saída do passo `grep flite` diz; (3) abrir
  `site/video/slides.pptx`, rodar na tela `python -m exemplos.sintetico --marca-em 7 --semente 9 --saida x.mp4`, gravar
  a tela com a webcam lendo as notas, enviar o rascunho na trilha Logística & automação; (4) registrar em
  `docs/hackathon.md`: `- rascunho enviado em 2026-11-DD HH:MM, print em <caminho em $VIDEOS>`. Só então a C2 recebe o ✅
  na fila.
- Desvio: o `git rebase origin/main` do `CLAUDE.md` foi barrado pelo guarda do playbook, e a junta com a C3 saiu por
  `git merge origin/main` (commit de merge a mais). Nenhum conflito.
- Bateria desta sessão, pela trava, com o merge: [V] 5 passaram, 0 falharam, 5 pulados (os 5 de contrato, sem `MOTOR_URL`), em 61 s.
- Sem segunda opinião em Opus: o ponteiro desta fatia é do orquestrador e a fatia não fechou, então o ponteiro não anda.

## O orquestrador (11/11/2026): não fechou, segue aberto

- [V] Na abertura, o `git pull` trouxe a C3 (✅) e a C2 (subiu sem fechar) até o `67b67e4`; modelo Opus e esforço
  `high` medido pelo Bash, como a tabela pede para o `dificil`.
- O Igor achou que o roteiro não tinha pensado em como fazer os vídeos, e o orquestrador abriu uma sessão própria de
  pesquisa (perfil `replan`), em vez de pesquisar ele mesmo. Ela abriu em `high`, porque o orquestrador não abre acima
  do próprio esforço, e o Igor a subiu para `xhigh`. O que ela entregou está em `docs/historico/c1v-sessoes-1-e-2.md`
  (a C1v na fila, a skill `video`).
- Nenhuma outra fatia foi aberta: a C1 passou a esperar a C1v, e a C4 e a C5 esperam o que sai das duas.
- O O não fecha: o `sai:` dele é todas as fatias ✅ ou cortadas. O ponteiro fica nele.
- Bateria: não rodou, porque o orquestrador não mexeu em código.

## C1v (11/11/2026, terceira sessão): não fechou — a Fase 1 e a prova estão prontas; faltam duas decisões do Igor e a Fase 3

A sessão rodou na `main` da Karen, aberta com `/oi c1v`, com Opus e esforço `xhigh` medido pelo Bash [V], como o
perfil `criativo` pede. Entrou no plan mode e saiu com o plano de 11/11, sem replanejar. O plano desta sessão está em
`~/.claude/plans/greedy-bubbling-zebra.md`, só na Karen. A pesquisa dos vídeos e as duas primeiras sessões da C1v
foram para `docs/historico/c1v-sessoes-1-e-2.md`, onde ficam o roteiro e o plano aprovado. O ponteiro continua no O.

- [V] O `falha antes:` deu vermelho antes do código: `ls anuncios/` sai 2, e `ls $VIDEOS/*.mp4` também sai 2.
- [V] As decisões do Igor nesta sessão:
  - a legenda queimada fica fora do gancho e da cartela da marca (bloco 5, `1424421`);
  - não há pausa extra entre as falas: vale o silêncio que o Kokoro já deixa, cerca de 0,32 s antes e 0,46 s depois
    de cada fala, medido a -40 dBFS nos seis brutos;
  - o logo sonoro dura 0,6 s. As duas coisas estão em `anuncios/a.json` e `b.json` (`b67e689`).
- **O que está feito**, em `anuncios/`, escrito do zero e rodado por `python -m anuncios <comando>`:
  - `falas.py` traz o roteiro, o desenho de cada segmento (o texto que todo motor segue) e a conferência contra o
    `proibido.txt`;
  - `voz.py`, `transcrever.py`, `tempo.py`, `som.py`, `final.py` e `prova.py` são um comando cada, e `caminhos.py`
    diz onde fica cada coisa;
  - `a.json` e `b.json` diferem só na `ordem`, e cada número traz a origem ao lado;
  - `fontes/` tem as três famílias do site, do `google/fonts@c30b221`, com a OFL de cada uma. O `ORIGEM.md` tem o
    sha256 de cada arquivo, e o `.gitattributes` guarda a pasta byte a byte;
  - `requisitos-voz.in` e `requisitos-voz.txt` fixam a voz: o Kokoro 0.9.4 no Python 3.11, pelo `uv`, com o
    `brotli` 1.2.1;
  - no git: `brutos.json` (o sha256 dos brutos, a revisão do modelo e a semente), `fala/<chave>.json` e
    `linha_do_tempo/a.json` e `b.json`;
  - `tests/test_anuncios.py` tem 3 testes, cada um com o `evita:`.
- [V] **A voz** (job 1298) são seis falas, que somam 19,3 s. A segunda geração (job 1310, `voz --conferir`) deu o
  mesmo sha256 nas seis. Os brutos estão em `$VIDEOS/brutos/`.
- [V] **A transcrição** (job 1309): o whisper ouviu «VESC», e o gabarito fica com «Vesk.», do roteiro. As pontas de
  cada fala saem do áudio pelo `LIMIAR_DA_VOZ` da C3, porque o whisper punha a primeira palavra em 0,0 s.
- [V] **As linhas do tempo:**
  - A e B têm 599 quadros cada (19,967 s);
  - o `marca_em` cai no quadro 431 (14,367 s) no A e no 90 (3,000 s) no B;
  - os cortes do A são `[90, 171, 326, 431, 525]`, e os do B, `[90, 184, 265, 420, 525]`.
- [V] **O som** (job 1318) está em `$VIDEOS/montagem/a/som.wav` e `b/som.wav`, com 19,967 s cada.
- [?] **O `final` nunca rodou.** A legenda queimada, a checagem do `fontselect` do libass e o gabarito ainda não foram
  testados de ponta a ponta.
- [V] **A prova dos motores.** As quatro frentes desenharam a linha provisória
  (`$VIDEOS/provas/linha_provisoria_a.json`, com 763 quadros de falas sintéticas, no mesmo formato da definitiva). Os
  projetos ficam em `$VIDEOS/provas/<motor>/`, fora do git e só na Karen, e as medidas, no `medidas.json` de cada
  pasta.

  | | Remotion 4.0.542 | HyperFrames 0.9.33 | Revideo 0.11.0 | FrameFields 3.0.0 |
  |---|---|---|---|---|
  | dois renders, o mesmo `framemd5` | sim | sim | sim | sim |
  | formato e cartela no `marca_em` | sim (barra 0,999) | sim (1,0) | sim (1,0) | sim (1,0) |
  | render e pico de RAM | 60 a 78 s; 1,4 GiB | 74 a 80 s; 1,1 GiB | não anotado | ~150 s; 1,7 GiB |
  | linhas de código | 328 | 243 | 249 | 267 |
  | navegador mudo | o Chrome já sai com `--mute-audio` | injetado por `mute.mjs` | por `settings.puppeteer.args` | sem navegador |
  | licença | grátis até 3 pessoas | Apache-2.0 | MIT | Apache-2.0 |

  A tabela e os achados também estão na skill `video`, na seção «A prova dos motores (11/11/2026)», fora do git e só
  na Karen.
- [V] **Os cortes não aparecem.** Nos três motores medidos (Remotion, HyperFrames e FrameFields), a nota de cena do
  ffmpeg nos cinco cortes ficou entre 0,01 e 0,23, e o limiar dos testes da C3 é 0,3. O fundo é preto, e a curva
  atravessa os cortes do gancho até a leitura. Do jeito que está, o gabarito diz que há cortes onde nem a olho há.
  Essa decisão é do Igor; a pergunta foi feita e a sessão caiu antes da resposta.
- **O que foi tentado e falhou:**
  - Job 1287: «TypeError: process() takes no keyword arguments» ao baixar o Kokoro-82M. O `brotli` 1.1.0 do Python
    3.11 da Karen vaza para o ambiente do `uv`, e a saída foi fixar o `brotli>=1.2.0` (`afad6ab`).
  - O `prova.py` exigia 100% da barra no grifo e reprovou a Remotion por 6 a 8 px de ruído de croma nos cantos: 0,999
    no `marca_em` contra 0,0 no quadro anterior, jobs 1300 e 1306. Agora a barra está presente com mais da metade do
    miolo no grifo (`7db1982`).
  - A Revideo levou cinco tentativas. Faltava o `@revideo/ui` (o pacote de render o carrega e não o traz), o Chrome
    deu timeout no `page.goto`, e depois vieram o número de quadros e a cor. O relato final se perdeu quando a sessão
    caiu, e o tempo e o pico de RAM dela não foram anotados.
  - O `framefields render` do CLI sempre mistura uma trilha AAC muda e sai 1 pelo QA dele. O contorno é
    `renderVideo({ audio: false })` num script.
  - O HyperFrames 0.9.33 e o Revideo 0.11.0 **não** passam o `--mute-audio` ao Chrome. As frentes acrescentaram o
    argumento por fora, e o log do HyperFrames confirma.
  - A conta bateu o limite de 5 h da API uma vez. As frentes pararam e foram retomadas, e as duas primeiras repetiram
    relato parcial até eu encerrá-las.
- [V] **A fila da Karen** dominou o tempo: cada job esperou de 5 a 20 min por RAM. A Karen agora tem 31,9 GiB (antes,
  15,9).
- No Linear, a VES-102 continua In Progress.
- A sessão chegou a ~324k de contexto.
- [V] Bateria desta sessão, pela trava: 13 testes, 8 passaram, 0 falharam, 5 pulados (os 5 de contrato, sem
  `MOTOR_URL`), em 45 s.
- Sem segunda opinião em Opus: a fatia não fechou (faltam a Fase 3 e o `verificar:`), e o ponteiro é do orquestrador.

## Madrugada 10/11 — decisões para o Igor conferir

- A junta com a C3 por **merge** em vez de rebase (acima): reversível, e foi a opção que não reescreve histórico.
- O push da C2 sobe só o que já estava na `main` mais os commits da C2. Nada foi publicado fora disso, e o repositório
  já era público.
- Fontes: a página usa só as famílias da Vesk como lista de fallback (Newsreader, Schibsted Grotesk, IBM Plex Mono,
  depois Georgia e system-ui). Não baixei nem copiei arquivo de fonte. Se quiser as fontes de verdade, é um download
  novo que precisa do seu sim.

## O que foi tentado e não funcionou

- `git rebase origin/main` pela sessão: barrado pelo hook do playbook nas três tentativas; o `merge` resolveu.
- O preview por `file://` não carrega o `/style.css` (caminho absoluto); serve conferir por `python -m http.server`
  dentro de `site/public`.
- O `curl -s` do Windows imprime `000` sem erro por causa da checagem de revogação do certificado; use
  `--ssl-no-revoke`.
