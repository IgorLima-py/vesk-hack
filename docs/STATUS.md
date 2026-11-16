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

**A próxima sessão continua a C1v com a terceira volta dos anúncios, no Mac, numa sessão nova com os plugins
Motion Reel e Design carregados.** Os quatro vídeos (A2, B2, A3 e B3) passam no `verificar:`, mas o Igor quer mais
movimento, mais cor, um logo sonoro novo e menos «cara de ia». As notas dele estão na seção «C1v (16/11/2026, quinta
sessão)», abaixo, e o plano está no fim de `anuncios/storylines.md`.

Em ordem:
1. **Abra:** `/oi c1v`, no Mac, com Opus xhigh (perfil `criativo`).
   - Exporte `VIDEOS=$HOME/Desktop/Side-Projects/vesk-hack-videos` e ponha `~/.local/ffmpeg-full/bin` na frente do
     PATH.
   - O trabalho pesado vai com `gpu_reserve` e roda do Bash: a fila não executa arquivo que a sessão criou.
2. **Leia antes de mexer:**
   - as referências oficiais do HyperFrames: `motion.md`, `sound.md` e `film.md`, em
     `anuncios/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/references/`;
   - o `SKILL.md` do Motion Reel.
3. **O som primeiro, e mostre ao Igor só o som antes de mexer na imagem:**
   - o logo sonoro novo, com três notas de sino em FM, uma para cada ponto do selo, em 2 a 3 s;
   - uma trilha discreta, sintetizada com o `dsp.py` do Motion Reel (MIT; a cópia anota a origem com URL e versão),
     de 18 a 24 dB abaixo da voz;
   - dois ou três takes do sopro, alternados, com o pico um quadro depois da imagem;
   - a mistura a cerca de -14 LUFS e -1 dBTP.
4. **O movimento e a cor, na história 2 primeiro** (a que o Igor preferiu):
   - a câmera nunca para, com aproximação em escala logarítmica;
   - as entradas têm direção e peso, com molas e uma curva por papel, sem «tudo entra com fade»;
   - algo novo a cada 2 a 4 s;
   - mais cor nos fundos e nos cartões;
   - os cortes continuam secos.
5. **A crítica:** três rodadas nas folhas de quadros, com o `prompts/critique-pass.txt` do Motion Reel e a skill
   `design-critique` do Design, até nota 8 em tudo, antes de mostrar.
6. **O render e a conferência:**
   - renderize de novo os quatro pelos comandos de `anuncios/roteiro.md` (o A duas vezes);
   - rode o `verificar:` em cada par;
   - atualize o `roteiro.md`: a nota de cena e o sha256 dos brutos, se a voz mudar.
7. **No fim:** peça ao Igor que desinstale os dois plugins. O pedido é dele, e daqui não há ferramenta para isso.

Duas decisões continuam com o Igor:
- **Os nomes dos vídeos:** o `sai:` pede `$VIDEOS/a.mp4` e `b.mp4`, e saem quatro. Ou um par vira o `a`/`b` do
  `sai:`, ou o `sai:` muda.
- **O teste A/B da ordem:** roda com uma história ou com as duas.

O ponteiro continua no O, e o aviso de que ele pede `dificil` é esperado.

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
  este repositório. Em outra, o `test -s` do bloco 3 barra a fatia até o arquivo ser copiado de lá. No Mac, desde
  16/11, há uma versão provisória escrita pela C5 a pedido do Igor (a seção da C5, abaixo).
- No Mac, o `ffmpeg` com `flite` é o de `~/.local/ffmpeg-full/bin` (C5, 16/11); o do Homebrew não roda o `E1`.
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

## C1v (16/11/2026, quinta sessão, no Mac): não fechou — quatro vídeos prontos e conferidos; o Igor quer uma terceira volta

Aberta pelo orquestrador no Mac, no worktree `c1v-mac-7e4e63`, porque a Karen está em conserto. Sobre o que a quinta
sessão da Karen mostrou, o Igor respondeu «Nada, recomece». As sessões 3 e 4 da C1v foram para
`docs/historico/c1v-sessoes-3-e-4.md`.

- **As decisões do Igor nesta sessão:**
  - [V] **O redesenho pelo vesklab.com:** achou «anos luz melhor». Depois pediu uma segunda volta, com o logo melhor,
    mais cor e o anúncio parecendo anúncio. Ela trouxe o selo de três pontos grande e em cor, manchas da paleta, o
    anúncio no cartão de um vídeo patrocinado genérico («yourbrand», «Sponsored», «Shop now») e as palavras do teste
    A/B na tela (Control, Variant, Drop-off). Com ela, escolheu as duas histórias: «faz os dois, gostei dos dois».
    Cada uma sai em A e em B, que diferem só na `ordem`, e são quatro vídeos.
  - [V] **Depois de ver os quatro vídeos:**
    - a história 2 está melhor, mas ainda tem «cara de ia»;
    - falta movimento e cor;
    - o logo sonoro está ruim;
    - «hack.vesklab.com» não é amigável, e o endereço vira `vesklab.com`.
  - [V] **Os plugins:** pediu a pesquisa funda, instalou o Motion Reel e o Design para a próxima volta e pediu que
    sejam desinstalados quando ela terminar.
- **O que foi feito:**
  - [V] **O projeto do HyperFrames:** está em `anuncios/hyperframes/`, com o HyperFrames 0.9.33 e o GSAP 3.15.0 do
    lock. Tem as cenas das histórias 2 e 3 (`compositions/h2-*`, `h3-*`, `marca`, `chamada`), o kit
    `assets/kit.js` (o campo de pontos, `aura`, o cartão do anúncio e o mosaico) e o Chrome mudo.
    - O Chrome mudo é `mudo/chrome-headless-shell`, um script que chama o Chrome do HyperFrames com `--mute-audio`.
      O HyperFrames o abre por `HYPERFRAMES_BROWSER_PATH`.
  - [V] **O texto na tela por história:**
    - o `tela` e o `desenho` de `anuncios/falas.py` têm uma lista para a 2 e outra para a 3;
    - a linha do tempo leva um gabarito de texto por história;
    - `python -m anuncios cenas a|b --historia 2|3` gera a raiz;
    - o `final` recebe `--historia` e grava `$VIDEOS/<a|b><história>.mp4`.
  - [V] **A voz no Mac:** o `voz --conferir` deu os seis sha256 diferentes dos da Karen (ARM contra x86). Cada fala
    tem as mesmas amostras, e as pontas da fala são iguais até o milésimo. A linha do tempo não mudou: 599 quadros,
    `marca_em` nos quadros 431 e 90 e os mesmos cortes. O `anuncios/brutos.json` agora tem os brutos do Mac.
  - [V] **O som:** um sopro antes de cada corte, menos o da cartela, e um clique em «one» e em «Upload». Os dois são
    da biblioteca do HyperFrames, sob a Pixabay Content License, conferidos pelo sha256 (`anuncios/som.py`).
  - [V] **A Fase 3:** os quatro renders (cerca de 40 s cada, SwiftShader, 2 workers), o `final` dos quatro e o
    `anuncios/roteiro.md`.
  - [V] **A pesquisa funda:** foi feita com a skill `pesquisa`, três trabalhadores e um conferente, e os subagentes
    custaram US$ 2,23. A fonte mais útil são as referências oficiais do HyperFrames, `motion.md` e `sound.md`. Elas
    também estão em `anuncios/hyperframes/node_modules/hyperframes/dist/skills/hyperframes/references/`. O plano da
    terceira volta está no fim de `anuncios/storylines.md`.
- **Medições:**
  - [V] **O `verificar:` em cada par, A2/B2 e A3/B3:**
    - os vídeos têm 1080x1920, 19,967 s e áudio;
    - o A, renderizado duas vezes, dá o mesmo `framemd5` em vídeo e áudio;
    - os gabaritos têm o `marca_em` em 14,367 e 3 s e o sha256 do mp4 ao lado;
    - só a `ordem` difere entre `a.json` e `b.json`;
    - não há mídia no git, e o `git grep -f` do `proibido.txt` não acha nada em revisão nenhuma (o arquivo não foi
      lido);
    - não há amarelo no retângulo da barra antes da marca.
  - [V] **A nota de cena nos cortes:** de 0,199 a 0,381 no A2 e de 0,138 a 0,199 no A3. Fora dos cortes, a maior é
    0,021.
  - [V] **O endereço nos vídeos:** os mp4 em `$VIDEOS` ainda mostram «hack.vesklab.com», porque a troca para
    `vesklab.com` (commit `23f0cb7`) veio depois do render.
- **O que é deste Mac:**
  - [V] **A fila:** ela não executa nem altera arquivo que esta sessão criou, por causa do atributo
    `com.apple.provenance`. O job 53 saiu com «Operation not permitted». O contorno é declarar RAM e CPU com
    `gpu_reserve` e rodar do Bash, um pesado por vez.
  - [V] **O ffmpeg:** o completo, compilado pela C5 (9.0.2, com libass, flite e libx264), está em
    `~/.local/ffmpeg-full/bin` e vai na frente do PATH.
  - [V] **O Chrome do render:** Chrome for Testing 152.0.7977.30, headless shell.
- **O que foi tentado e falhou:**
  - os snapshots pela fila, por causa da proveniência;
  - as fontes com fallback de sistema: com «Times New Roman», o Chrome baixava a EB Garamond, e os fallbacks saíram;
  - o caça-níquel da variante 3 medido em `document.fonts.ready`: saiu vazio, e a rolagem passou a ser em px;
  - o primeiro layout da leitura da história 2: punha as faixas em cima do anúncio.
- **O que não foi feito:**
  - **A segunda opinião em Opus:** a fatia não fechou, e o ponteiro é do orquestrador, como nas sessões anteriores.
  - **O Linear:** não mudou. A VES-102 continua In Progress.
  - **Os plugins:** não foram desinstalados, porque a próxima volta usa os dois. Daqui não há ferramenta para
    desinstalar plugin.
- [V] **A bateria desta sessão, pela trava:** 15 testes, 10 passaram, 0 falharam e 5 foram pulados (os do contrato,
  sem `MOTOR_URL`), em 23 s.

## C5 (16/11/2026, adiantada, no Mac): não fechou — a parte do `E1` está pronta; faltam a variante do `A` e o teste A/B

A Karen está no conserto desde ~14/11. Por decisão do Igor, a C5 abriu antes de a C1v fechar, num worktree próprio
(`c5-variante-ecdf65`) no Mac (macOS arm64), só com a parte que roda com o `E1`. Ela rodou com Opus e esforço `high`
medido pelo Bash [V], como o `dificil` pede, em plan mode, com o plano aprovado pelo Igor. O ponteiro continua no O.

- [V] O `falha antes:` deu vermelho antes do código: `python -m variante --help` → `No module named variante`, sai 1.
- **O ffmpeg do Mac.** O do Homebrew (9.0.2) não tem `flite`, `subtitles` nem `drawtext`. A C5 compilou o mesmo 9.0.2
  do fonte da fórmula do Homebrew (sha256 conferido), ao lado dele, pela fila (job 54, 5 min):
  - [V] `~/.local/ffmpeg-full/bin/ffmpeg -hide_banner -filters` lista `flite`, `ass`, `subtitles` e `drawtext`, e o
    `-encoders` lista o `libx264`;
  - use com `export PATH=$HOME/.local/ffmpeg-full/bin:$PATH`; a sessão `c1v` recebeu o caminho;
  - o `brew install flite libass nasm pkgconf` rodou a limpeza automática do Homebrew (versões velhas e caches).
- **O `proibido.txt` do Mac.** Ele não existia aqui, e o Igor não lembrava do conteúdo. A pedido dele, a C5 escreveu
  `$VIDEOS/proibido.txt` com o que é de terceiros e interno, e mais 6 padrões de chave (Meta, Resend, Modal, Stripe,
  GitHub, chave privada):
  - [V] o `test -s` sai 0, o `git grep` em todas as revisões sai 1, e um clone com uma palavra da lista plantada é pego;
  - o `faster-whisper` ficou de fora, porque a C1v o usa na legenda e ele já está no histórico;
  - falta o Igor pôr o e-mail, o telefone e a palavra proibida (há um rascunho em `$VIDEOS/proibido.rascunho.txt`) e,
    quando a Karen voltar, juntar com o original de lá.
- **O que está feito**, tudo novo:
  - `variante/`: `gerar` troca cada quadro do 1º segundo pelo primeiro quadro com pts ≥ `marca_em`. Os quadros vão em
    cru, no formato de pixel do original, para o x264 sem perda (`-qp 0`), e o áudio é copiado. O `certificado.json`
    traz o original (caminho e sha256), o trecho `[0, 1 s)`, o quadro da marca e o sha256 de cada quadro fora do
    trecho. `conferir` decodifica de novo os dois vídeos e recusa vídeo de taxa variável;
  - `teste/`: `poder` dá o n por braço pelo `h` de Cohen (1988, cap. 6), escrito com `math` e `NormalDist`, e procura o
    menor n inteiro com o poder pedido;
  - `tests/test_variante.py` (os três testes da seção) e `tests/test_poder.py` (5 pares contra o `statsmodels`, e o
    caso sem efeito); o `statsmodels` no `requirements-dev.txt`.
- [V] O `verificar:`, os itens do `E1`, no Mac:
  - um `python -c` fora do pacote conferiu: 450 quadros nos dois, o trecho `[0, 30)` e os 420 de fora idênticos; a
    variante em 0,5 s é igual ao original em 4 s e diferente do original em 0,5 s; 720×1280 e 15,000 s nos dois; o
    `trecho.inicio` é 0;
  - duas gerações deram o mesmo sha256 (`c3037883…`);
  - controles negativos: um quadro mexido (o 333) faz o `conferir` sair 1 apontando o quadro; uma cópia do original
    com o certificado de mudança faz sair 1 com «cópia»;
  - o `teste poder` dá 3762, 3835 e 1565, iguais ao `statsmodels`; com `--p1 0.05 --p2 0.05`, sai 2 com a mensagem.
- **O que falta, em ordem:**
  1. Com o `A` da C1v: `python -m variante gerar --video $VIDEOS/a.mp4 --marca-em <marca_em de $VIDEOS/a.gabarito.json>
     --mudanca marca_no_inicio --saida $VIDEOS/variante-a`, e depois `python -m variante conferir $VIDEOS/variante-a`.
  2. Risco: a variante sai em H.264 sem perda, no perfil High 4:4:4 Predictive. Antes do teste, ver se o Gerenciador
     da Meta aceita o arquivo.
  3. Com a C1 ✅: o Igor monta o teste A/B (o `A` contra a variante, com o teto dele), e a linha
     `- teste A/B no ar desde 2026-11-DD, teto de R$ <N>, variante sha256 <hash>` entra em `docs/anuncios.md`. O
     `python -m teste poder` dá o n por braço do plano.
  4. O resto do `verificar:` (a linha do `docs/anuncios.md` e o `conferir` do `A`), e então o ✅ na fila.
- Os sha256 do `E1` e da variante valem neste Mac, com este ffmpeg; na Karen eles mudam.
- [V] Bateria desta sessão, pela trava, com o ffmpeg de `~/.local/ffmpeg-full` no `PATH`, depois do conserto da
  segunda opinião: 25 testes, 20 passaram, 0 falharam, 5 pulados (os 5 de contrato, sem `MOTOR_URL`), em 70 s; o `-k`
  dos três da seção deu `3 passed` (pela fila, antes do conserto, que não mexeu em `variante/`).
- [V] A segunda opinião (Opus, contexto limpo, diff desde o `1a4fea6`) achou o `sai:` desta sessão entregue e um
  achado de severidade baixa, já consertado (`ed95015`): o `teste poder` caía com traceback ou travava quando `p1` e
  `p2` só diferiam no float (`0.3` contra `0.30000000000000004`). Agora `h` igual a 0 e n acima de 1e9 por braço saem
  2 com «não há efeito a detectar», a busca do n é binária, e o `test_poder_sem_efeito` cobre os três casos.
- Para quando a variante do `A` for gerada: o certificado grava o caminho absoluto do original. Um `conferir` feito
  em outra máquina, com a `$VIDEOS` em outro caminho, diria que o original não existe. Gere e confira na mesma máquina.

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
