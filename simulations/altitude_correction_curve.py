import numpy as np
import matplotlib.pyplot as plt
import os

# Constants
G = 6.674e-11      # Gravitational constant
M_E = 5.972e24     # Earth mass
c = 3e8            # Speed of light
R_E = 6.371e6      # Earth radius
GM = 3.986e14      # GM product

# Altitude range
altitude_km = np.linspace(0, 40000, 1000)
r = altitude_km * 1000 + R_E

# Orbital velocity at each altitude
v = np.sqrt(GM / r)

# Special Relativity correction (in μs/day)
SR_correction = -(v**2 / (2 * c**2)) * 86400 * 1e6

# General Relativity correction (in μs/day)
GR_correction = (GM / c**2) * (1/R_E - 1/r) * 86400 * 1e6

# Net correction
net_correction = SR_correction + GR_correction

# Plot
plt.figure(figsize=(12, 7))
plt.plot(altitude_km, SR_correction, 'r-', linewidth=2, label='SR (Special Relativity)')
plt.plot(altitude_km, GR_correction, 'b-', linewidth=2, label='GR (General Relativity)')
plt.plot(altitude_km, net_correction, 'g-', linewidth=2.5, label='Net Correction')

# Null-point
null_altitude = (3/2 * R_E - R_E) / 1000  # Convert to km
plt.axvline(null_altitude, color='gray', linestyle='--', linewidth=1.5, label=f'Null altitude ({null_altitude:.0f} km)')

# GNSS markers
gnss_systems = [
    ('GPS', 20200, 38.4),
    ('Galileo', 23222, 40.7),
    ('GLONASS', 19100, 37.5),
    ('BeiDou', 21528, 39.5),
]

for name, alt, corr in gnss_systems:
    plt.plot(alt, corr, 'ko', markersize=8)
    plt.annotate(name, (alt, corr), xytext=(5, 10), textcoords='offset points', fontsize=9)

# Labels and formatting
plt.xlabel('Altitude (km)', fontsize=12)
plt.ylabel('Clock Correction (μs/day)', fontsize=12)
plt.title('Relativistic Clock Corrections for GNSS Satellites', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11, loc='best')
plt.xlim(0, 40000)
plt.ylim(-30, 60)
plt.tight_layout()

# Save
if not os.path.exists('plots/altitude_vs_correction.png'):
    plt.savefig('plots/altitude_vs_correction.png', dpi=300, bbox_inches='tight')
    print("Plot saved: plots/altitude_vs_correction.png")

plt.show()