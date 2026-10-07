import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import os

# Constants
GM = 3.986e14              # Earth GM product [m^3/s^2]
R_EARTH = 6.371e6          # Earth radius [m]
SIM_HOURS = 24
FRAMES = 240                # 0.1 hour per frame
TIME_STEP_HOURS = SIM_HOURS / FRAMES
EARTH_ROTATION_PER_FRAME = 2 * np.pi / FRAMES

# Satellite data: (name, altitude_km, orbital_radius_m, dilation_us_per_day, color)
SATELLITES = [
    ("ISS",           400,    6.771e6,   -25.4,  "#ff4444"),
    ("Null-altitude", 3186,   9.557e6,    0.0,   "#ffaa00"),
    ("GPS",           20200,  26.57e6,   +38.5,  "#44ff44"),
    ("Galileo",       23222,  29.6e6,    +40.7,  "#44aaff"),
    ("Geostationary", 35786,  42.164e6,  +45.8,  "#aa44ff"),
]

# Pre-compute orbital parameters
sat_data = []
for name, alt_km, r_m, dilation, color in SATELLITES:
    period_seconds = 2 * np.pi * np.sqrt(r_m**3 / GM)
    period_hours = period_seconds / 3600
    angular_velocity = 2 * np.pi / period_seconds
    sat_data.append({
        "name": name,
        "alt_km": alt_km,
        "radius_m": r_m,
        "radius_km": r_m / 1000,
        "dilation_us_per_day": dilation,
        "color": color,
        "period_hours": period_hours,
        "angular_velocity": angular_velocity,
    })

# Pre-compute all frame positions and dilations
frame_data = []
for frame in range(FRAMES):
    elapsed_hours = frame * TIME_STEP_HOURS
    elapsed_seconds = elapsed_hours * 3600
    earth_angle = frame * EARTH_ROTATION_PER_FRAME
    
    sat_positions = []
    for sat in sat_data:
        angle = sat["angular_velocity"] * elapsed_seconds
        x_sat = sat["radius_km"] * np.cos(angle)
        y_sat = sat["radius_km"] * np.sin(angle)
        
        orient_length = sat["radius_km"] * 0.12
        x_toward_earth = x_sat - orient_length * np.cos(angle)
        y_toward_earth = y_sat - orient_length * np.sin(angle)
        
        cumulative_dilation = sat["dilation_us_per_day"] * (elapsed_hours / SIM_HOURS)
        
        sat_positions.append({
            "x": x_sat,
            "y": y_sat,
            "x_toward": x_toward_earth,
            "y_toward": y_toward_earth,
            "dilation": cumulative_dilation,
        })
    
    frame_data.append({
        "earth_angle": earth_angle,
        "sat_positions": sat_positions,
    })

# Figure setup
fig, ax = plt.subplots(figsize=(14, 12))
ax.set_aspect('equal')
ax.set_xlim(-50000, 50000)
ax.set_ylim(-50000, 50000)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlabel('Distance (km)', fontsize=12, fontweight='bold')
ax.set_ylabel('Distance (km)', fontsize=12, fontweight='bold')
ax.set_title('Multi-Orbit Time Dilation Visualization: 24-Hour Accumulation', 
             fontsize=14, fontweight='bold')

# Earth
earth_circle = patches.Circle((0, 0), R_EARTH / 1000, 
                               facecolor='#2a7f2a', edgecolor='#1a5f1a', 
                               linewidth=2, zorder=10, alpha=0.9)
ax.add_patch(earth_circle)


earth_rotation_line, = ax.plot([0, R_EARTH/1000], [0, 0], 'w-', linewidth=3, zorder=11)

# Orbital tracks
theta_orbit = np.linspace(0, 2*np.pi, 400)
label_angles = np.linspace(np.pi/4, 2*np.pi + np.pi/4, len(sat_data), endpoint=False)
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

# Clock counters
clock_texts = []
text_x = 48000
text_y_start = 40000
text_y_step = -8500
for i, sat in enumerate(sat_data):
    y_pos = text_y_start + i * text_y_step
    txt = ax.text(text_x, y_pos, '', fontsize=10, fontweight='bold',
                  ha='right', va='center',
                  bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                            edgecolor=sat["color"], linewidth=2, alpha=0.85),
                  zorder=20)
    clock_texts.append(txt)


# Legend
legend_elements = []
for sat in sat_data:
    sign = "+" if sat["dilation_us_per_day"] >= 0 else ""
    label = f'{sat["name"]}: {sign}{sat["dilation_us_per_day"]:.1f} μs/day'
    legend_elements.append(plt.Line2D([0], [0], color=sat["color"], lw=3, label=label))

ax.legend(handles=legend_elements, fontsize=9, loc='lower left', 
          framealpha=0.9, edgecolor='gray', title='Time Dilation Rates',
          title_fontsize=10)

# Animation function
def animate(frame):
    frame_info = frame_data[frame]
    
    earth_angle = frame_info["earth_angle"]
    earth_rotation_line.set_data(
        [0, (R_EARTH/1000) * np.cos(earth_angle)],
        [0, (R_EARTH/1000) * np.sin(earth_angle)]
    )
    
    artists = [earth_rotation_line]
    
    for i, (sat, pos_info) in enumerate(zip(sat_data, frame_info["sat_positions"])):
        sat_dots[i].set_data([pos_info["x"]], [pos_info["y"]])
        artists.append(sat_dots[i])
        
        sat_orientation_lines[i].set_data(
            [pos_info["x"], pos_info["x_toward"]],
            [pos_info["y"], pos_info["y_toward"]]
        )
        artists.append(sat_orientation_lines[i])
        
        cumulative_dilation = pos_info["dilation"]
        
        if cumulative_dilation >= 0:
            status = "FAST"
            color = "green"
        else:
            status = "SLOW"
            color = "red"
        
        sign = "+" if cumulative_dilation >= 0 else ""
        clock_texts[i].set_text(
            f'{sat["name"]}\n{sign}{cumulative_dilation:.2f} μs {status}'
        )
        clock_texts[i].set_color(color)
        artists.append(clock_texts[i])
    
    return artists

# Create and save animation
anim = animation.FuncAnimation(fig, animate, frames=FRAMES, interval=100, 
                               blit=True, repeat=True, repeat_delay=2000)

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, 'multi_orbit_time_dilation.mp4')
if not os.path.exists(output_path):
    writer = animation.FFMpegWriter(fps=10, bitrate=2000)
    anim.save(output_path, writer=writer)
    print(f"Animation saved: {output_path}")
else:
    print(f"Animation already exists: {output_path}")

plt.show()