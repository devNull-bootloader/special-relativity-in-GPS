import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Constants
c = 3e8                    # Speed of light
net_correction_us = 38.4   # GPS net correction
position_error_per_day_km = 11.5  # km/day without correction

# Animation parameters
total_hours = 24
frames = 24
time_step = 1

# Time array
time_hours = np.arange(frames) * time_step

# Position traces
corrected_distance = np.zeros(frames)  # Blue trace: stays at origin (with tiny jitter)
uncorrected_distance = position_error_per_day_km / 24 * time_hours  # Red trace: linear drift

# Tiny random jitter for realism
np.random.seed(42)
corrected_distance += np.random.normal(0, 0.001, frames)  # ±1 meter jitter

# Figure and axis
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(-1, 13)
ax.set_ylim(-1, 13)
ax.set_aspect('equal')

# Grid and labels
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlabel('Distance East (km)', fontsize=12, fontweight='bold')
ax.set_ylabel('Distance North (km)', fontsize=12, fontweight='bold')
ax.set_title('GPS Position Error Accumulation Over 24 Hours (Without Relativistic Correction)', 
             fontsize=14, fontweight='bold')

# Origin marker
ax.plot(0, 0, 'g*', markersize=20, label='True Position', zorder=5)

# Initialize line objects
line_corrected, = ax.plot([], [], 'b-', linewidth=2.5, label='Corrected GPS (with Einstein)', zorder=3)
line_uncorrected, = ax.plot([], [], 'r-', linewidth=2.5, label='Uncorrected GPS (without Einstein)', zorder=2)

# Initialize scatter points
scatter_corrected, = ax.plot([], [], 'bo', markersize=8, zorder=4)
scatter_uncorrected, = ax.plot([], [], 'ro', markersize=8, zorder=4)

# Text annotations
time_text = ax.text(0.98, 0.98, '', transform=ax.transAxes, 
                    fontsize=12, verticalalignment='top', horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
error_text = ax.text(0.98, 0.88, '', transform=ax.transAxes,
                     fontsize=12, verticalalignment='top', horizontalalignment='right',
                     bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8),
                     fontweight='bold')

ax.legend(fontsize=11, loc='upper left')

# Animation function
def animate(frame):
    # Update traces
    x_corrected = corrected_distance[:frame+1]
    y_corrected = np.zeros(frame+1)
    
    x_uncorrected = uncorrected_distance[:frame+1]
    y_uncorrected = np.zeros(frame+1)
    
    # Update lines
    line_corrected.set_data(x_corrected, y_corrected)
    line_uncorrected.set_data(x_uncorrected, y_uncorrected)
    
    # Update current positions
    scatter_corrected.set_data([x_corrected[-1]], [y_corrected[-1]])
    scatter_uncorrected.set_data([x_uncorrected[-1]], [y_uncorrected[-1]])
    
    # Update time label
    time_text.set_text(f'Elapsed Time: {frame} hours')
    
    # Update error label
    error_distance = uncorrected_distance[frame]
    if error_distance > 0.1:
        error_text.set_text(f'Position Error: {error_distance:.2f} km')
    else:
        error_text.set_text(f'Position Error: ~0 km')
    
    return line_corrected, line_uncorrected, scatter_corrected, scatter_uncorrected, time_text, error_text

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=frames, interval=200, 
                              blit=True, repeat=True, repeat_delay=2000)

# Save animation
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, 'position_error_animation.mp4')
if not os.path.exists(output_path):
    writer = animation.FFMpegWriter(fps=5, bitrate=1800)
    anim.save(output_path, writer=writer)
    print(f"Animation saved: {output_path}")
else:
    print(f"Animation already exists: {output_path}")

plt.show()