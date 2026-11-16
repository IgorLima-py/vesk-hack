# O roteiro dos anúncios A e B

Os dois anúncios da Vesk, montados por código: seis falas em inglês na voz do Kokoro, as cenas no HyperFrames, e a
legenda, o som e o gabarito no Python. Em 16/11/2026, o Igor escolheu as duas linhas de história de
`anuncios/storylines.md`, a 2 (a curva é feita de gente) e a 3 (o tipo carrega o argumento). São quatro vídeos: A2,
B2, A3 e B3, em `$VIDEOS/<a|b><história>.mp4`, cada um com o gabarito ao lado.

- A e B diferem em: ordem

A voz, os cortes e o `marca_em` são os mesmos nas duas histórias. No A, a marca entra em 14,367 s; no B, em 3,000 s.

## Segundo a segundo

O A, com 599 quadros a 30 fps (19,967 s):

| tempo | fala | história 2 | história 3 |
|---|---|---|---|
| 0,000 a 3,000 s | «Your ad is losing people in the first seconds.» | o anúncio no feed (só o logo na abertura) e quem o assiste, um ponto por pessoa; os pontos do penhasco se apagam | «losing people» enorme sobre a mancha de pontos, que se apaga |
| 3,000 a 5,700 s | «You can see when they leave. Not why.» | de perto, no penhasco: «Drop-off» em «when» e o «?» em «Not» | a frase palavra a palavra; «Not why.» em «Not» |
| 5,700 a 10,867 s | «We read your video, second by second, and match it to the moment people drop off.» | a tela do produto: o mosaico, a leitura, a curva e as faixas; o cabeçote volta ao penhasco em «match» | o rolo de «second» freia em «match»; «Drop-off» em «drop» |
| 10,867 a 14,367 s | «Then you get a variant with one change, ready to test.» | control e variant no feed; o frasco entra na variante em «one» | «Logo first.» vira «Bottle first.» em «one» |
| 14,367 a 17,500 s | «Vesk. The creative autopilot.» | a cartela: o selo de três pontos, «Vesk», a barra e «The creative autopilot for video ads.» | a mesma |
| 17,500 a 19,967 s | «Upload your ad. Get the report.» | o anúncio vira relatório; «vesklab.com» | a mesma |

O B tem as mesmas cenas na ordem gancho, marca, problema, leitura, variante e chamada: a marca entra em 3,000 s, logo
depois do gancho, e cada fala seguinte começa 3,133 s mais tarde do que no A, até a chamada, que fica no mesmo lugar.

## Os comandos

Na raiz do repositório, com `$VIDEOS` apontando para a pasta dos vídeos, fora do git, e um `ffmpeg` com `libass` na
frente do `PATH` (o filtro `subtitles` queima a legenda). O `npm ci` instala o HyperFrames 0.9.33 e o GSAP 3.15.0 do
`package-lock.json`, que fixa a versão exata.

A voz, uma vez (o `--conferir` gera de novo e compara o sha256):

```bash
uv run --no-project --python 3.11 --with-requirements anuncios/requisitos-voz.txt python -X utf8 -m anuncios voz
```

Um anúncio (aqui, o A da história 2):

```bash
(cd anuncios/hyperframes && npm ci)
python -m anuncios cenas a --historia 2
(cd anuncios/hyperframes && HYPERFRAMES_BROWSER_PATH=$PWD/mudo/chrome-headless-shell npx hyperframes render --no-browser-gpu --fps 30 --quality delivery --workers 2 -o "$VIDEOS/montagem/a/imagem-h2.mp4")
python -m anuncios som a
python -m anuncios final a --historia 2 --imagem "$VIDEOS/montagem/a/imagem-h2.mp4"
```

O `--no-browser-gpu` faz o Chrome desenhar no SwiftShader, sem a placa de vídeo: o mesmo quadro sai igual toda vez.

## O navegador mudo

O HyperFrames abre o Chrome que `HYPERFRAMES_BROWSER_PATH` aponta. Ele aponta para `anuncios/hyperframes/mudo/
chrome-headless-shell`, um script que chama o Chrome sem cabeça baixado pelo próprio HyperFrames com todos os
argumentos dele e mais `--mute-audio`. O render e o `snapshot` usam o mesmo script, e as cenas não têm áudio.

## Os brutos

O sha256 de cada fala em `$VIDEOS/brutos/`, gerada no Mac em 16/11/2026 (torch 2.15.0, Python 3.11.17, semente
20261111, 2 fios). Os da Karen eram outros bits com as mesmas amostras e as mesmas pontas da fala: a linha do tempo não
mudou.

- gancho: `6c99723a1f2fe42235bb2ebd66fe5d92d022ce01a10c4a7aff38587e75d29fd3`
- problema: `1fddd7da31b3da3c503a38cf827d9731892e015df277d70d9a86494b68fe2990`
- leitura: `e3b9264e218ca56b86127a0c374e3d817197572eabf4a5af9d394d9fac98cdd9`
- variante: `60c80c2e79309642ab42ac802fdd285e6eaa32a1323aed243168cfc3aabee5fb`
- marca: `c2fdad471a95d7980e7b753d54d422ec1e7c45022cf51e4216014dea42660b71`
- chamada: `0df2cbb14428097ca0e2e5afe42a10e5dc4104db19529b97f293b7de998c2f13`

## O som

A voz no quadro de cada fala, o logo sonoro na cartela (duas notas do `aevalsrc` do `ffmpeg`) e dois efeitos discretos
da biblioteca que vem com o HyperFrames 0.9.33, do Pixabay, sob a Pixabay Content License
(https://pixabay.com/service/license-summary/), que permite uso comercial sem atribuição:
- `whoosh-short`, 0,12 s antes de cada corte, menos o da cartela, a 18 dB abaixo do pico da fala;
- `click-soft` em «one» e em «Upload», a 14 dB abaixo.

O mp3 não entra no git: `anuncios/som.py` lê o arquivo do `node_modules` e confere o sha256.

## A nota de cena em cada corte

O corte é de verdade: no primeiro quadro de cada fala, nada da fala anterior fica na tela. A nota de cena é a do
`ffmpeg` (`select='gte(scene,0)',metadata=print`), medida nos mp4 finais de 16/11/2026, no quadro de cada corte, com a
maior nota fora dos cortes ao lado.

| vídeo | cortes (quadro: nota) | maior fora dos cortes |
|---|---|---|
| A2 | 90: 0,312 · 171: 0,297 · 326: 0,332 · 431: 0,381 · 525: 0,199 | 0,021 |
| B2 | 90: 0,276 · 184: 0,247 · 265: 0,297 · 420: 0,332 · 525: 0,342 | 0,021 |
| A3 | 90: 0,184 · 171: 0,138 · 326: 0,172 · 431: 0,145 · 525: 0,199 | 0,018 |
| B3 | 90: 0,229 · 184: 0,108 · 265: 0,138 · 420: 0,172 · 525: 0,194 | 0,018 |

Na história 3, as notas são menores porque as cenas são quase só fundo preto com tipo; ainda assim, cada corte fica
pelo menos 5 vezes acima do maior movimento dentro de uma cena.
