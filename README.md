# Vesk Hack — creative autopilot

Every week, a media buyer runs the same manual loop on each new video ad: pull the retention curve, watch the video
second by second, guess why people left, write the report, brief a new cut and plan a test. This project runs that
loop on its own.

## Track

**Logistics & automation** at Hack Brasil 2026: «Projetos que movem bens, informação ou trabalho de forma mais
eficiente.» (https://hackbrasil.com/regulamento)

## How it works

1. **Pull:** the ad video and the platform's retention curve, from the Meta Insights API or from the Ads Manager export.
2. **Read:** a private video-reading engine, called by API, reads every second of the video: cuts, faces, logo,
   speech and on-screen text.
3. **Cross:** what was on screen and in the audio at each drop of the curve. Only the points the platform gives are
   used, and nothing is interpolated.
4. **Deliver:** a report, a variant with one change only (with a pixel certificate that nothing else changed) and a
   test plan with the sample size per arm. A new ad triggers a new report.

## Status

Being built during the online phase of Hack Brasil (November 5–30, 2026). The work queue is in `docs/ROADMAP.md`, in
Portuguese.

## License

PolyForm Noncommercial 1.0.0 (see `LICENSE`). Anyone can read, run and test this code. Commercial use is not licensed.
