# Exemplos com gabarito

Vídeos sintéticos cuja resposta se conhece por construção. Eles servem para medir o motor (C7) e para a variante
(C5) ter uma entrada que qualquer sessão gera igual.

```bash
python -m exemplos.sintetico --marca-em 4 --semente 1 --saida <pasta>/e1.mp4   # o E1
python -m exemplos.suite --saida <pasta>                                         # os 24 da C7
```

## O que tem no vídeo

- 720×1280, a 30 fps, com 15 s por padrão (`--duracao`).
- **Cortes:** planos de cor lisa que alternam um plano escuro e um claro. A semente sorteia trechos de 1,5 a 3,5 s,
  e o último plano tem pelo menos 1 s.
- **Texto na tela:** «VESK» em magenta puro (`[255, 0, 255]`), do segundo da marca até o fim. A fonte é a que vem
  embutida no Pillow (`ImageFont.load_default(size=160)`), então o texto sai igual em qualquer máquina, sem
  depender de fonte do sistema.
- **Voz:** a frase «Vesk. The creative autopilot.» começa exatamente no segundo da marca. Quando cabe, a frase «Watch
  this.», que não tem a marca, vem antes, em 0,5 s. Com `--sem-fala` o áudio fica em silêncio; com `--sem-marca`,
  saem o texto e a frase da marca.

## O gabarito

O `gabarito.json` fica na pasta do mp4, com estes campos:
- `marca_em`: `null` sem marca;
- `cortes`: os segundos de cada troca de plano;
- `fala`: a lista de frases, cada uma com `texto`, `inicio`, `fim` e `tem_marca`;
- `texto`: o que aparece na tela, com início e fim;
- `cor_do_texto`;
- `duracao`, `fps`, `largura`, `altura`, `semente` e `video_sha256`.

O início e o fim de cada frase são medidos na própria faixa de áudio, onde a amplitude passa de 500 em int16 (cerca de
-36 dBFS).

A mesma semente dá o mesmo arquivo, byte a byte, na mesma máquina e na mesma versão do `ffmpeg`: o x264 e o AAC rodam
com `+bitexact` e sem metadados.

## De onde vem a voz

A voz vem do filtro `flite` do `ffmpeg` (https://ffmpeg.org/ffmpeg-filters.html#flite), com a voz `kal16`. Ele usa o
Flite, o sintetizador de fala da Carnegie Mellon, e roda sem rede.
- **Windows:** o build «full» do gyan.dev (https://www.gyan.dev/ffmpeg/builds/) traz o filtro, compilado com
  `--enable-libflite`. O build «essentials» não traz.
- **Linux e CI:** o pacote `ffmpeg` do Ubuntu 24.04 serve. O `libavfilter9` dele depende de `libflite1`
  (https://packages.ubuntu.com/noble/libavfilter9).

Sem o `ffmpeg`, ou com um `ffmpeg` sem o `flite`, o gerador sai com código 2 e diz o que falta.
