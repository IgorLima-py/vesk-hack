# As duas linhas de história dos anúncios A e B, no visual do vesklab.com

Em 13/11/2026, o Igor viu as três histórias da quarta sessão renderizadas e preferiu a 3 (o tipo) e a 2 (a curva).
Achou todas com «cara de IA» e sem a estética do site. A versão anterior deste arquivo está no git (`d7ffa9f`).
Em 16/11, no Mac, as duas foram redesenhadas a partir do vesklab.com, e cada uma virou um storyboard de quadros
parados. Ele aprova antes de qualquer render inteiro. As folhas estão fora do git, em
`$VIDEOS/historias/storyboard-historia-2.png` e `-3.png`.

## O visual, medido no site

Os quadros do vesklab.com estão em `$VIDEOS/referencias/`: a página inteira no desktop, o topo no celular e o DOM.
Eles foram tirados com o Chrome mudo e sem cabeça. As cores do tema escuro saíram do DOM; a paleta dos pontos saiu dos
quadros, como a mediana do quartil mais claro de cada faixa de matiz.

- **O campo de pontos:** é o fundo do site. Pontos redondos numa grade, apagados em `#18181d`, que acendem em
  `#5762fe`, `#7c4aff`, `#b53de8`, `#f43ca7`, `#ff516e`, `#ff7c44` e `#ffb84a`. No vídeo, a grade tem passo de 24 px;
  no site, ela tem cerca de 12 px a 1440 de largura.
- **O tipo:**
  - Newsreader 300 grande, com o espaço entre letras apertado, como os títulos do site;
  - Schibsted Grotesk no apoio;
  - IBM Plex Mono em caixa-alta para os rótulos pequenos («ORIGINAL», «VARIANT») e no endereço.
- **O grifo:** `#ffe14a` só como marca-texto atrás de uma palavra ou de uma linha, e a letra escurece junto. O campo
  inteiro amarelo saiu, porque o site não o usa.
- **O selo:** os três pontos do logo do site, na cartela, na chamada e em cada linha da leitura.
- **A tela do produto:** um cartão escuro com borda fina e um anúncio lido em mosaico, numa janela de barra clara
  listrada, como as do topo do site. Ao lado, a leitura em linhas e as faixas do que estava na tela, com as cores das
  faixas do site (`#8fa8ff`, `#ffe14a` e `#ff8a5b`) e o cabeçote branco.
- **O anúncio fictício:** o cartaz de um sérum de uma marca sem nome, com frasco âmbar, sol e pedestal. Ele é
  desenhado em código e mostrado em mosaico pontilhado, sem foto e sem pessoa. O clipe do topo do site é do Pexels e
  fica de fora.

## O que as duas respeitam

Isto já estava decidido e não mudou:
- as seis falas, a voz e o tempo de cada uma (`anuncios/linha_do_tempo/`);
- A e B diferem só na `ordem`;
- corte de verdade no primeiro quadro de cada fala;
- a cartela inteira no `marca_em`, com a barra no retângulo de sempre;
- nada em `#ffe14a` dentro desse retângulo antes da cartela, em nenhuma fala;
- nenhum número na tela;
- o texto dentro da zona segura do Reels;
- a faixa da legenda (y de 1088 a 1248) sem texto do motor e com o campo de pontos apagado embaixo dela.

A marca e a chamada são as mesmas cenas nas duas histórias.

## 2. A curva é feita de gente

**A ideia:** cada ponto aceso é uma pessoa assistindo. O campo de pontos do site vira a área sob a curva de permanência.
No penhasco dos primeiros segundos, os pontos se apagam um a um enquanto a voz fala.

- **Gancho:** no quadro 0, a frase já está na tela em cinza, e a massa de pontos já cai. Cada palavra vira tinta no
  quadro em que é dita, «first seconds.» ganha o grifo, e o penhasco se aprofunda.
- **Problema:** de perto, no penhasco, com pontos grandes. Um anel marca o beiral em «when», e um «?» enorme ocupa o
  vazio de quem saiu em «Not».
- **Leitura:** a tela do produto. O cabeçote corre o anúncio de «read» até «and»; em «match» ele volta ao penhasco, e
  em «drop» a linha «Logo only, no product» é grifada.
- **Variante:** o anúncio e a cópia dele lado a lado, iguais. Em «one», só a cópia muda: o frasco entra na abertura,
  contornado no grifo, com a etiqueta «One change».
- **Marca e chamada:** as comuns, abaixo.
- **O risco:** a tela do produto tem muito texto pequeno para 5 s, e a leitura depende da legenda.

## 3. O tipo carrega o argumento

**A ideia:** uma ou duas palavras enormes por fala, em Newsreader fina, com o grifo numa palavra só e o campo de pontos
atrás como atmosfera. Não há desenho de produto.

- **Gancho:** «losing people» enorme. No quadro 0, a frase toda está em cinza sobre a mancha de pontos. As palavras
  viram tinta quando são ditas, e a mancha se apaga ponto a ponto.
- **Problema:** «You can see when they leave.» chega palavra a palavra. Em «Not», ela sai num borrão, e «Not why.» ocupa
  a largura, com «why.» grifado.
- **Leitura:** um rolo de «second» corre pelo cabeçote, um por segundo do anúncio. Em «match» ele freia, e em «drop» o
  segundo parado no cabeçote é grifado.
- **Variante:** original e variante iguais, «Logo first.». Em «one», a linha da variante roda como caça-níquel e para em
  «Bottle first.», com «Bottle» grifado; a original ganha um risco.
- **O risco:** sem a tela do produto, o anúncio não mostra o que a Vesk entrega, só diz.

## A marca e a chamada (comuns)

- **Marca:** o selo ∵ do site, grande e em cor: os três pontos cheios com o degradê da paleta do campo, do azul ao
  âmbar. Embaixo, «Vesk» em Newsreader 500, a barra do grifo no retângulo de sempre e «The creative autopilot for video
  ads.». Tudo está inteiro no primeiro quadro; só a faixa de pontos de trás se mexe.
- **Chamada:** o anúncio no feed à esquerda e o relatório vazio à direita. Em «Upload», pontos da paleta correm de um
  para o outro; em «report», a leitura e o próximo teste aparecem no lugar do esqueleto. Embaixo, «vesklab.com» (era «hack.vesklab.com» até 16/11)
  em IBM Plex Mono, sublinhado no grifo em «Upload».

## A segunda volta (16/11)

O Igor viu o primeiro storyboard e achou «anos-luz melhor», com três notas: o logo ainda está ruim, falta cor, e o
anúncio precisa dar a entender que é sobre anúncio, na língua de quem compra para empresa (B2B). As folhas novas estão
em `$VIDEOS/historias/storyboard-historia-2-v2.png` e `-3-v2.png`.

- **O logo:** o selo de três pontos, que era pequeno e branco em cima do nome, virou a marca: grande e com a paleta.
- **A cor:** as cenas ganharam manchas da paleta em volta do texto e dos cartões (`VeskKit.aura`), apagadas embaixo
  do texto e na faixa da legenda.
- **É sobre anúncio:** o anúncio fictício aparece como anúncio, no cartão de um vídeo patrocinado genérico
  (`VeskKit.Anuncio`): barra de progresso, perfil «yourbrand», «Sponsored» e «Shop now», sem a marca de plataforma
  nenhuma. Na história 2, ele está no gancho, ao lado de quem o assiste, e na variante. Nas duas histórias, ele está na
  chamada, virando relatório.
- **A língua B2B:** na tela, as palavras do ofício de quem compra mídia: control e variant (os nomes do teste A/B),
  drop-off, readout e next test, além de «for video ads» na assinatura. A voz não mudou: ela já fala do resultado
  (a saída das pessoas, a variante com uma mudança, o teste), e mudar a fala refaz a voz, o tempo e o gabarito.
- **O que a história 3 não resolve:** ela continua sem o anúncio na tela até a chamada, porque o desenho dela são as
  palavras enormes. A história 2 mostra o anúncio desde o primeiro quadro.

## O texto na tela muda o gabarito

As duas histórias escrevem na tela mais do que o `tela` de `anuncios/falas.py` declara hoje. São rótulos, linhas da
leitura e palavras gigantes. Na história escolhida, o `tela` de cada fala passa a listar tudo o que o motor escreve.
Na frase que já começa em cinza, o texto vale desde o começo da fala. A voz, os cortes e o `marca_em` não mudam.

## A escolha

Em 16/11, depois da segunda volta, o Igor escolheu as duas: «faz os dois, gostei dos dois». Cada história sai em A e
em B, e A e B continuam diferindo só na `ordem`. São quatro vídeos: A2, B2, A3 e B3. A voz, os cortes e o `marca_em`
são os mesmos nos quatro.

O que isso muda no código, antes da Fase 3:
- **O texto na tela por história:** o `tela` de `anuncios/falas.py` passa a ter uma lista por história. A marca e a
  chamada são as mesmas nas duas.
- **A linha do tempo por história:** `python -m anuncios tempo` gera uma linha do tempo para cada par de anúncio e
  história, e o gabarito de cada vídeo vem da dele.
- **O `cenas` e o `final` recebem `--historia`,** e os vídeos saem com a história no nome.
- **O `roteiro.md` e o `verificar:`** cobrem os quatro vídeos. Os dois renders iguais (o mesmo framemd5) valem para
  o A de cada história.

Fica em aberto, para o Igor: o teste A/B da ordem roda com uma história ou com as duas.

## Depois dos quatro vídeos (16/11)

O Igor assistiu A2, B2, A3 e B3. A história 2 está melhor, mas ainda pede outra volta:
- **O endereço:** «hack.vesklab.com» não é amigável, e ele mesmo não entraria num site com esse nome.
- **O logo sonoro:** o som da Vesk na cartela está ruim.
- **A cara de IA:** os vídeos ainda parecem feitos por IA.
- **O movimento e a cor:** falta movimento, falta ser mais dinâmico, e ainda cabe mais cor.

Ele pediu skills e plugins que ajudem. No catálogo do claude.ai, os que servem são:
- o **Motion Reel**: vídeo de movimento feito por código, com grade de batida, lista de planos aprovada, trilha e
  efeitos sintetizados, crítica em folha de quadros e entrega em 9:16 a -14 LUFS;
- o **Design**: crítica de design.

A busca de skills não achou nada de movimento nem de som.

## O plano da terceira volta (16/11, depois da pesquisa)

A pesquisa (skill `pesquisa`, modo fundo, conferida) achou a fonte mais útil no próprio motor: as referências
oficiais do HyperFrames, `skills/hyperframes/references/motion.md` e `sound.md`. Elas estão também no
`node_modules/hyperframes/dist/skills/` da 0.9.33. A volta segue nesta ordem:
- **Movimento:**
  - a câmera nunca para: aproximação lenta em escala logarítmica em cada cena e profundidade em três planos;
  - as entradas têm direção e peso (molas, uma curva por papel), e não «tudo entra com fade»;
  - algo novo acontece a cada 2 a 4 s;
  - o corte continua de verdade, como o Igor decidiu.
- **Cor:** fundos e cartões com a paleta, sem cenas quase pretas.
- **Som:**
  - o logo sonoro é novo: três notas de sino em FM, uma para cada ponto do selo, com 2 a 3 s;
  - uma trilha discreta, sintetizada com o `dsp.py` do Motion Reel (MIT, origem anotada), de 18 a 24 dB abaixo da
    voz;
  - dois ou três takes do sopro, alternados, com o pico um quadro depois da imagem;
  - a mistura vai a cerca de -14 LUFS e -1 dBTP.
- **Crítica antes de mostrar:** três rodadas na folha de quadros, com o prompt de crítica do Motion Reel e a skill de
  crítica do Design, até nota 8 em gancho, leitura no celular, movimento, variedade, marca e sincronia do som.
- **O endereço:** `vesklab.com`, já trocado.
