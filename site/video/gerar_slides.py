"""Gera site/video/slides.pptx: 6 slides no visual da Vesk, com a fala inteira de cada um nas notas.
Uso (precisa do python-pptx): python site/video/gerar_slides.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

BG, FG, MUT, GRIFO = (RGBColor.from_string(c) for c in ("000000", "EEEDF4", "A09DB2", "FFE14A"))
SERIFA, TEXTO, MONO = "Georgia", "Segoe UI", "Consolas"

SLIDES = [
    dict(
        titulo="Creative autopilot",
        sub="Hack Brasil 2026 · Logistics & automation",
        corpo=["A media buyer's weekly loop on each new video ad, running on its own."],
        notas="""[0:00] Hi, I'm Igor. This is Creative autopilot, my entry in the Logistics and automation track.
Every week, a media buyer repeats the same loop on each new video ad. This project runs that loop on its own.
(Look at the camera for this one. Next slide.)""",
    ),
    dict(
        titulo="The loop nobody automates",
        corpo=[
            "1. Pull the retention curve",
            "2. Watch the video, second by second",
            "3. Guess why people left",
            "4. Write the report, brief a new cut, plan the test",
            "Hours of manual work, per ad, every week.",
        ],
        notas="""[0:15] Here is the loop. You pull the retention curve from the ad platform. You watch the video second by second.
Then you guess why people left, write the report, brief a new cut, and plan the test.
It is information moving between three places: the platform, a video analysis, and the person who decides what to test next. That is the work this track is about, and it takes hours per ad.""",
    ),
    dict(
        titulo="Pull → Read → Cross → Deliver",
        corpo=[
            "Pull: video and retention curve, from Meta",
            "Read: a private engine, called by API, reads every second",
            "Cross: what was on screen at each drop of the curve",
            "Deliver: report, one-change variant, test plan",
        ],
        notas="""[0:40] The autopilot has four steps.
Pull: the ad video and the platform's retention curve, from the Meta Insights API or the Ads Manager export.
Read: a private video-reading engine, called by API, reads every second: cuts, faces, logo, speech and on-screen text. To this repository the engine is a black box with a written contract.
Cross: what was on screen and in the audio at each drop of the curve. We only use the points the platform gives us. Nothing is interpolated.
Deliver: a report, a variant with one change only, and a test plan with the sample size per arm. A new ad triggers a new report.""",
    ),
    dict(
        titulo="Proof with a known answer",
        corpo=[
            "python -m exemplos.sintetico --marca-em 7 --semente 9 --saida x.mp4",
            "Synthetic video: the brand appears at second 7",
            "The answer key says marca_em = 7; the check compares it with what the tools find",
        ],
        mono_primeira=True,
        notas="""[1:10] How do we know it works? With synthetic videos where the answer is known.
(Switch to the terminal and run the command on the slide. Show the generated video and the gabarito.json next to it, the field marca_em says 7.)
This generator makes a video with cuts at known seconds, the word VESK on screen and the word Vesk in the voice, starting at second seven. The answer key is written next to the file.
The tests check the cuts and the on-screen text with ffmpeg, outside the generator, so the generator never grades itself.
(If the command is slow on the day, show a screenshot of the passing tests instead and say the same lines.)""",
    ),
    dict(
        titulo="Where it stands today",
        corpo=[
            "Done: synthetic examples with answer key, engine contract, tests on every push, this page",
            "Next: the pull from Meta, the report, the one-change variant, the test plan",
            "Only our own ads, synthetic videos, and what a person sends",
        ],
        notas="""[1:50] Here is the honest state, because this is a draft of a project still being built during the online phase.
Done today: the synthetic examples with an answer key, the contract the engine has to meet, tests that run on every push, and this page.
Next: the pull from Meta, the report, the one-change variant with its pixel certificate, and the test plan.
And one rule about data: we only process our own ads, synthetic videos, and what a person sends us. Nothing from third parties collected outside official APIs.""",
    ),
    dict(
        titulo="Code, page, license",
        corpo=[
            "github.com/IgorLima-py/vesk-hack",
            "hack.vesklab.com",
            "PolyForm Noncommercial 1.0.0",
        ],
        mono_primeira=True,
        notas="""[2:15] Everything is in a public repository: github.com/IgorLima-py/vesk-hack. The page is at hack.vesklab.com, in English and Portuguese, with no forms.
The license is PolyForm Noncommercial: anyone can read, run and test the code.
Thank you for watching.
(Stop recording around 2:30.)""",
    ),
]


def texto(slide, x, y, w, h, linhas, tam, cor, fonte, negrito=False):
    caixa = slide.shapes.add_textbox(x, y, w, h)
    tf = caixa.text_frame
    tf.word_wrap = True
    for i, linha in enumerate(linhas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(14)
        r = p.add_run()
        r.text = linha
        r.font.size, r.font.name, r.font.bold = Pt(tam), fonte, negrito
        r.font.color.rgb = cor
    return caixa


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    vazio = prs.slide_layouts[6]
    for i, s in enumerate(SLIDES):
        sl = prs.slides.add_slide(vazio)
        sl.background.fill.solid()
        sl.background.fill.fore_color.rgb = BG
        texto(sl, Inches(0.9), Inches(0.9), Inches(11.5), Inches(1.6), [s["titulo"]],
              54 if i == 0 else 44, FG, SERIFA)
        barra = sl.shapes.add_shape(1, Inches(0.9), Inches(2.35), Inches(1.4), Emu(76200))
        barra.fill.solid(); barra.fill.fore_color.rgb = GRIFO; barra.line.fill.background()
        y = Inches(2.9)
        if s.get("sub"):
            texto(sl, Inches(0.9), y, Inches(11.5), Inches(0.6), [s["sub"]], 22, GRIFO, MONO)
            y = Inches(3.7)
        for j, linha in enumerate(s["corpo"]):
            mono = s.get("mono_primeira") and j == 0
            texto(sl, Inches(0.9), y, Inches(11.5), Inches(0.9), [linha],
                  22 if mono else 26, GRIFO if mono else (FG if j == 0 else MUT),
                  MONO if mono else TEXTO)
            y += Inches(0.95)
        texto(sl, Inches(0.9), Inches(6.7), Inches(8), Inches(0.4),
              [f"Vesk · Hack Brasil 2026 · {i + 1}/{len(SLIDES)}"], 12, MUT, MONO)
        sl.notes_slide.notes_text_frame.text = s["notas"]
    saida = Path(__file__).with_name("slides.pptx")
    prs.save(saida)
    print(saida)


if __name__ == "__main__":
    main()
