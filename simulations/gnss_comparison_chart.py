import csv, os
import numpy as np
import matplotlib.pyplot as plt

# GNSS constellation data (altitude_km, SR_us_per_day, GR_us_per_day, net_us_per_day)
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(script_dir, "..", "data", "gnss_orbital_parameters.csv"))

gnss_systems = {}
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gnss_systems[row['System']] = (
            int(row['Altitude_km']),
            float(row['SR_correction_us_per_day']),
            float(row['GR_correction_us_per_day']),
            float(row['Net_correction_us_per_day'])
        )


# Data for plotting
systems = list(gnss_systems.keys())
SR_corrections = [gnss_systems[sys][1] for sys in systems]
GR_corrections = [gnss_systems[sys][2] for sys in systems]
net_corrections = [gnss_systems[sys][3] for sys in systems]

# Bar chart setup
x = np.arange(len(systems))
bar_width = 0.25

# Create figure
plt.figure(figsize=(12, 7))

# Plot bars
bars_SR = plt.bar(x - bar_width, SR_corrections, bar_width, label='SR (Special Relativity)', color='red', alpha=0.8)
bars_GR = plt.bar(x,            GR_corrections, bar_width, label='GR (General Relativity)', color='blue', alpha=0.8)
bars_net = plt.bar(x + bar_width, net_corrections, bar_width, label='Net Correction', color='green', alpha=0.8)

# Value labels on net bars
for i, (bar, value) in enumerate(zip(bars_net, net_corrections)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{value:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Value labels on SR bars
for bar, value in zip(bars_SR, SR_corrections):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 1.5,
             f'{value:.1f}', ha='center', va='top', fontsize=8)

# Value labels on GR bars
for bar, value in zip(bars_GR, GR_corrections):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 1.5,
             f'{value:.1f}', ha='center', va='top', fontsize=8, color='white')

# Formatting
plt.xlabel('GNSS Constellation', fontsize=12, fontweight='bold')
plt.ylabel('Clock Correction (μs/day)', fontsize=12, fontweight='bold')
plt.title('Relativistic Clock Corrections: GNSS Constellation Comparison', fontsize=14, fontweight='bold')
plt.xticks(x, systems, fontsize=11)
plt.grid(True, axis='y', alpha=0.3, linestyle='--')
plt.axhline(y=0, color='black', linewidth=0.8)
plt.legend(fontsize=11, loc='upper left')
plt.ylim(-15, 55)
plt.tight_layout()

# Save
output_path = 'plots/gnss_comparison_chart.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved: {output_path}")

plt.show()
