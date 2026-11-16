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

- **Marca:** o selo de três pontos, «Vesk» em Newsreader 500, a barra do grifo e «The creative autopilot.». Tudo está
  inteiro no primeiro quadro. Só a faixa de pontos do rodapé do site se mexe atrás.
- **Chamada:** «hack.vesklab.com» em IBM Plex Mono, sublinhado no grifo em «Upload», sobre a faixa de pontos.

## O texto na tela muda o gabarito

As duas histórias escrevem na tela mais do que o `tela` de `anuncios/falas.py` declara hoje. São rótulos, linhas da
leitura e palavras gigantes. Na história escolhida, o `tela` de cada fala passa a listar tudo o que o motor escreve.
Na frase que já começa em cinza, o texto vale desde o começo da fala. A voz, os cortes e o `marca_em` não mudam.

## A escolha

Ainda não feita: decisão do Igor, pelo storyboard.
