"""O tamanho de amostra por braço de um teste A/B de duas proporções, escrito do zero.

Fonte: Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*, 2ª ed., Lawrence Erlbaum,
cap. 6 («Differences between proportions»). O efeito é o `h` de Cohen, a diferença das proporções na escala do
arco-seno, onde a variância de cada braço fica 1/n:

    φ = 2·arcsen(√p)          h = φ2 − φ1

O teste é bicaudal, com braços do mesmo tamanho n. A diferença φ̂2 − φ̂1 tem variância 2/n, e o poder é

    poder(n) = Φ(|h|·√(n/2) − z) + Φ(−|h|·√(n/2) − z),     z = Φ⁻¹(1 − α/2)

O n por braço é o menor inteiro com poder(n) ≥ o poder pedido. A forma fechada, que ignora o segundo termo,

    n ≈ 2·((z + Φ⁻¹(poder)) / h)²

dá o ponto de partida, e a busca anda de 1 em 1 a partir dele. É a mesma conta do `NormalIndPower` com o
`proportion_effectsize` do statsmodels (o n dele, arredondado para cima), que só entra nos testes, como conferência:
https://www.statsmodels.org/stable/generated/statsmodels.stats.power.NormalIndPower.html
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist

FONTE = ("Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences, 2ª ed., cap. 6 "
         "(diferenças entre proporções, h de Cohen)")
CONFERENCIA = "https://www.statsmodels.org/stable/generated/statsmodels.stats.power.NormalIndPower.html"
_N = NormalDist()


class SemEfeito(ValueError):
    pass


@dataclass(frozen=True)
class Plano:
    p1: float
    p2: float
    alfa: float
    poder_pedido: float
    h: float
    z_alfa: float
    z_poder: float
    n_aproximado: float
    n_por_braco: int
    poder_atingido: float


def efeito_h(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))


def poder(n: float, h: float, alfa: float) -> float:
    z = _N.inv_cdf(1 - alfa / 2)
    d = abs(h) * math.sqrt(n / 2)
    return _N.cdf(d - z) + _N.cdf(-d - z)


def _entre_0_e_1(nome: str, x: float) -> None:
    if not 0 < x < 1:
        raise ValueError(f"{nome} precisa estar entre 0 e 1, sem incluir as pontas (veio {x:g})")


def calcular(p1: float, p2: float, alfa: float = 0.05, poder_pedido: float = 0.8) -> Plano:
    for nome, x in (("--p1", p1), ("--p2", p2), ("--alfa", alfa), ("--poder", poder_pedido)):
        _entre_0_e_1(nome, x)
    if p1 == p2:
        raise SemEfeito(f"não há efeito a detectar: p1 é igual a p2 ({p1:g}), e nenhum n chega ao poder pedido")
    h = efeito_h(p1, p2)
    z_alfa = _N.inv_cdf(1 - alfa / 2)
    z_poder = _N.inv_cdf(poder_pedido)
    aproximado = 2 * ((z_alfa + z_poder) / h) ** 2
    # A forma fechada ignora o segundo termo, que só soma poder: o n certo é ≤ ceil(aproximado).
    n = max(1, math.ceil(aproximado))
    while n > 1 and poder(n - 1, h, alfa) >= poder_pedido:
        n -= 1
    while poder(n, h, alfa) < poder_pedido:
        n += 1
    return Plano(p1, p2, alfa, poder_pedido, h, z_alfa, z_poder, aproximado, n, poder(n, h, alfa))


def texto(pl: Plano) -> str:
    return "\n".join([
        f"n por braço: {pl.n_por_braco}",
        f"total (2 braços): {2 * pl.n_por_braco}",
        f"p1 = {pl.p1:g}, p2 = {pl.p2:g}, alfa = {pl.alfa:g} (bicaudal), poder pedido = {pl.poder_pedido:g}, "
        f"poder com esse n = {pl.poder_atingido:.4f}",
        f"h de Cohen = 2·arcsen(√p2) − 2·arcsen(√p1) = {pl.h:.6f}",
        f"fórmula: o menor n com poder(n) ≥ {pl.poder_pedido:g}, em que "
        f"poder(n) = Φ(|h|·√(n/2) − z) + Φ(−|h|·√(n/2) − z) e z = Φ⁻¹(1 − α/2) = {pl.z_alfa:.4f}; "
        f"a forma fechada 2·((z + Φ⁻¹(poder))/h)² dá {pl.n_aproximado:.2f}",
        f"fonte: {FONTE}",
        f"conferência: o NormalIndPower do statsmodels dá o mesmo n ({CONFERENCIA})",
    ])
