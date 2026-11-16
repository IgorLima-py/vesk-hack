/* O kit comum das cenas: o campo de pontos do vesklab.com e o anúncio fictício em mosaico.
   Tudo é função do tempo da cena: nenhum relógio, nenhum Math.random sem semente (o contrato do HyperFrames). */
(function () {
  // A paleta dos pontos do site, medida nos quadros de $VIDEOS/referencias/ (a mediana do quartil mais claro de cada
  // faixa de matiz): azul, violeta, roxo, magenta, rosa, laranja e âmbar. O apagado é o ponto de fundo do site.
  const PALETA = ["#5762fe", "#7c4aff", "#b53de8", "#f43ca7", "#ff516e", "#ff7c44", "#ffb84a"];
  const APAGADO = [24, 24, 29];
  const FPS = 30;

  const rgb = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const P = PALETA.map(rgb);
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const mix = (a, b, f) => [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f];
  const suave = (a, b, x) => {
    const t = clamp((x - a) / (b - a), 0, 1);
    return t * t * (3 - 2 * t);
  };
  const css = (c) => `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})`;

  function cor(u) {
    const x = clamp(u, 0, 1) * (P.length - 1);
    const i = Math.min(Math.floor(x), P.length - 2);
    return mix(P[i], P[i + 1], x - i);
  }

  function prng(seed) {
    let s = seed | 0;
    return function () {
      s = (s + 0x6d2b79f5) | 0;
      let t = Math.imul(s ^ (s >>> 15), 1 | s);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Ruído de valor 2D, liso e determinístico, para o brilho dos pontos não ser um bloco chapado.
  function ruido(seed) {
    const r = prng(seed);
    const T = Array.from({ length: 256 }, () => r());
    const h = (i, j) => T[(i * 57 + j * 131 + ((i * j) & 255)) & 255];
    return function (x, y) {
      const i = Math.floor(x), j = Math.floor(y);
      const fx = x - i, fy = y - j;
      const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      const a = h(i, j), b = h(i + 1, j), c = h(i, j + 1), d = h(i + 1, j + 1);
      return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
    };
  }

  /* O campo de pontos: uma grade de pontos redondos, apagados no fundo, que acendem na cor da paleta.
     fn(p) devolve {v, u}: v de 0 a 1 é o quanto o ponto acende (tamanho e cor), u de 0 a 1 é a cor na paleta. */
  class Campo {
    constructor(canvas, o = {}) {
      this.c = canvas;
      this.ctx = canvas.getContext("2d");
      this.passo = o.passo || 24;
      this.rMin = o.rMin ?? this.passo * 0.11;
      this.rMax = o.rMax ?? this.passo * 0.36;
      const W = canvas.width, H = canvas.height, r = prng(o.semente || 7);
      const ox = o.x0 ?? ((W % this.passo) / 2 + this.passo / 2);
      const oy = o.y0 ?? ((H % this.passo) / 2 + this.passo / 2);
      this.pontos = [];
      for (let j = 0, y = oy; y < H + this.passo; j++, y += this.passo)
        for (let i = 0, x = ox; x < W + this.passo; i++, x += this.passo) this.pontos.push({ x, y, i, j, s: r() });
    }
    desenhar(fn, fundo) {
      const { ctx, c } = this;
      if (fundo) {
        ctx.fillStyle = fundo;
        ctx.fillRect(0, 0, c.width, c.height);
      } else ctx.clearRect(0, 0, c.width, c.height);
      for (const p of this.pontos) {
        const o = fn(p);
        const v = o ? clamp(o.v, 0, 1) : 0;
        const raio = this.rMin + (this.rMax - this.rMin) * Math.pow(v, 0.8);
        ctx.fillStyle = v <= 0.001 ? css(APAGADO) : css(mix(APAGADO, cor(o.u), Math.min(1, v * 1.6)));
        ctx.beginPath();
        ctx.arc(p.x, p.y, raio, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  /* O anúncio fictício: o cartaz de um sérum (frasco âmbar de conta-gotas) de uma marca sem nome, desenhado pequeno e
     mostrado em mosaico com pontilhado, como os quadros lidos no topo do vesklab.com. Nenhuma foto, nenhuma pessoa.
     tomada: "abertura" (fundo e logo, sem produto), "frasco", "close", "gotas". */
  function desenharAnuncio(ctx, w, h, tomada, t) {
    const g = ctx.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, "#f3c6a5");
    g.addColorStop(1, "#d9785c");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
    const sol = (cx, cy, r, a) => {
      ctx.fillStyle = `rgba(255,236,214,${a})`;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();
    };
    const pedestal = (y) => {
      ctx.fillStyle = "#e9ddd2";
      ctx.fillRect(w * 0.18, y, w * 0.64, h * 0.07);
      ctx.fillStyle = "#c9b8aa";
      ctx.fillRect(w * 0.18, y + h * 0.07, w * 0.64, h * 0.3);
    };
    const frasco = (cx, base, esc) => {
      const bw = w * 0.26 * esc, bh = h * 0.27 * esc;
      ctx.fillStyle = "rgba(60,30,20,0.35)";
      ctx.fillRect(cx - bw * 0.55, base - h * 0.012, bw * 1.25, h * 0.02);
      ctx.fillStyle = "#8a3f12";
      ctx.fillRect(cx - bw / 2, base - bh, bw, bh);
      ctx.fillStyle = "#c46a22";
      ctx.fillRect(cx - bw * 0.32, base - bh * 0.95, bw * 0.14, bh * 0.85);
      ctx.fillStyle = "#f4efe8";
      ctx.fillRect(cx - bw / 2, base - bh * 0.62, bw, bh * 0.3);
      ctx.fillStyle = "#1c1717";
      ctx.fillRect(cx - bw * 0.3, base - bh - bh * 0.22, bw * 0.6, bh * 0.22);
      ctx.beginPath();
      ctx.ellipse(cx, base - bh - bh * 0.3, bw * 0.2, bh * 0.16, 0, 0, Math.PI * 2);
      ctx.fill();
    };
    const logo = (y, a) => {
      ctx.fillStyle = `rgba(255,250,244,${a})`;
      ctx.fillRect(w * 0.27, y, w * 0.46, h * 0.045);
      ctx.fillRect(w * 0.36, y + h * 0.065, w * 0.28, h * 0.022);
    };
    if (tomada === "abertura") {
      sol(w * 0.5, h * 0.42, w * (0.34 + 0.03 * t), 0.85);
      logo(h * 0.4, 0.95);
    } else if (tomada === "frasco") {
      sol(w * 0.66, h * 0.3, w * 0.3, 0.7);
      pedestal(h * 0.66);
      frasco(w * 0.5, h * 0.66, 1);
    } else if (tomada === "close") {
      sol(w * 0.3, h * 0.25, w * 0.4, 0.6);
      frasco(w * 0.52, h * 0.95, 2.1);
    } else if (tomada === "gotas") {
      sol(w * 0.5, h * 0.5, w * 0.42, 0.5);
      ctx.fillStyle = "#f7e3c6";
      for (const [x, y, r] of [[0.34, 0.42, 0.09], [0.6, 0.5, 0.13], [0.45, 0.66, 0.07], [0.68, 0.72, 0.05]]) {
        ctx.beginPath();
        ctx.arc(w * x, h * (y + 0.04 * t), w * r, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  // A matriz de Bayer 4x4, para o pontilhado ordenado do mosaico.
  const BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map((x) => (x + 0.5) / 16 - 0.5);

  /* Desenha a tomada num canvas pequeno (colunas x linhas) e copia para o canvas de destino em quadradinhos com fresta,
     com as cores reduzidas a 5 níveis por canal e pontilhadas: o «anúncio lido» do site. */
  class Mosaico {
    constructor(canvas, colunas = 40) {
      this.c = canvas;
      this.ctx = canvas.getContext("2d");
      this.col = colunas;
      this.lin = Math.round((colunas * canvas.height) / canvas.width);
      this.p = document.createElement("canvas");
      this.p.width = this.col;
      this.p.height = this.lin;
      this.pctx = this.p.getContext("2d", { willReadFrequently: true });
    }
    desenhar(tomada, t) {
      const { col, lin, pctx, ctx, c } = this;
      desenharAnuncio(pctx, col, lin, tomada, t);
      const d = pctx.getImageData(0, 0, col, lin).data;
      const cw = c.width / col, chh = c.height / lin, fresta = Math.max(1, cw * 0.12);
      ctx.fillStyle = "#0b0b10";
      ctx.fillRect(0, 0, c.width, c.height);
      for (let j = 0; j < lin; j++)
        for (let i = 0; i < col; i++) {
          const k = (j * col + i) * 4, b = BAYER[(j & 3) * 4 + (i & 3)];
          const q = (x) => clamp(Math.round((x / 255) * 4 + b) / 4, 0, 1) * 255;
          ctx.fillStyle = `rgb(${q(d[k]) | 0},${q(d[k + 1]) | 0},${q(d[k + 2]) | 0})`;
          ctx.fillRect(i * cw, j * chh, cw - fresta, chh - fresta);
        }
    }
  }

  /* O tempo das cenas. A raiz põe cada cena 1/4 de quadro antes do quadro dela (anuncios/cenas.py), e por isso a
     palavra que a linha do tempo põe no quadro q da cena aparece com um set em q/30 s, que cai entre os quadros
     q-1 e q, longe da igualdade de ponto flutuante. */
  const q = (quadro) => quadro / FPS;
  function segmento(chave) {
    const s = (window.VESK && window.VESK.segmentos && window.VESK.segmentos[chave]) || null;
    if (!s) throw new Error(`a raiz não passou o segmento ${chave} em window.VESK`);
    return s;
  }
  function palavra(seg, texto) {
    const p = seg.palavras.find((x) => x.texto.replace(/[.,?!;:]/g, "") === texto);
    if (!p) throw new Error(`a palavra ${texto} não está na fala ${seg.chave}`);
    return p;
  }

  /* As palavras de uma frase: cada uma vira tinta no quadro em que é dita, em 0,1 s, sem mexer de lugar
     (a entrada «do cinza à tinta» do motion.md do HyperFrames). */
  function falarPalavras(tl, seg, elementos) {
    elementos.forEach((el, i) => {
      const p = seg.palavras[i];
      tl.fromTo(el, { color: "#3b3a46" }, { color: "#eeedf4", duration: 0.1, ease: "power1.out" }, q(p.inicio));
    });
  }

  /* O marca-texto: o amarelo corre da esquerda para a direita em `dur` segundos, e a letra escurece junto. */
  function grifar(tl, el, inicio, dur = 0.35) {
    tl.fromTo(el, { "--g": "0%" }, { "--g": "100%", duration: dur, ease: "power2.inOut" }, inicio);
    const alvos = [el, ...el.querySelectorAll(".vk-palavra")];
    tl.fromTo(alvos, { color: "#eeedf4" }, { color: "#0b0b10", duration: dur * 0.6, ease: "none", immediateRender: false },
      inicio + dur * 0.3);
  }

  /* Um relógio da cena para o que é desenhado em canvas: um único tween de 0 até a duração, sem ease, cujo onUpdate
     redesenha o quadro a partir do tempo e de nada mais. */
  function relogio(tl, duracao, desenhar) {
    const t = { t: 0 };
    tl.fromTo(t, { t: 0 }, { t: duracao, duration: duracao, ease: "none", onUpdate: () => desenhar(t.t) }, 0);
    desenhar(0);
  }

  window.VeskKit = { PALETA, FPS, cor, css, mix, clamp, suave, prng, ruido, Campo, Mosaico, desenharAnuncio,
    q, segmento, palavra, falarPalavras, grifar, relogio };
})();
