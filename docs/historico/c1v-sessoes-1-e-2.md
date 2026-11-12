# A C1v antes do código: a pesquisa dos vídeos e as duas primeiras sessões (11/11/2026)

Saiu do `docs/STATUS.md` em 11/11/2026, na terceira sessão da C1v, quando o arquivo ia passar de 400 linhas.
Aqui ficam o roteiro e o plano aprovado; o que veio depois está no `docs/STATUS.md`.

## Pesquisa dos vídeos e a C1v (11/11/2026)

Sessão de pesquisa aberta pelo orquestrador (perfil `replan`), na `main` da Karen, sem worktree. Não é fatia, e o
ponteiro não andou: ele é do orquestrador.
- [V] O mapa dos jeitos de fazer um anúncio em vídeo está na skill global `video`
  (`~/.claude/skills/video/SKILL.md`), fora de qualquer git, como o Igor escolheu. Ele cobre gravado de verdade, tela,
  vídeo por código, IA generativa, avatar, banco de imagens, voz e legenda, com a fonte de cada linha.
- [V] A recomendação para A e B é o híbrido montado por código: rosto e voz do Igor no celular, e por cima texto,
  marca e legenda compostos no Remotion, com o gabarito ao lado de cada mp4.
- [V] O Igor aprovou a fatia nova, e o commit `ee92833` mudou o `docs/ROADMAP.md`:
  - a C1v entrou na fila, com a seção própria;
  - a C1 passa a depender dela, e o verificar da C1 ganhou a marca à mão contra o gabarito, com ±1 s;
  - a C5 espera o vídeo `A` da C1v;
  - a C13 ganha a skill na entrada;
  - o bloco 5 ganhou uma linha.
- [V] No Linear: a VES-102 é o espelho da C1v (Todo), e a VES-76 (C1) e a VES-82 (C5) têm o «Depende de» novo.
- [V] Um conferente Opus releu na fonte as três afirmações que decidem:
  - a página do rótulo de IA da Meta fala de **imagem**: a feita com IA de terceiros não leva o rótulo, e de vídeo a
    página não diz nada;
  - o regulamento: a 6.4 permite IA, e a 6.2 trata só de código;
  - o Remotion é grátis para empresa de até 3 pessoas, inclusive para uso comercial.
- [V] Fora do ar desde 2026: a API do Sora 2 (24/09) e o Veo 3.1 Preview da Gemini API (22/10).
- Não achei semente para refazer o mesmo vídeo por IA, nem estudo revisado por pares de anúncio em vídeo feito por IA
  contra feito por gente.
- O relatório completo e a proposta estão na pasta de notas das sessões: `video-pesquisa-relatorio.md` e
  `video-proposta-da-fila.md`.
- [?] Esforço: o Igor disse que subiu a sessão para xhigh; não foi conferido por comando.
- **Pendências:**
  - o idioma e o público do anúncio. A fala em `vesk-hack-videos/voz/fala.txt` é em português, e o `CLAUDE.md`
    limita a prospecção ativa a empresa dos EUA. O Igor decide no plano da C1v;
  - mover a skill `video` para `playbook/.claude/skills`, com link, como as outras skills globais;
  - o vídeo de demo da C13 (gravação de tela com áudio) ficou fora da pesquisa.
- Bateria: não rodou, porque esta sessão não mexeu em código, só em `docs/`.

## C1v (11/11/2026): não fechou — o plano está aprovado e ainda não há código

A sessão rodou na `main` da Karen, sem worktree, aberta com `/oi c1v`, com Opus e esforço `xhigh` medido pelo Bash,
como o perfil `criativo` pede [V]. O ponteiro continua no O. O que entrou:
- [V] O `falha antes:` deu vermelho: `ls anuncios/` sai 2, e `ls $VIDEOS/*.mp4` também sai 2.
- [V] As decisões do Igor estão no bloco 5 e na seção C1v do `docs/ROADMAP.md` (`e7dbc89`):
  - sem rosto nem voz dele, nem de pessoa real;
  - inglês, para o público dos EUA;
  - a marca é o wordmark do visual do site;
  - A e B diferem só na posição da cartela da marca: perto de 14 s no A e perto de 3 s no B, numa chave só, `ordem`;
  - a imagem é motion por código;
  - a voz é o Kokoro `af_heart`, com um logo sonoro gerado no `ffmpeg` e sem trilha;
  - o motor sai de uma prova entre Remotion, HyperFrames e Revideo, e o Igor escolhe.
- **O plano aprovado.** O arquivo mora só na Karen (`~/.claude/plans/tender-wiggling-biscuit.md`), então o essencial
  está aqui:
  - **Roteiro**, com as chaves `gancho`, `problema`, `leitura`, `variante`, `marca` e `chamada`:
    - «Your ad is losing people in the first seconds.»
    - «You can see when they leave. Not why.»
    - «We read your video, second by second, and match it to the moment people drop off.»
    - «Then you get a variant with one change, ready to test.»
    - «Vesk. The creative autopilot.» (a cartela com o wordmark e o logo sonoro no primeiro quadro)
    - «Upload your ad. Get the report.» (a cartela final com `hack.vesklab.com`)

    O A segue 1 2 3 4 5 6, e o B segue 1 5 2 3 4 6. A marca é dita uma vez só, e o primeiro quadro da cartela é o
    `marca_em`. Na tela, sem número nenhum: a frase, uma curva desenhada caindo, o ponto de queda com «?», uma tira de
    quadros, e dois quadros lado a lado com um elemento trocado no grifo. O texto passa pelo `grep` do `$PROIBIDO`
    antes de virar voz.
  - **Fase 1** (Python, `python -m anuncios`):
    - `voz` usa o Kokoro e grava em `$VIDEOS/brutos/`, com o sha256 em `anuncios/brutos.json`;
    - `transcrever` usa o faster-whisper e grava em `anuncios/fala/<chave>.json`, com a grafia do roteiro e o tempo
      do whisper. Se faltar ou sobrar palavra, o comando para;
    - `tempo <a|b>` grava a `linha_do_tempo.json`, que é a única entrada dos motores;
    - `som <a|b>` monta o áudio pelo `ffmpeg`, com cada voz no seu quadro e o logo sonoro por `aevalsrc`. O pico é
      normalizado, sem `loudnorm`;
    - `final <a|b> --imagem <mp4 mudo>` queima o `.ass` com o filtro `subtitles` e usa as flags `bitexact` do
      `exemplos/sintetico.py`. Grava o `$VIDEOS/<a|b>.mp4` e o gabarito, nas chaves da C3, com as legendas dentro
      de `texto`.

    Testes: `test_alinhar_fala_usa_grafia_do_roteiro` e `test_marca_em_e_cortes_saem_da_ordem`.
  - **Fase 2, a prova dos motores.** São três subagentes em paralelo: Remotion 4.0.542, HyperFrames e Revideo. Cada
    um desenha, em `$VIDEOS/provas/<motor>/`, fora do git, a imagem muda do A a partir da mesma linha do tempo, em
    1080x1920 e 30 fps. `python -m anuncios prova <motor>` mede seis coisas:
    - se dois renders dão o mesmo `framemd5`;
    - se a cartela cai no quadro do `marca_em`;
    - o tempo e o pico de RAM;
    - as linhas de código;
    - a licença;
    - o que travou.

    Os renders vão pela fila da Karen (`gpu_submit`). O Igor escolhe o vencedor, e a tabela vai para a skill
    `video`.
  - **Fase 3, o vencedor.** Ele vai para `anuncios/<motor>/`, com o lock exato e as fontes de pacote local.
    - `a.json` e `b.json` diferem só na `ordem`.
    - `anuncios/roteiro.md` cumpre o `sai:`. O `--mute-audio` do Remotion está na lista de argumentos de
      `packages/renderer/src/open-browser.ts`, conferido em 11/11.
    - `*.m4a` e `*.mp3` entram no `.gitignore`, porque hoje faltam e o `verificar:` os conta.
- [V] A pesquisa teve duas levas de trabalhadores Sonnet e um conferente Opus. O conferente achou o literal de seis
  afirmações:
  - o Kokoro é Apache-2.0, e a `af_heart` tem nota «A»;
  - o Chatterbox foi aposentado em 08/2026 e põe marca d'água;
  - Meta e Toluna: marca e mensagem nos primeiros 5 s deram 1,7 vez mais intenção de compra forte;
  - o HyperFrames é Apache-2.0 e «Deterministic: same input, same frames, same output»;
  - a Sound Collection libera anúncio;
  - «Over 75% of Reels views on Instagram are sound on».

  Tudo isso, com a URL de cada linha, está na skill global `video` (`~/.claude/skills/video/SKILL.md`), **fora do git
  e só na Karen**.
- Não rodaram o `medir.ps1` nem o `conferir.ps1` da `/pesquisa`, porque o plan mode só deixa gravar o arquivo do
  plano. O custo das duas levas não foi medido.
- [V] O que existe na Karen:
  - Node v24.13.0 e npm 11.6.2;
  - ffmpeg 9.0.1 full, com `flite`, `subtitles` e `ass`;
  - Python 3.14.3, com faster-whisper 1.2.1 e torch 2.10, só CPU.

  O que **não** está instalado: `kokoro` e `chatterbox`. Se o `kokoro` não instalar no 3.14, use um venv de outra
  versão e anote no roteiro.
- [V] A máquina estava cheia: de 3 a 4 GiB de RAM livre, e de 4 a 5 tarefas esperando na fila do workerq.
- Há três worktrees velhos, em HEAD solto: `c1-anuncios-8fcf4c` e `c2-vitrine-3b0944`, em `67b67e4`, e
  `c3-exemplos-contrato-c9b4ec`, em `b789318`. O da C1 é de antes da C1v.
- A seção C1v pede plan mode. A próxima sessão entra nele, lê este plano e sai com ele, sem replanejar.
- No Linear, a VES-102 foi para In Progress.
- Bateria: não rodou, porque esta sessão só mexeu em `docs/` e não em código.

## C1v (11/11/2026, segunda sessão): não fechou — a /pesquisa completa e os quatro motores; ainda sem código

A sessão rodou na `main` da Karen, aberta com `/oi c1v`, com Opus e esforço `xhigh` medido pelo Bash [V]. O ponteiro
continua no O.
- [V] O `falha antes:` deu vermelho de novo: `ls anuncios/` sai 2, e `ls $VIDEOS/*.mp4` também.
- [V] O Igor perguntou se o plano tinha usado a `/pesquisa`. Tinha usado só em parte: sem o `medir.ps1`, sem o
  `conferir.ps1`, com duas levas e sem registro da varredura do GitHub, porque o plan mode só deixa gravar o arquivo
  do plano. Ele pediu para completar a pesquisa, e o plano novo pôs a pesquisa como Fase 0, fora do plan mode
  (`~/.claude/plans/hidden-stirring-twilight.md`, só na Karen, aprovado). O resto do plano de 11/11 não mudou.
- [V] A `/pesquisa` rodou inteira:
  - uma leva de 3 trabalhadores Sonnet (família do navegador, família sem navegador, quem já comparou) e um
    conferente Opus sobre as afirmações que decidem;
  - o `conferir.ps1` saiu 0, e o `medir.ps1` (`20261111-134346-00c0`) deu US$ 5,04 nesta sessão;
  - o relatório foi entregue na conversa e apagado do `%TEMP%`. Os achados estão na skill `video`, na tabela «Motores
    de vídeo por código» e nas ressalvas logo abaixo dela (fora do git, só na Karen).
- [V] A decisão do Igor: **quatro frentes na prova, Remotion, HyperFrames, Revideo e FrameFields**, no bloco 5 e na
  seção C1v do `docs/ROADMAP.md` (`1109c7d`).
- O que a prova precisa levar em conta (conferido no literal pelo conferente):
  - **Remotion 4.0.542:** a correção dos quadros diferentes no Windows (PR #12939) saiu na 4.0.541 e está dentro da
    4.0.542, mas a PR diz «Windows runtime verification is still needed». Renderize com `--concurrency=1`.
  - **HyperFrames:** renderize com 1 worker, porque 1 e 3 workers dão quadros diferentes (#7111, aberta). No Windows, o
    `spawn EBUSY` transitório do ffmpeg derruba o render (#4058, aberta).
  - **Revideo:** o `npm run render` do exemplo padrão falha no Windows 10 com «Output file #0 does not contain any
    stream» (#348, aberta). A prova mede se ele renderiza na Karen.
  - **FrameFields:** sem navegador, WebGPU com Dawn, D3D12 no Windows, Apache-2.0, cena em TypeScript. O README diz
    «Deterministic & Frame-Accurate» e não diz que alguém testou o Windows. Usa a GPU: vai pelo `gpu_submit` com
    `vram_gb`.
- [V] A zona segura do Reels, no literal da Meta: «Deixe pelo menos 14% da parte superior, 35% da parte inferior e 6%
  de cada lado do seu ativo sem texto, logotipos ou outros elementos criativos importantes.»
  (https://web.facebook.com/business/ads-guide/update/video/instagram-reels). Em 1080x1920 são 269 px em cima, 672
  embaixo e 65 dos lados (conta: 1920 × 0,14; 1920 × 0,35; 1080 × 0,06). A legenda fica logo acima dos 672 px de
  baixo, e os motores desenham dentro da zona.
- O que esta sessão levantou para a Fase 1, ainda sem código:
  - [V] No Python 3.14, o pip só acha o `kokoro` até a 0.7.16 (`pip index versions kokoro`); a 0.9.4 não tem
    distribuição para ele. Há um Python 3.11 (`py -0`) e o `uv` no PATH. O caminho é
    `uv run --no-project --python 3.11 --with-requirements <requisitos com versão exata> python -m anuncios voz`.
  - [?] O `misaki`, que o `kokoro` usa, baixa o `en_core_web_sm` do spaCy pelo pip, e o ambiente do `uv` não tem pip.
    Fixe a wheel do `en_core_web_sm` no arquivo de requisitos. Não medi.
  - [?] O decodificador do Kokoro soma ruído aleatório: ponha `torch.manual_seed` antes de cada fala e confira o
    sha256 gerando duas vezes. Não medi.
  - [V] O `faster-whisper` 1.2.1 está no Python 3.14, e o modelo `faster-whisper-small` está no cache do Hugging
    Face na Karen.
  - [V] As três fontes do site estão no `google/fonts`, no commit `c30b221beb0c1da59d563feb91ec8656a1fa972a`:
    `ofl/schibstedgrotesk/SchibstedGrotesk[wght].ttf`, `ofl/newsreader/Newsreader[opsz,wght].ttf` e
    `ofl/ibmplexmono/IBMPlexMono-*.ttf`, cada uma com o `OFL.txt`. Elas vão para `anuncios/fontes/` com a origem
    (URL@commit), e servem à legenda e aos motores sem rede.
  - Proposta de desenho, que não foi aprovada nem escrita:
    - `a.json` e `b.json` levam os mesmos parâmetros (as cores e as fontes do site, a zona segura, as pausas) e
      diferem só na `ordem`;
    - cada segmento é a pausa antes, mais o bruto inteiro (sem cortar silêncio, para não ter limiar sem fonte),
      mais a pausa depois, arredondado para cima em quadros;
    - na cartela da marca, o logo sonoro toca no primeiro quadro e a voz entra depois dele;
    - os `cortes` são o começo de cada segmento menos o primeiro, e a imagem tem de cortar de verdade ali;
    - a legenda queimada não aparece no gancho nem na cartela da marca, onde a tela já mostra a própria frase. Isso
      precisa do sim do Igor;
    - no filtro `subtitles`, o `ffmpeg` roda com o diretório da montagem como pasta de trabalho, e as fontes vão
      copiadas para lá: assim o caminho não tem `C:` para escapar.
- [V] A fila da Karen: com o sim do Igor, cancelei o job #1232 (`c1-voz-chatterbox`, de 10/11, do plano antigo, com
  a voz dele). A RAM livre ficou entre 4,7 e 5,9 GiB, e três jobs de outro projeto esperam 6 GiB cada. O Kokoro e o whisper vão
  pelo `gpu_submit` com `gpus: 0`.
- No Linear, a VES-102 continua In Progress.
- Bateria: não rodou, porque esta sessão não mexeu em código, só em `docs/`.
