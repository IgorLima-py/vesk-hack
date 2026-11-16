# A C1v na Karen: a terceira e a quarta sessão (11 a 13/11/2026)

Saiu do `docs/STATUS.md` em 16/11/2026, na quinta sessão da C1v (no Mac), para o arquivo não passar de 400 linhas.
O que veio depois está no `docs/STATUS.md`.

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

## C1v (12 e 13/11/2026, quarta sessão): não fechou — três histórias feitas nos dois motores; o Igor achou todas com «cara de IA»

Continuação da terceira sessão, na `main` da Karen, depois de um resumo de contexto. O ponteiro continua no O.

- **As decisões do Igor nesta sessão:**
  - [V] **Os cortes:** corte de verdade. No primeiro quadro de cada fala, nada da fala anterior fica na tela. O gabarito
    fica com os 5 cortes, e o `roteiro.md` vai anotar a nota de cena medida em cada um.
  - [V] **O desenho:** ao ver a folha de quadros da prova, achou feio («mt feio»). Pediu pesquisa de direção de arte,
    com referências do PC e da internet, e depois as três histórias feitas até o fim nos dois motores, para escolher
    assistindo.
  - [V] **O veredito, em 13/11:** gostou mais da história 3 (o tipo) e da 2 (a fita), mas disse que todas estão
    «ABSURDAMENTE cara de ia», com «zero gosto de design», sem alma, «nem msm a estetica parecida com a do site», e
    «de design ta mt cru». A locução ficou ok. O som pede um pouco de efeito sonoro melhor, sem exagero.
- **O que foi feito:**
  - [V] `anuncios/storylines.md`: as três linhas de história, pelo método da skill do HyperFrames (Apache-2.0) (`d7ffa9f`).
  - [V] A pesquisa de direção de arte, conferida pela `/pesquisa` (US$ 3,81), está fora do git, na skill global
    `video` (`direcao-de-arte.md` e a seção «Direção de arte» do `SKILL.md`). A conclusão: a doutrina mais útil é a
    da própria skill do HyperFrames, e a `impeccable` só serve para tipografia e cor, porque é de interface web.
  - [V] **Seis versões renderizadas** pela fila, por agentes Opus, em `$VIDEOS/historias/<1|2|3>-<hyperframes|remotion>/`.
    Cada pasta tem `SPEC.md` (só nas do HyperFrames), `stills/folha.png`, `a_mudo.mp4`, o segundo render para o
    determinismo e o `a.mp4` com som e legenda. Só o A foi renderizado; o B só foi conferido em quadros parados.
  - [V] Para assistir, os 10 vídeos estão numa pasta só, `$VIDEOS/TODOS-OS-VIDEOS/`, por link físico (sem ocupar
    espaço a mais): os 6 finais e os 4 esboços da prova.
  - [V] **O `final` rodou de ponta a ponta** (job 1336, e depois um por história): som, legenda queimada e gabarito
    certos, com `marca_em` 14,367 s. Isso fecha o `[?]` da terceira sessão.
- **As medidas, como os agentes relataram** [?] (os vídeos e as folhas foram vistos nesta sessão; os números não
  foram reconferidos):

  | | 1. O seu anúncio | 2. A curva | 3. O tipo |
  |---|---|---|---|
  | nota de cena nos 5 cortes (HyperFrames) | 0,53 / 0,28 / 0,09 / 0,003 / 0,02 | 0,43 / 0,42 / 0,21 / 0,11 / 0,10 | 1,0 / 0,82 / 0,91 / 0,77 / 0,93 |
  | cortes que a prova vê (limiar 0,3) | 1 de 5 | 2 de 5 | 5 de 5 |
  | barra no `marca_em` / no quadro anterior | 1,0 / 0,0 | 1,0 / 0,0 | 0,9997 / 0,0 |
  | dois renders iguais, HyperFrames | sim | sim | sim |
  | dois renders iguais, Remotion | **não** (133 quadros diferentes) | **não** (143 a 499) | sim, byte a byte |
  | Remotion contra HyperFrames | PSNR médio 44,95 dB | 13 de 20 quadros idênticos | 18 de 26 idênticos |
  | render e pico de RAM, HyperFrames | 115 s; 1,4 GiB | 174 a 323 s; 1,35 GiB | 85 a 122 s; 1,4 GiB |
  | render e pico de RAM, Remotion | 133 a 143 s; 1,8 GiB | 106 a 129 s; 1,8 GiB | 191 a 219 s; 1,8 GiB |

  A nota de cena baixa da 1 e da 2 vem da saída do segmento, que mexe a tela antes do corte; nos quadros, nada da fala
  anterior fica na tela.
- **O que foi tentado e falhou:**
  - **O desenho a partir de doutrina escrita.** Cada agente recebeu a linha de história, a skill do HyperFrames e a
    página do hack como marca, e não o vesklab.com. Saíram campos inteiros de amarelo e de claro, que o site não usa,
    e garrafa e cartões desenhados em código, com linhas cinzas no lugar de texto, com cara de rascunho. [V] O
    vesklab.com foi aberto nesta sessão, e a diferença está no passo 3 do «Próximo passo imediato».
  - **O determinismo no Remotion 4.0.542**, nas histórias 1 e 2. Os agentes tentaram e não zeraram a diferença:
    - grão em canvas;
    - transform sempre 2D;
    - véu no lugar da `mask-image`;
    - trocar o GL;
    - `disableSharedMemoryCapture`;
    - `--disable-gpu-rasterization`, ligado por uma variável interna reservada do Remotion.

    A causa provável, não provada: o Remotion não deixa passar ao Chrome as flags de determinismo que o HyperFrames
    usa. O mesmo quadro desenhado sozinho sai igual nas duas vezes.
  - Os agentes quebraram regras da casa, e cada um disse no relatório:
    - alguns comandos começaram com `cd`;
    - um agente rodou o `hyperframes check` uma vez fora da fila, com o Chrome mudo.
  - O commit `11038c8` citava o nome da pasta do app privado; o Igor o refez como `d7ffa9f` antes do push, porque o
    guarda do playbook barra o `--amend` da sessão. [V] O `git log -p origin/main..HEAD` não tem mais o nome.
- [V] No Linear, a VES-102 continua In Progress.
- [V] Bateria desta sessão, pela trava: 13 testes, 8 passaram, 0 falharam, 5 pulados (os 5 de contrato, sem
  `MOTOR_URL`), em 40 s.
- Sem segunda opinião em Opus: a fatia não fechou (falta o desenho aprovado, o A e o B e o `verificar:`), e o ponteiro
  é do orquestrador.
- A sessão passou de ~320k de contexto antes do resumo e voltou a ~190k.
