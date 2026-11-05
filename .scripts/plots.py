#!/usr/bin/env python3
"""Generate data figures and tables for the Stardust NEXT manual.

Output goes to tex/figures/generated/ (PDF figures, .tex tables).
Run:  python3 .scripts/plots.py
Needs: matplotlib, numpy; geopandas<1.0 (for the map outline, optional).
"""
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "tex" / "figures" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

ORANGE = "#E8592B"
NAVY = "#1B2A4A"
GRAY = "#6B7280"
BLUE = "#2F6DB5"
GREEN = "#2E8B57"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,   # TrueType: text in figures is selectable/searchable
})


# ---------------------------------------------------------------- helpers
def read_kml_track(path, name_hint=None, min_points=10):
    text = Path(path).read_text(errors="ignore")
    tracks = []
    for pm in re.findall(r"<Placemark[^>]*>(.*?)</Placemark>", text, re.S):
        for c in re.findall(r"<coordinates>(.*?)</coordinates>", pm, re.S):
            pts = [tuple(map(float, x.split(","))) for x in c.split() if x.count(",") == 2]
            if len(pts) >= min_points:
                tracks.append(np.array(pts))
    return max(tracks, key=len)


def haversine_km(lon1, lat1, lon2, lat2):
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def along_track_km(tr):
    d = haversine_km(tr[:-1, 0], tr[:-1, 1], tr[1:, 0], tr[1:, 1])
    return np.concatenate([[0], np.cumsum(d)])


# ---------------------------------------------------------------- atmosphere
SCALE_H = 7238.3      # m, scale height used by the classic burst calculator
RHO0 = 1.2050         # kg/m3, air density at ground
RHO_HE = 0.1786       # kg/m3, helium density
G = 9.80665


def rho_air(h):
    return RHO0 * np.exp(-h / SCALE_H)


# ---------------------------------------------------------------- 1. typical flight
def typical_flight():
    v_up = 5.0                # m/s
    h_burst = 33000.0         # m
    v_down0 = 5.0             # m/s at ground under parachute
    t_up = h_burst / v_up
    t = [0.0]
    h = [0.0]
    dt = 10.0
    while h[-1] < h_burst:
        t.append(t[-1] + dt)
        h.append(min(h_burst, h[-1] + v_up * dt))
    # descent: terminal velocity scales with 1/sqrt(rho)
    while h[-1] > 0:
        v = v_down0 * math.sqrt(RHO0 / rho_air(h[-1]))
        t.append(t[-1] + dt)
        h.append(max(0.0, h[-1] - v * dt))
    t = np.array(t) / 60.0
    h = np.array(h) / 1000.0
    t_burst = t_up / 60.0
    t_land = t[-1]

    # 2020 mission timeline (Test Mission Technical Report 2020/07/20)
    m20_t = np.array([0, 43, 152, 177, 272, 278, 285, 296])  # min after 11:36
    m20_h = np.array([0.04, 11, 32, 33, 33, 16, 8, 0.1])

    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    ax.fill_between(t, 0, h, color=ORANGE, alpha=0.08)
    ax.plot(t, h, color=ORANGE, lw=2, label="model: wznoszenie 5 m/s, pęknięcie 33 km")
    ax.plot(m20_t, m20_h, "o--", color=NAVY, ms=4, lw=1,
            label="misja 20.07.2020 (brak odcinacza, dryf 1,5 h)")
    ax.axhspan(0, 12, color=BLUE, alpha=0.05)
    ax.text(205, 6, "troposfera", color=BLUE, fontsize=8, va="center")
    ax.text(205, 24, "stratosfera", color=NAVY, fontsize=8, va="center")
    ax.annotate("pęknięcie powłoki", (t_burst, 33), xytext=(t_burst - 60, 36),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=8)
    ax.annotate(f"lądowanie po ok. {t_land:.0f} min", (t_land, 0), xytext=(t_land + 12, 2.5),
                arrowprops=dict(arrowstyle="->", color=GRAY), fontsize=8)
    ax.annotate("wznoszenie\n≈ 110 min", (72, 3), fontsize=8, ha="center", color=ORANGE)
    ax.annotate(f"opadanie\n≈ {t_land - t_burst:.0f} min", (t_burst + 25, 20), fontsize=8,
                ha="center", color=ORANGE)
    ax.set_xlabel("czas od startu [min]")
    ax.set_ylabel("wysokość [km]")
    ax.set_ylim(0, 40)
    ax.set_xlim(0, 310)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False)
    fig.savefig(OUT / "profil_typowy.pdf")
    plt.close(fig)
    return t_burst, t_land


# ---------------------------------------------------------------- 2. altitude vs distance
def altitude_vs_distance():
    tr22 = read_kml_track(DATA / "2022-02-27_ilawa.kml")
    tr20 = read_kml_track(DATA / "2020-07-20_torun.kml")
    fig, ax = plt.subplots(figsize=(6.3, 2.8))
    for tr, lab, col in [(tr22, "27.02.2022 Iława (RTTY)", ORANGE),
                         (tr20, "20.07.2020 Toruń (rejestrator)", NAVY)]:
        d = along_track_km(tr)
        ax.plot(d, tr[:, 2] / 1000, color=col, lw=1.5, label=lab)
        ground = haversine_km(tr[0, 0], tr[0, 1], tr[-1, 0], tr[-1, 1])
        txt = (f"lądowanie {ground:.0f} km od startu\n(w linii prostej)" if tr[-1, 2] < 2000
               else "zapis rejestratora kończy się\nna wys. ok. 6 km")
        ax.annotate(txt, (d[-1], tr[-1, 2] / 1000), xytext=(d[-1] - 75, 3 + 9 * (col == NAVY)),
                    fontsize=7.5, color=col, arrowprops=dict(arrowstyle="->", color=col))
    ax.set_xlabel("droga przebyta nad ziemią [km]")
    ax.set_ylabel("wysokość [km]")
    ax.set_ylim(0, 38)
    ax.legend(loc="upper right", fontsize=7.5, frameon=False)
    fig.savefig(OUT / "profil_dystans.pdf")
    plt.close(fig)
    return tr20, tr22


# ---------------------------------------------------------------- 3. map
def flight_map(tr20, tr22):
    fig, ax = plt.subplots(figsize=(6.3, 5.2))
    try:
        import geopandas as gpd
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        world.plot(ax=ax, color="#F3F4F6", edgecolor="#9CA3AF", lw=0.6)
        bad = world[world.name.isin(["Russia", "Belarus", "Ukraine"])]
        bad.plot(ax=ax, color="#FDE2E2", edgecolor="#DC2626", lw=0.8, hatch="///")
    except Exception as exc:  # pragma: no cover
        print("map outline unavailable:", exc)
    ax.plot(tr20[:, 0], tr20[:, 1], color=NAVY, lw=1.8, label="20.07.2020 Toruń")
    ax.plot(tr22[:, 0], tr22[:, 1], color=ORANGE, lw=1.8, label="27.02.2022 Iława")
    # 26.05.2023: only start and landing are known
    s23, l23 = (19.565, 53.596), (19.952, 53.556)
    ax.annotate("", xy=l23, xytext=s23,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8, ls="--"))
    ax.plot([], [], color=GREEN, ls="--", label="26.05.2023 Iława (start–lądowanie)")
    cities = {"Gdańsk": (18.65, 54.35), "Toruń": (18.60, 53.01), "Iława": (19.57, 53.60),
              "Olsztyn": (20.48, 53.78), "Brodnica": (19.40, 53.26),
              "Góra Dylewska": (19.95, 53.56), "Warszawa": (21.01, 52.23)}
    for n, (x, y) in cities.items():
        ax.plot(x, y, "o", color="black", ms=2.5)
        ax.text(x + 0.06, y + 0.04, n, fontsize=7)
    ax.text(21.0, 54.55, "Obwód królewiecki\n(Rosja)", fontsize=7.5, color="#B91C1C", ha="center")
    ax.text(23.9, 53.0, "Białoruś", fontsize=7.5, color="#B91C1C", ha="center")
    ax.text(18.6, 54.85, "Morze Bałtyckie", fontsize=7.5, color=BLUE, style="italic")
    ax.set_xlim(16.8, 24.4)
    ax.set_ylim(51.9, 55.1)
    ax.set_aspect(1 / math.cos(math.radians(53.5)))
    ax.set_xlabel("długość geograficzna [°E]")
    ax.set_ylabel("szerokość geograficzna [°N]")
    ax.legend(loc="lower left", fontsize=7.5, framealpha=0.9)
    fig.savefig(OUT / "mapa_lotow.pdf")
    plt.close(fig)


# ---------------------------------------------------------------- 4. ascent-rate heuristic
def burst_calc(m_payload, m_balloon, d_burst, v, cd=0.25):
    """Classic burst calculator (UKHAS / SondeHub) – returns launch volume,
    burst altitude, neck lift and time to burst."""
    a = G * (RHO0 - RHO_HE) * (4 / 3) * math.pi
    b = -0.5 * v ** 2 * cd * RHO0 * math.pi
    d = -(m_payload + m_balloon) * G
    roots = np.roots([a, b, 0, d])
    r = max(x.real for x in roots if abs(x.imag) < 1e-9 and x.real > 0)
    v_launch = 4 / 3 * math.pi * r ** 3
    v_burst = 4 / 3 * math.pi * (d_burst / 2) ** 3
    h_burst = -SCALE_H * math.log(v_launch / v_burst)
    neck_lift = (v_launch * (RHO0 - RHO_HE) - m_balloon) * 1000
    return v_launch, h_burst, neck_lift, h_burst / v / 60


def ascent_heuristic():
    rates = np.linspace(2.0, 8.0, 61)
    cases = [(0.8, 7.00, "powłoka 800 g"), (1.2, 8.63, "powłoka 1200 g")]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.7))
    for (mb, db, lab), col in zip(cases, [ORANGE, NAVY]):
        res = [burst_calc(2.0, mb, db, v) for v in rates]
        ax1.plot(rates, [x[1] / 1000 for x in res], color=col, lw=1.8, label=lab)
        ax2.plot(rates, [x[3] for x in res], color=col, lw=1.8, label=lab)
    for ax in (ax1, ax2):
        ax.axvspan(2.0, 5.0, color="#DC2626", alpha=0.07)
        ax.axvline(5.0, color="#DC2626", lw=1, ls="--")
        ax.set_xlabel("prędkość wznoszenia [m/s]")
    ax1.text(3.5, 25.3, "ryzyko\nucieczki", color="#B91C1C", fontsize=7.5, ha="center")
    ax1.set_ylabel("wysokość pęknięcia [km]")
    ax2.set_ylabel("czas wznoszenia [min]")
    ax1.set_ylim(25, 40)
    ax1.legend(fontsize=7.5, frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "heurystyka_wznoszenia.pdf")
    plt.close(fig)

    # example table for the manual (payload 2 kg, 800 g balloon)
    rows = []
    for v in [3, 4, 5, 6, 7]:
        vl, hb, nl, tb = burst_calc(2.0, 0.8, 7.0, v)
        rows.append(f"{v} & {vl:.1f} & {nl/1000:.2f} & {hb/1000:.1f} & {tb:.0f} \\\\")
    (OUT / "tabela_wznoszenia.tex").write_text("\n".join(rows) + "\n")


# ---------------------------------------------------------------- 5. gas from pressure
P0 = 1.01325  # bar


def z_helium(p_abs_bar):
    """Compressibility of helium near room temperature (second virial
    coefficient B ≈ 11.8 cm3/mol at 293 K): Z ≈ 1 + 4.8e-4·p[bar]."""
    return 1 + 4.84e-4 * p_abs_bar


def gas_released(v_cyl_l, p1_gauge, p2_gauge, t_c=15.0):
    p1 = p1_gauge + P0
    p2 = p2_gauge + P0
    t_ref = 288.15
    t = t_c + 273.15
    return v_cyl_l / 1000 * (p1 / z_helium(p1) - p2 / z_helium(p2)) / P0 * (t_ref / t)


def gas_table():
    rows = []
    for p2 in [180, 160, 150, 140, 120, 100, 80, 60, 40, 20, 0]:
        v50 = gas_released(50, 200, p2)
        v10 = gas_released(10, 200, p2)
        rows.append(f"{p2} & {200-p2} & {v10:.2f} & {v50:.2f} & {v50*1.056:.2f} \\\\")
    (OUT / "tabela_gazu.tex").write_text("\n".join(rows) + "\n")
    # coefficient per bar near full cylinder
    return gas_released(50, 200, 0)


# ---------------------------------------------------------------- 6. parachute
def descent_speed(m, d, cd=0.8, rho=1.225):
    """Terminal velocity under a parachute of diameter d [m] (canopy area pi d^2/4)."""
    area = math.pi * d ** 2 / 4
    return math.sqrt(2 * m * G / (rho * cd * area))


def parachute_table():
    diams = [0.6, 0.9, 1.2, 1.5, 1.8]
    rows = []
    for m in [1.0, 2.0, 3.0, 4.0]:
        cells = []
        for d in diams:
            v = descent_speed(m, d)
            txt = f"{v:.1f}".replace(".", ",")
            if 4.0 <= v <= 6.0:
                txt = "\\cellcolor{sdtip}\\textbf{" + txt + "}"
            cells.append(txt)
        rows.append(f"{m:.0f} & " + " & ".join(cells) + " \\\\")
    (OUT / "tabela_spadochronu.tex").write_text("\n".join(rows) + "\n")


if __name__ == "__main__":
    parachute_table()
    tb, tl = typical_flight()
    tr20, tr22 = altitude_vs_distance()
    flight_map(tr20, tr22)
    ascent_heuristic()
    full = gas_table()
    print(f"typical flight: burst {tb:.0f} min, landing {tl:.0f} min")
    print(f"50 l cylinder at 200 bar holds {full:.2f} m3 of helium")
    print("figures written to", OUT)
