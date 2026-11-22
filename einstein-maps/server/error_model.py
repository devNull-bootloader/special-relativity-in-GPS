import sys, os, csv
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "simulations"))
from bounded_utilities import (kepler_solver, true_anomaly, satellite_distance,
    eccentricity_correction_ns, sagnac_correction_ns, latlon_to_ecef,
    satellite_position_ecef, GM, c, R_EARTH, OMEGA_EARTH)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "gnss_orbital_parameters.csv")

TIME_SCALE = 600          # TODO: tune
BEARING_DEG = 45          # direction of the error vector
STATION = (53.1, 8.8, 10) # TODO: replace with real exhibition location

ECC = {"GPS": 0.015, "Galileo": 0.000394, "GLONASS": 0.0015, "BeiDou": 0.006801}
NS_TO_M = c * 1e-9

ground_ecef = latlon_to_ecef(*STATION)

def load_systems():
    systems = {}
    with open(CSV_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["System"]
            alt_km = float(row["Altitude_km"])
            a = R_EARTH + alt_km * 1000
            period_s = 2 * np.pi * np.sqrt(a**3 / GM)
            systems[name] = {"alt_km": alt_km, "e": ECC[name], "net_us_per_day": float(row["Net_correction_us_per_day"]), "a": a, "period_s": period_s}
    return systems

SYSTEMS = load_systems()

def secular_range_m(system, sim_s):
    net = SYSTEMS[system]["net_us_per_day"]
    return c * net * 1e-6 * (sim_s / 86400)

def bounded_ns(system, sim_s):
    s = SYSTEMS[system]
    M = (2 * np.pi * sim_s / s["period_s"]) % (2 * np.pi)
    E = kepler_solver(M, s["e"])
    nu = true_anomaly(E, s["e"])
    r = satellite_distance(s["a"], s["e"], nu)
    ecc_ns = eccentricity_correction_ns(s["a"], s["e"], E, s["period_s"])
    earth_angle = 2 * np.pi * sim_s / 86400
    r_sat = satellite_position_ecef(r, nu - earth_angle)
    sagnac_ns = sagnac_correction_ns(r_sat, ground_ecef)
    return ecc_ns, sagnac_ns

def error_vector(system, mode, sim_s):
    secular_m = secular_range_m(system, sim_s)
    ecc_ns, sagnac_ns = bounded_ns(system, sim_s)
    bounded_m = (ecc_ns + sagnac_ns) * NS_TO_M
    if mode == "full":
        range_m = 0.0
    elif mode == "secular_only":
        range_m = bounded_m
    elif mode == "none":
        range_m = secular_m + bounded_m
    else:
        raise ValueError("Enter 'full', 'secular_only' or 'none'.")

    b = np.radians(BEARING_DEG)
    return {
        "range_m": range_m,
        "east_m": range_m * np.sin(b),
        "north_m": range_m * np.cos(b),
        "ecc_ns": ecc_ns,
        "sagnac_ns": sagnac_ns,
        "secular_m": secular_m
    }

if __name__ == "__main__":
    print(secular_range_m("GPS", 86400))
    for name in SYSTEMS:
        ts = range(0, 86401, 60)
        ecc = max(abs(bounded_ns(name, t)[0]) for t in ts)
        sag = max(abs(bounded_ns(name, t)[1]) for t in ts)
        print(f"{name:8s} max|ecc| = {ecc:6.2f} ns   max|sagnac| = {sag:6.2f} ns")
