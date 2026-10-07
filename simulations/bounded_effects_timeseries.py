import numpy as np
import matplotlib.pyplot as plt
import os
from bounded_utilities import *

# Satellite constellations: (name, altitude_km, eccentricity, color)
SATELLITES = [
    ("GPS",     20200, 0.015,  "#44ff44"),
    ("Galileo", 23222, 0.000394,  "#44aaff"),
    ("GLONASS", 19100, 0.0015, "#ff4444"),
    ("BeiDou",  21528, 0.006801, "#aa44ff"),
]

# Ground station: Bremen, Germany
GROUND_LAT = 53.1
GROUND_LON = 8.8
GROUND_ALT = 10
ground_ecef = latlon_to_ecef(GROUND_LAT, GROUND_LON, GROUND_ALT)

# Pre-compute satellite data
sat_data = []
for name, alt_km, e, color in SATELLITES:
    r_orbit_m = (R_EARTH + alt_km * 1000)
    a = r_orbit_m
    period_s = 2 * np.pi * np.sqrt(a**3 / GM)
    period_h = period_s / 3600
    
    sat_data.append({
        "name": name,
        "alt_km": alt_km,
        "a": a,
        "e": e,
        "period_s": period_s,
        "period_h": period_h,
        "color": color,
    })

# Time array: 24 hours
hours = np.linspace(0, 24, 1440)  # 1 minute resolution
times_s = hours * 3600

# Pre-compute all corrections
corrections = {sat["name"]: {"ecc": [], "sagnac": [], "total": []} for sat in sat_data}

for sat in sat_data:
    for t in times_s:
        # Mean anomaly from time (starting at t=0 with M=0)
        M = (2 * np.pi * t) / sat["period_s"]
        M = M % (2 * np.pi)  # Keep in [0, 2*pi]
        
        # Solve Kepler's equation
        E = kepler_solver(M, sat["e"])
        
        # True anomaly
        nu = true_anomaly(E, sat["e"])
        
        # Orbital radius and velocity
        r = satellite_distance(sat["a"], sat["e"], nu)
        v = satellite_velocity(sat["a"], sat["e"], nu)
        
        # Eccentricity correction (nanoseconds)
        ecc_corr = eccentricity_correction_ns(sat["a"], sat["e"], E, sat["period_s"])
        
        # Sagnac uses both positions in the Earth-fixed frame.
        earth_angle = 2 * np.pi * t / (24 * 3600)
        r_sat_ecef = satellite_position_ecef(r, nu - earth_angle)
        sagnac_corr = sagnac_correction_ns(r_sat_ecef, ground_ecef)
        
        # Total bounded correction
        total_bounded = ecc_corr + sagnac_corr
        
        corrections[sat["name"]]["ecc"].append(ecc_corr)
        corrections[sat["name"]]["sagnac"].append(sagnac_corr)
        corrections[sat["name"]]["total"].append(total_bounded)

# Plot
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Bounded Effects (Eccentricity + Sagnac): 24-Hour GNSS Corrections', 
             fontsize=16, fontweight='bold')

for idx, sat in enumerate(sat_data):
    ax = axes[idx // 2, idx % 2]
    
    ax.plot(hours, corrections[sat["name"]]["ecc"], 'r-', linewidth=1.5, 
            label=f'Eccentricity', alpha=0.7)
    ax.plot(hours, corrections[sat["name"]]["sagnac"], 'b-', linewidth=1.5, 
            label=f'Sagnac', alpha=0.7)
    ax.plot(hours, corrections[sat["name"]]["total"], 'g-', linewidth=2, 
            label=f'Total Bounded', alpha=0.9)
    
    ax.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Time (hours)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Correction (nanoseconds)', fontsize=11, fontweight='bold')
    ax.set_title(f'{sat["name"]} (e={sat["e"]:.4f}, period={sat["period_h"]:.1f} h)', 
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.set_xlim(0, 24)

plt.tight_layout()

# Save
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, 'bounded_effects_timeseries.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved: {output_path}")

plt.show()
