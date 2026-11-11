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

**A próxima sessão é a C1v** (decisão do Igor no `/tchau` do orquestrador, 11/11). Abra com `/oi c1v`: o ponteiro
continua no O, porque só o orquestrador mexe nele, e o `/oi` com a fatia no comando compara o perfil com o da C1v
(`criativo`, opus/xhigh, plan mode, na Karen). O aviso de que o ponteiro pede `dificil` é esperado.

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

## O orquestrador (11/11/2026): não fechou, segue aberto

- [V] Na abertura, o `git pull` trouxe a C3 (✅) e a C2 (subiu sem fechar) até o `67b67e4`; modelo Opus e esforço
  `high` medido pelo Bash, como a tabela pede para o `dificil`.
- O Igor achou que o roteiro não tinha pensado em como fazer os vídeos, e o orquestrador abriu uma sessão própria de
  pesquisa (perfil `replan`), em vez de pesquisar ele mesmo. Ela abriu em `high`, porque o orquestrador não abre acima
  do próprio esforço, e o Igor a subiu para `xhigh`. O que ela entregou está na seção «Pesquisa dos vídeos e a C1v»
  acima (a C1v na fila, a skill `video`).
- Nenhuma outra fatia foi aberta: a C1 passou a esperar a C1v, e a C4 e a C5 esperam o que sai das duas.
- O O não fecha: o `sai:` dele é todas as fatias ✅ ou cortadas. O ponteiro fica nele.
- Bateria: não rodou, porque o orquestrador não mexeu em código.

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
