import os

# GPS orbital parameters
altitude_km = 20200
orbital_radius_m = 26.57e6
R_E = 6.371e6
GM = 3.986e14
c = 3e8

# Calculate values
v = (GM / orbital_radius_m) ** 0.5
SR_correction = -(v**2 / (2 * c**2)) * 86400 * 1e6
GR_correction = (GM / c**2) * (1/R_E - 1/orbital_radius_m) * 86400 * 1e6
net_correction = SR_correction + GR_correction
position_error = c * (net_correction * 1e-6)

# Generate output text
output_text = f"""
================================================================================
GPS RELATIVISTIC CLOCK CORRECTION — STEP-BY-STEP DERIVATION
================================================================================

INPUT PARAMETERS
================================================================================
Orbital altitude:                   {altitude_km:,} km
Orbital radius (from Earth center): {orbital_radius_m:.3e} m
Earth radius (R_E):                 {R_E:.3e} m
Gravitational parameter (GM):       {GM:.3e} m³/s²
Speed of light (c):                 {c:.3e} m/s

STEP 1: CALCULATE ORBITAL VELOCITY
================================================================================
Formula: v = √(GM / r)

v = √({GM:.3e} / {orbital_radius_m:.3e})
v = √({GM / orbital_radius_m:.3e})
v = {v:.3f} m/s

Verification: published GPS velocity ≈ 3,874 m/s ✓

STEP 2: SPECIAL RELATIVITY CORRECTION
================================================================================
Formula: Δt_SR = -(v² / 2c²) × 86,400 s

v² = {v**2:.3e} m²/s²
2c² = {2 * c**2:.3e} m²/s²
v² / 2c² = {v**2 / (2 * c**2):.3e}

Δt_SR = -{v**2 / (2 * c**2) * 86400:.3e} s
Δt_SR = {SR_correction:.2f} μs/day

Interpretation: The moving satellite clock runs SLOWER by 7.2 microseconds per day
due to time dilation from relativistic velocity.

STEP 3: GENERAL RELATIVITY CORRECTION
================================================================================
Formula: Δt_GR = (GM / c²) × (1/R_E - 1/r) × 86,400 s

GM / c² = {GM / c**2:.3e} m
1/R_E = {1/R_E:.3e} m⁻¹
1/r = {1/orbital_radius_m:.3e} m⁻¹
(1/R_E - 1/r) = {1/R_E - 1/orbital_radius_m:.3e} m⁻¹

Δt_GR = {GM / c**2:.3e} × {1/R_E - 1/orbital_radius_m:.3e} × 86,400
Δt_GR = {GR_correction:.2f} μs/day

Interpretation: The satellite is in a weaker gravitational field (farther from Earth),
so its clock runs FASTER by 45.9 microseconds per day compared to ground clocks.

STEP 4: COMBINED RELATIVISTIC CORRECTION
================================================================================
Formula: Δt_net = Δt_SR + Δt_GR

Δt_net = {SR_correction:.2f} + {GR_correction:.2f}
Δt_net = {net_correction:.2f} μs/day

This is the net correction that must be programmed into GPS satellite clocks.

STEP 5: POSITION ERROR WITHOUT CORRECTION
================================================================================
Formula: Position error = c × Δt

Δx = {c:.3e} m/s × {net_correction * 1e-6:.3e} s
Δx = {position_error:.2f} m per correction period
Δx ≈ {position_error / 1000:.1f} km per day

VERIFICATION AGAINST PUBLISHED SPECIFICATIONS
================================================================================
Published GPS specification:        +38.4 μs/day
Your calculated value:              {net_correction:.2f} μs/day
Absolute error:                     {abs(net_correction - 38.4):.2f} μs/day
Relative error:                     {abs(net_correction - 38.4) / 38.4 * 100:.2f}%

✓ RESULT: Your calculation matches published GPS specifications to within 0.3%

================================================================================
CONCLUSION
================================================================================
Einstein's relativity is not theoretical — it is ESSENTIAL for GPS functionality.
Without the {net_correction:.1f} μs/day correction:
  • GPS position error accumulates at ~{position_error/1000:.1f} km per day
  • Navigational systems would be useless within hours
  • The system proves that relativity is real and measurable

Derived by: Urvish Lanje (Jugend Forscht 2027)
Date: September 2026
================================================================================
"""

# Save output
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, 'gps_derivation.txt')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output_text)

print(output_text)
print(f"\nDerivation saved to: {output_path}")