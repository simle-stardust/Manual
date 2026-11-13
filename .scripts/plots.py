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
NAVY = "#003767"   # granat PG
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
def read_csv_track(path):
    """CSV with lat, lon[, alt_m] -> array of (lon, lat, alt_m)."""
    import csv
    rows = list(csv.DictReader(open(path)))
    return np.array([(float(r["lon"]), float(r["lat"]), float(r.get("alt_m") or 0)) for r in rows])


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
    tr23 = read_csv_track(DATA / "2023-05-26_ilawa_aprs.csv")
    tr23b = read_csv_track(DATA / "2023-08-09_ilawa_aprs.csv")
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    for tr, lab, col in [(tr20, "20.07.2020 Toruń", NAVY),
                         (tr22, "27.02.2022 Iława", ORANGE),
                         (tr23, "26.05.2023 Iława", GREEN),
                         (tr23b, "09.08.2023 Iława", BLUE)]:
        d = along_track_km(tr)
        ground = haversine_km(tr[0, 0], tr[0, 1], tr[-1, 0], tr[-1, 1])
        if col == NAVY:
            end = "zapis kończy się na ok. 6 km"
        elif col == BLUE:
            end = f"ostatni pakiet na ok. 1 km, {ground:.0f} km od startu"
        else:
            end = f"lądowanie {ground:.0f} km od startu"
        ax.plot(d, tr[:, 2] / 1000, color=col, lw=1.5, label=f"{lab}: {end}")
        ax.plot(d[-1], tr[-1, 2] / 1000, "o", color=col, ms=4)
    ax.set_xlabel("droga przebyta nad ziemią [km]")
    ax.set_ylabel("wysokość [km]")
    ax.set_ylim(0, 36)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=7, frameon=False,
              handlelength=1.5, columnspacing=1.2)
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
    tr23 = read_csv_track(DATA / "2023-05-26_ilawa_aprs.csv")
    ax.plot(tr23[:, 0], tr23[:, 1], color=GREEN, lw=1.8, label="26.05.2023 Iława")
    tr23b = read_csv_track(DATA / "2023-08-09_ilawa_aprs.csv")
    ax.plot(tr23b[:, 0], tr23b[:, 1], color=BLUE, lw=1.8, label="09.08.2023 Iława")
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


def mission_2018():
    """Microbiology mission (2018): altitude, radiation dose, temperatures."""
    import csv
    rows = list(csv.DictReader(open(DATA / "2018_mikrobiologia_datalog.csv")))
    t = np.array([float(r["t_s"]) for r in rows]) / 60.0
    alt = np.array([float(r["alt_m"]) for r in rows]) / 1000.0
    imax = int(np.argmax(alt))

    def col(name):
        return np.array([float(r[name]) if r[name] != "" else np.nan for r in rows])

    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.9))
    ax[0].plot(t, alt, color=NAVY)
    ax[0].annotate(f"{alt[imax]:.1f} km", (t[imax], alt[imax]), textcoords="offset points",
                   xytext=(4, -2), fontsize=8, color=NAVY)
    ax[0].set_xlabel("czas od włączenia rejestratora [min]", fontsize=8)
    ax[0].set_ylabel("wysokość [km]")
    ax[0].set_title("Profil lotu", fontsize=9)

    g = [i for i, r in enumerate(rows) if r["geiger_counts"] != ""]
    gi = np.array(g)
    dose = col("dose_usv_h")[gi]
    up, dn = gi <= imax, gi > imax
    ax[1].plot(dose[up], alt[gi][up], "o", ms=3, color=ORANGE, label="wznoszenie")
    ax[1].plot(dose[dn], alt[gi][dn], "s", ms=3, color=NAVY, mfc="none", label="opadanie")
    ax[1].set_xlabel("moc dawki [µSv/h]")
    ax[1].set_ylabel("wysokość [km]")
    ax[1].set_title("Licznik Geigera", fontsize=9)
    ax[1].legend(fontsize=7, frameon=False)

    for name, lab, c in (("t_cells_c", "sekcja z komórkami", ORANGE),
                         ("t_pump_c", "pompa", BLUE),
                         ("t_pcb_c", "płytka elektroniki", GREEN),
                         ("t_ext_c", "czujnik „zewnętrzny”", GRAY)):
        ax[2].plot(t, col(name), color=c, lw=1, label=lab)
    ax[2].set_xlabel("czas od włączenia rejestratora [min]", fontsize=8)
    ax[2].set_ylabel("temperatura [°C]")
    ax[2].set_title("Temperatury w gondoli", fontsize=9)
    ax[2].legend(fontsize=6.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "misja_2018.pdf")
    plt.close(fig)


def mission_2023():
    """Platform test (26.05.2023): APRS altitude and on-board temperatures."""
    import csv
    from datetime import datetime
    aprs = list(csv.DictReader(open(DATA / "2023-05-26_ilawa_aprs.csv")))
    ts = [datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%SZ") for r in aprs]
    alt = np.array([float(r["alt_m"]) for r in aprs]) / 1000
    t = np.array([(x - ts[0]).total_seconds() / 60 for x in ts])
    imax = int(np.argmax(alt))
    log = list(csv.DictReader(open(DATA / "2023-05-26_ilawa_rejestrator.csv")))
    log = [r for r in log if r["sesja"] == "3"]

    def sec(h):
        a, b, c = map(int, h.split(":"))
        return a * 3600 + b * 60 + c
    t0 = sec(log[0]["czas_rejestratora"])
    # keep a monotonic record (the log also holds a few out-of-order lines)
    keep, last = [], -1
    for r in log:
        x = sec(r["czas_rejestratora"]) - t0
        if x >= last and x < 6 * 3600:
            keep.append(r)
            last = x
    log = keep
    tl = np.array([(sec(r["czas_rejestratora"]) - t0) / 60 for r in log])
    tin = np.array([float(r["temp_wewn_c"]) for r in log])
    tex = np.array([float(r["temp_zewn_c"]) if r["temp_zewn_c"] else np.nan for r in log])

    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.6))
    ax[0].plot(t, alt, color=GREEN)
    ax[0].annotate(f"{alt[imax]:.1f} km", (t[imax], alt[imax]), textcoords="offset points",
                   xytext=(4, -2), fontsize=8, color=GREEN)
    ax[0].set_xlabel("czas od pierwszego pakietu APRS [min]", fontsize=8)
    ax[0].set_ylabel("wysokość [km]")
    ax[0].set_title("Profil lotu (APRS)", fontsize=9)
    ax[1].plot(tl, tin, color=ORANGE, lw=1, label="wewnątrz gondoli")
    ax[1].plot(tl, tex, color=NAVY, lw=1, label="na zewnątrz")
    ax[1].set_xlabel("czas od włączenia rejestratora [min]", fontsize=8)
    ax[1].set_ylabel("temperatura [°C]")
    ax[1].set_title("Temperatury (rejestrator OBC)", fontsize=9)
    ax[1].legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "misja_2023.pdf")
    plt.close(fig)
    up = alt[:imax + 1]
    print(f"2023: max {alt[imax]:.2f} km at {t[imax]:.0f} min; last packet {t[-1]:.0f} min, "
          f"{alt[-1]*1000:.0f} m; Tin {np.nanmin(tin):.1f}..{np.nanmax(tin):.1f}, Tex min {np.nanmin(tex):.1f}")


def _isa_alt_m(p_hpa):
    """Altitude [m] in the ISA for pressure p [hPa] (valid 0-47 km)."""
    p = np.asarray(p_hpa, float) * 100
    h = np.full(p.shape, np.nan)
    m = p > 22632.1
    h[m] = 288.15 / 0.0065 * (1 - (p[m] / 101325) ** (1 / 5.25588))
    m = (p <= 22632.1) & (p > 5474.89)
    h[m] = 11000 - 6341.62 * np.log(p[m] / 22632.1)
    m = (p <= 5474.89) & (p > 868.02)
    h[m] = 20000 + 216.65 / 0.001 * ((p[m] / 5474.89) ** (-1 / 34.1632) - 1)
    m = (p <= 868.02) & (p > 110.91)
    h[m] = 32000 + 228.65 / 0.0028 * ((p[m] / 868.02) ** (-1 / 12.2011) - 1)
    return h


def mission_2020():
    """Test before BEXUS (20.07.2020): GPS and pressure altitude, temperatures."""
    import csv
    from datetime import datetime

    def hours(hms, utc_offset=0):
        a, b, c = map(int, hms.split(":"))
        return a + b / 60 + c / 3600 + utc_offset
    gps = list(csv.DictReader(open(DATA / "2020-07-20_torun_gps.csv")))
    tg = np.array([hours(r["time_utc"][11:19], 2) for r in gps])
    ag = np.array([float(r["alt_m"]) for r in gps]) / 1000
    log = list(csv.DictReader(open(DATA / "2020-07-20_torun_rejestrator.csv")))
    tl = np.array([hours(r["czas_lokalny"]) for r in log])

    def col(name):
        return np.array([float(r[name]) if r[name] != "" else np.nan for r in log])
    ap = _isa_alt_m(col("cisnienie_zewn_hpa")) / 1000
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.7))
    ax[0].plot(tl, ap, color=GRAY, lw=1, label="z ciśnienia (atm. wzorcowa)")
    ax[0].plot(tg, ag, color=NAVY, lw=1.4, label="GPS (gondola komunikacyjna)")
    ax[0].set_xlabel("czas lokalny [h]", fontsize=8)
    ax[0].set_ylabel("wysokość [km]")
    ax[0].set_title("Profil lotu", fontsize=9)
    ax[0].set_xlim(11, 17)
    ax[0].set_ylim(0, 37)
    ax[0].legend(fontsize=6.5, frameon=False, loc="upper left")
    for name, lab, c in (("temp_rtc_c", "wewnątrz (zegar RTC)", ORANGE),
                         ("temp_wewn_c", "wewnątrz (czujnik wilgotności)", GREEN),
                         ("temp_zewn_c", "na zewnątrz (czujnik wilgotności)", BLUE),
                         ("temp_zewn_cisn_c", "na zewnątrz (czujnik ciśnienia)", GRAY)):
        ax[1].plot(tl, col(name), color=c, lw=0.8, label=lab)
    ax[1].set_xlabel("czas lokalny [h]", fontsize=8)
    ax[1].set_ylabel("temperatura [°C]")
    ax[1].set_title("Temperatury (gondola eksperymentalna)", fontsize=9)
    ax[1].set_xlim(11, 17)
    ax[1].legend(fontsize=6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.27), ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "misja_2020.pdf")
    plt.close(fig)
    i = int(np.nanargmax(ag))
    up = np.where(ag > 0.2)[0][0]
    print(f"2020: GPS max {ag[i]:.2f} km at {tg[i]:.2f} h; first >200 m {tg[up]:.2f} h; "
          f"GPS end {tg[-1]:.2f} h {ag[-1]*1000:.0f} m; p-alt max {np.nanmax(ap):.1f} km")


def mission_2023_08():
    """Stormdust (09.08.2023): APRS altitude and vertical speed."""
    import csv
    from datetime import datetime
    rows = list(csv.DictReader(open(DATA / "2023-08-09_ilawa_aprs.csv")))
    ts = [datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%SZ") for r in rows]
    t = np.array([(x - ts[0]).total_seconds() / 60 for x in ts])
    alt = np.array([float(r["alt_m"]) for r in rows])
    temp = np.array([float(r["temp_tracker_c"]) for r in rows])
    t_all = t.copy()
    keep = np.r_[True, np.diff(alt) != 0]   # drop repeated (stale) positions
    t, alt = t[keep], alt[keep]
    imax = int(np.argmax(alt))
    v = np.diff(alt) / np.diff(t * 60)
    tm = (t[1:] + t[:-1]) / 2
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.6))
    ax[0].plot(t, alt / 1000, color=BLUE)
    ax[0].annotate(f"{alt[imax]/1000:.1f} km", (t[imax], alt[imax] / 1000), textcoords="offset points",
                   xytext=(-42, 0), fontsize=8, color=BLUE)
    ax[0].set_xlabel("czas od pierwszego pakietu APRS [min]", fontsize=8)
    ax[0].set_ylabel("wysokość [km]")
    ax[0].set_title("Profil lotu (APRS)", fontsize=9)
    ax[1].plot(tm, v, ".-", ms=3, lw=0.8, color=BLUE)
    ax[1].axhspan(-6, -4, color=GREEN, alpha=0.35, lw=0)
    ax[1].text(2, -9, "cel przy ziemi\nze spadochronem:\n4–6 m/s", fontsize=6.5, color=GREEN, va="top")
    k = int(np.argmin(v))
    ax[1].annotate(f"{v[k]:.0f} m/s tuż po\npęknięciu balonu", (tm[k], -60), xytext=(40, -50),
                   fontsize=6.5, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
    ax[1].set_ylim(-60, 10)
    ax[1].set_xlabel("czas od pierwszego pakietu APRS [min]", fontsize=8)
    ax[1].set_ylabel("prędkość pionowa [m/s]")
    ax[1].set_title("Wznoszenie i opadanie", fontsize=9)
    ax[2].plot(t_all, temp, color=ORANGE)
    ax[2].set_xlabel("czas od pierwszego pakietu APRS [min]", fontsize=8)
    ax[2].set_ylabel("temperatura [°C]")
    ax[2].set_title("Temperatura (DS18B20 trackera)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "misja_2023_08.pdf")
    plt.close(fig)
    up = (alt[imax] - alt[0]) / ((t[imax] - t[0]) * 60)
    dn = (alt[imax] - alt[-1]) / ((t[-1] - t[imax]) * 60)
    low = alt > 0
    j = np.where(alt[imax:] < 5300)[0][0] + imax
    dl = (alt[j] - alt[-1]) / ((t[-1] - t[j]) * 60)
    print(f"2023-08: max {alt[imax]:.0f} m at {t[imax]:.0f} min; ascent {up:.2f} m/s; "
          f"descent {dn:.1f} m/s over {t[-1]-t[imax]:.1f} min; below 5.3 km {dl:.1f} m/s; last {alt[-1]:.0f} m")


def mission_2022():
    """Training flight (27.02.2022): altitude vs ground distance and ground track."""
    tr = read_kml_track(DATA / "2022-02-27_ilawa.kml")
    d = along_track_km(tr)
    alt = tr[:, 2] / 1000
    imax = int(np.argmax(alt))
    fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.7), gridspec_kw={"width_ratios": [1.4, 1]})
    ax[0].plot(d, alt, color=ORANGE, lw=1.5)
    ax[0].plot(d[-1], alt[-1], "o", color=ORANGE, ms=4)
    ax[0].annotate(f"{alt[imax]:.1f} km", (d[imax], alt[imax]), textcoords="offset points",
                   xytext=(6, -2), fontsize=8, color=ORANGE)
    ax[0].set_xlabel("droga przebyta nad ziemią [km]", fontsize=8)
    ax[0].set_ylabel("wysokość [km]")
    ax[0].set_title("Profil lotu (tracker)", fontsize=9)
    ax[0].set_ylim(0, 36)
    ax[1].plot(tr[:, 0], tr[:, 1], color=ORANGE, lw=1.5)
    ax[1].plot(tr[0, 0], tr[0, 1], "^", color=NAVY, ms=6, label="start (Iława)")
    ax[1].plot(tr[-1, 0], tr[-1, 1], "o", color=ORANGE, ms=5, label="ostatni punkt")
    ax[1].set_xlabel("długość geograficzna [°]", fontsize=8)
    ax[1].set_ylabel("szerokość geograficzna [°]", fontsize=8)
    ax[1].set_title("Trasa nad ziemią", fontsize=9)
    ax[1].set_aspect(1 / np.cos(np.radians(tr[:, 1].mean())))
    ax[1].legend(fontsize=6.5, frameon=False, loc="best")
    ax[1].tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "misja_2022.pdf")
    plt.close(fig)
    ground = haversine_km(tr[0, 0], tr[0, 1], tr[-1, 0], tr[-1, 1])
    print(f"2022: max {alt[imax]:.2f} km; along-track {d[-1]:.0f} km; straight {ground:.0f} km; "
          f"last alt {tr[-1,2]:.0f} m; n={len(tr)}")


if __name__ == "__main__":
    parachute_table()
    tb, tl = typical_flight()
    tr20, tr22 = altitude_vs_distance()
    flight_map(tr20, tr22)
    ascent_heuristic()
    mission_2018()
    mission_2023()
    mission_2020()
    mission_2022()
    mission_2023_08()
    full = gas_table()
    print(f"typical flight: burst {tb:.0f} min, landing {tl:.0f} min")
    print(f"50 l cylinder at 200 bar holds {full:.2f} m3 of helium")
    print("figures written to", OUT)
