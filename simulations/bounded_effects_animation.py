import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import os
from bounded_utilities import *

# Constants
SIM_HOURS = 24
FRAMES = 240
TIME_STEP_HOURS = SIM_HOURS / FRAMES
EARTH_ROTATION_PER_FRAME = 2 * np.pi / FRAMES

# Satellite data
SATELLITES = [
    ("GPS",     20200, 0.015,  "#44ff44"),
    ("Galileo", 23222, 0.000394,  "#44aaff"),
    ("GLONASS", 19100, 0.0015, "#ff4444"),
    ("BeiDou",  21528, 0.006801,  "#aa44ff"),
]

# Ground station
GROUND_LAT = 53.1
GROUND_LON = 8.8
GROUND_ALT = 10
ground_ecef = latlon_to_ecef(GROUND_LAT, GROUND_LON, GROUND_ALT)

# Pre-compute satellite orbital parameters
sat_data = []
for name, alt_km, e, color in SATELLITES:
    r_orbit_m = R_EARTH + alt_km * 1000
    a = r_orbit_m
    period_s = 2 * np.pi * np.sqrt(a**3 / GM)
    period_h = period_s / 3600
    angular_velocity = 2 * np.pi / period_s
    
    sat_data.append({
        "name": name,
        "alt_km": alt_km,
        "a": a,
        "e": e,
        "period_s": period_s,
        "period_h": period_h,
        "angular_velocity": angular_velocity,
        "color": color,
        "radius_km": r_orbit_m / 1000,
    })

# Pre-compute frame data
frame_data = []
for frame in range(FRAMES):
    elapsed_hours = frame * TIME_STEP_HOURS
    elapsed_s = elapsed_hours * 3600
    earth_angle = frame * EARTH_ROTATION_PER_FRAME
    
    sat_positions = []
    for sat in sat_data:
        # Mean anomaly
        M = (2 * np.pi * elapsed_s) / sat["period_s"]
        M = M % (2 * np.pi)
        
        # Solve Kepler
        E = kepler_solver(M, sat["e"])
        nu = true_anomaly(E, sat["e"])
        
        # Orbital position
        r = satellite_distance(sat["a"], sat["e"], nu)
        v = satellite_velocity(sat["a"], sat["e"], nu)
        
        # Position in orbital plane
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        z_orb = 0
        
        # Convert for visualization
        x_sat = (r / 1000) * np.cos(nu)
        y_sat = (r / 1000) * np.sin(nu)
        
        # Orientation toward Earth
        orient_length = sat["radius_km"] * 0.12
        x_toward = x_sat - orient_length * np.cos(nu)
        y_toward = y_sat - orient_length * np.sin(nu)
        
        # Bounded corrections
        ecc_corr = eccentricity_correction_ns(sat["a"], sat["e"], E, sat["period_s"])
        r_sat_ecef = satellite_position_ecef(r, nu - earth_angle)
        sagnac_corr = sagnac_correction_ns(r_sat_ecef, ground_ecef)
        bounded_total = ecc_corr + sagnac_corr
        
        # Position error from bounded effects
        # 1 ns ≈ 0.3 meters ≈ 0.0003 km
        position_error_km = bounded_total * 0.0003
        
        sat_positions.append({
            "x": x_sat,
            "y": y_sat,
            "x_toward": x_toward,
            "y_toward": y_toward,
            "ecc": ecc_corr,
            "sagnac": sagnac_corr,
            "bounded_total": bounded_total,
            "position_error_km": position_error_km,
        })
    
    frame_data.append({
        "earth_angle": earth_angle,
        "sat_positions": sat_positions,
    })

# Figure setup
fig, ax = plt.subplots(figsize=(16, 14))
ax.set_aspect('equal')
ax.set_xlim(-50000, 50000)
ax.set_ylim(-50000, 50000)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlabel('Distance (km)', fontsize=12, fontweight='bold')
ax.set_ylabel('Distance (km)', fontsize=12, fontweight='bold')
ax.set_title('Bounded Effects (Eccentricity + Sagnac) Animation: 24 Hours', 
             fontsize=14, fontweight='bold')

# Earth
earth_circle = patches.Circle((0, 0), R_EARTH / 1000, 
                               facecolor='#2a7f2a', edgecolor='#1a5f1a', 
                               linewidth=2, zorder=10, alpha=0.9)
ax.add_patch(earth_circle)

earth_rotation_line, = ax.plot([0, R_EARTH/1000], [0, 0], 'w-', linewidth=3, zorder=11)

# Ground station, shown in the inertial visualization frame
ground_marker, = ax.plot([ground_ecef[0]/1000], [ground_ecef[1]/1000], 'rx', 
                         markersize=15, markeredgewidth=3, zorder=12, label='Ground Station (Bremen)')

# Orbital tracks
theta_orbit = np.linspace(0, 2*np.pi, 400)
label_angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
for i, sat in enumerate(sat_data):
    r_km = sat["radius_km"]
    x_orbit = r_km * np.cos(theta_orbit)
    y_orbit = r_km * np.sin(theta_orbit)
    ax.plot(x_orbit, y_orbit, '-', color=sat["color"], 
            linewidth=1.5, alpha=0.5, zorder=2)
    
    label_angle = label_angles[i]
    label_x = r_km * np.cos(label_angle)
    label_y = r_km * np.sin(label_angle)
    ax.text(label_x, label_y, f'{sat["name"]}\n({sat["alt_km"]} km)', 
            color=sat["color"], fontsize=8, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                      edgecolor=sat["color"], alpha=0.7),
            zorder=5)

# Satellites
sat_dots = []
sat_orientation_lines = []
for sat in sat_data:
    dot, = ax.plot([], [], 'o', color=sat["color"], markersize=10, 
                   markeredgecolor='white', markeredgewidth=1.5, zorder=15)
    sat_dots.append(dot)
    
    orient_line, = ax.plot([], [], '-', color=sat["color"], linewidth=2, zorder=14)
    sat_orientation_lines.append(orient_line)

# Correction boxes
corr_texts = []
text_x = 48000
text_y_start = 45000
text_y_step = -9000
for i, sat in enumerate(sat_data):
    y_pos = text_y_start + i * text_y_step
    txt = ax.text(text_x, y_pos, '', fontsize=9, fontweight='bold',
                  ha='right', va='center',
                  bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                            edgecolor=sat["color"], linewidth=2, alpha=0.85),
                  zorder=20)
    corr_texts.append(txt)



# Legend
legend_elements = []
for sat in sat_data:
    legend_elements.append(plt.Line2D([0], [0], color=sat["color"], lw=3, 
                                    label=f'{sat["name"]} (e={sat["e"]:.4f})'))
legend_elements.append(plt.Line2D([0], [0], marker='x', color='w', 
                                 markerfacecolor='r', markersize=10, label='Ground Station'))

ax.legend(handles=legend_elements, fontsize=10, loc='lower left', 
          framealpha=0.9, edgecolor='gray', title='Satellites & Ground',
          title_fontsize=11)

# Animation function
def animate(frame):
    frame_info = frame_data[frame]
    
    # Earth rotation
    earth_angle = frame_info["earth_angle"]
    earth_rotation_line.set_data(
        [0, (R_EARTH/1000) * np.cos(earth_angle)],
        [0, (R_EARTH/1000) * np.sin(earth_angle)]
    )

    ground_marker.set_data(
        [(ground_ecef[0] * np.cos(earth_angle) - ground_ecef[1] * np.sin(earth_angle)) / 1000],
        [(ground_ecef[0] * np.sin(earth_angle) + ground_ecef[1] * np.cos(earth_angle)) / 1000]
    )
    
    artists = [earth_rotation_line, ground_marker]
    
    # Satellites
    for i, (sat, pos_info) in enumerate(zip(sat_data, frame_info["sat_positions"])):
        sat_dots[i].set_data([pos_info["x"]], [pos_info["y"]])
        artists.append(sat_dots[i])
        
        sat_orientation_lines[i].set_data(
            [pos_info["x"], pos_info["x_toward"]],
            [pos_info["y"], pos_info["y_toward"]]
        )
        artists.append(sat_orientation_lines[i])
        
        # Correction text
        bounded = pos_info["bounded_total"]
        ecc = pos_info["ecc"]
        sagnac = pos_info["sagnac"]
        
        if bounded >= 0:
            color = "green"
            status = "ahead"
        else:
            color = "red"
            status = "behind"
        
        corr_texts[i].set_text(
            f'{sat["name"]}\nBounded: {bounded:+.0f} ns\n'
            f'(ecc: {ecc:+.0f} | sag: {sagnac:+.0f})'
        )
        corr_texts[i].set_color(color)
        artists.append(corr_texts[i])
    
    return artists

# Animation
anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=100, 
                               blit=True, repeat=True, repeat_delay=2000)

# Save
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, 'bounded_effects_animation.mp4')
writer = animation.FFMpegWriter(fps=10, bitrate=2000)
anim.save(output_path, writer=writer)
print(f"Animation saved: {output_path}")

plt.show()