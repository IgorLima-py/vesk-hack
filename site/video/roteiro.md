# Vídeo do rascunho — roteiro

Os slides estão em `site/video/slides.pptx`, com a fala inteira de cada um nas notas do slide (o `gerar_slides.py` refaz o arquivo).
Como gravar: abra o PowerPoint em modo apresentador, grave a tela com a webcam e leia as notas. Esta tabela é só o mapa de tempo.

Limite do regulamento: 3 min, com demo, sem login; de preferência narrado em inglês. Alvo: 2:30.
O rascunho só pede trilha, repositório público com README, vídeo e página HTTPS. Mostre só o que já existe no dia da
gravação; o que ainda não existe fica como «em construção», nunca como pronto.

| # | Tempo | Slide / tela | Fala (EN) |
|---|-------|--------------|-----------|
| 1 | 0:00–0:15 | Título: «Creative autopilot», Hack Brasil, Logística & automação | Every week a media buyer repeats the same loop on each new video ad. This project runs that loop on its own. |
| 2 | 0:15–0:40 | O ciclo manual: curva → assistir → adivinhar → laudo → briefing → teste | Pull the retention curve, watch the video second by second, guess why people left, write the report, brief a new cut, plan the test. Hours per ad. |
| 3 | 0:40–1:10 | Diagrama: Pull → Read → Cross → Deliver (README) | We pull the video and the curve from Meta. A private engine, called by API, reads every second. We cross what was on screen with each drop. Only the points the platform gives; nothing is interpolated. |
| 4 | 1:10–1:50 | Demo: vídeo sintético com marca em segundo conhecido (C3) e o gabarito ao lado | To prove it works we use synthetic videos with a known answer key: the brand appears at second seven, and we check that the engine finds second seven. |
| 5 | 1:50–2:15 | Estado: o que roda hoje × o que vem (laudo, variante de uma mudança, plano do teste) | Today: the pull, the contract with the engine, the tests on every push. Next: the report, the one-change variant and the test plan. |
| 6 | 2:15–2:30 | Repositório + página + licença | Public repository, PolyForm Noncommercial, page at hack.vesklab.com. Thank you. |

Antes de gravar: o slide 4 só entra depois que a C3 fechar; sem ela, troque por um print da bateria verde.
Navegador aberto no vídeo: sempre mudo (`--mute-audio`).
