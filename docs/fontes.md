# O que a Meta e o TikTok dão por anúncio

Lido na doc oficial em 03/11/2026. Cada linha traz a URL e a frase literal.

## Conclusão

A Meta dá a curva por segundo de 0 a 14 s, depois em faixas, mais os pontos de 25 a 100% e o tempo médio. O TikTok dá
o tempo médio, os pontos de 25 a 100% e as visualizações de 2 s e de 6 s. Que o export do Gerenciador de Anúncios da
Meta traga essas colunas: não achei na doc, e a C4 confere no export real.

## Meta (Insights API)

- Curva por segundo, `video_play_curve_actions` — https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights diz «Entries 0 to 14 represent seconds 0 thru 14.»
- Tempo médio, `video_avg_time_watched_actions` — mesma página: «The average time a video was played, including any time spent replaying the video for a single impression.»
- Pontos de 25, 50, 75, 95 e 100%: `video_p25_watched_actions`, `video_p50_watched_actions`, `video_p75_watched_actions`, `video_p95_watched_actions` e `video_p100_watched_actions` — mesma página, por exemplo «The number of times your video was played at 25% of its length, including plays that skipped to this point.»
- Acesso: «If your app is managing other people's ad accounts, you need advanced access to the `ads_read` and/or `ads_management` permissions» — https://developers.facebook.com/docs/marketing-api/overview/authorization (04/11/2026). Este repositório lê só a conta da Vesk.

## TikTok

- Tempo médio, `average_video_play` — https://ads.tiktok.com/help/article/video-play?lang=en diz «Average time your video was played per single video view, including any time spent replaying the video.»
- Pontos de 25, 50, 75 e 100%: `video_views_p25`, `video_views_p50`, `video_views_p75` e `video_views_p100` — mesma página, por exemplo «Number of times your video was played at least 25% of its length.»
- Visualizações de 2 s, `video_watched_2s` — mesma página: «Number of times your video starts playing for at least 2 seconds in an impression session.»
- Visualizações de 6 s, `video_watched_6s` — a ajuda soma o engajamento nos primeiros 6 s, e a tabela da API (https://business-api.tiktok.com/portal/docs/basic-reports-supported-metrics/v1.3) não soma: as duas fontes oficiais divergem.
- O export do Ads Manager — https://ads.tiktok.com/resources/help/article/view-report diz «click Download to export the table as a CSV.»
