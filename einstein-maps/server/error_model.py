import sys, os, csv
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "simulations"))
from simulations.bounded_utilities import (kepler_solver, true_anomaly, satellite_distance,
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

def secular_range_m(system, sim_s):
    """TODO: c * net_us_per_day * 1e-6 * (sim_s / 86400)"""

def bounded_ns(system, sim_s):
    """TODO: return (ecc_ns, sagnac_ns). Copy the loop body of bounded_effects_timeseries.py:
    M = 2*pi*sim_s/period % 2*pi -> kepler_solver -> true_anomaly -> r
    -> eccentricity_correction_ns -> earth_angle = 2*pi*sim_s/86400
    -> satellite_position_ecef(r, nu - earth_angle) -> sagnac_correction_ns"""

def error_vector(system, mode, sim_s):
    """TODO: mode in {"full", "secular_only", "none"}.
    full -> 0 | secular_only -> bounded only | none -> secular + bounded.
    bounded_m = (ecc_ns + sagnac_ns) * 0.299792458
    Return dict with range_m, east_m, north_m, ecc_ns, sagnac_ns, secular_m.
    east = range*sin(bearing), north = range*cos(bearing)"""

if __name__ == "__main__":
    # TODO: sanity checks against paper:
    # GPS secular at 86400 s ≈ 11540 m; max |ecc| ≈ 34 ns; max |sagnac| ≈ 83 ns
    pass
