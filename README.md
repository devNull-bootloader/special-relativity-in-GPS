# Special Relativity in GPS

A compact project exploring why GPS satellite clocks require relativistic corrections, and how those corrections emerge from first-principles physics.

## Overview

GPS satellites experience two competing effects:

- **Special Relativity (SR):** orbital speed makes onboard clocks run slower.
- **General Relativity (GR):** weaker gravity at orbital altitude makes onboard clocks run faster.

For GPS, the net correction is about **+38.5 µs/day**. Without applying this correction, position error would grow by roughly **11.5 km per day**.

## Repository Status

The core derivation and simulation scripts are implemented. The repository includes a Typst physics write-up, reproducible Python calculations, GNSS orbital data, and generated plots and animations.

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   └── gnss_orbital_parameters.csv
├── derivations/
│   ├── derivations.typ
│   └── derivations.pdf
├── outputs/
│   ├── gps_derivation.txt
│   ├── bounded_effects_timeseries.png
│   ├── bounded_effects_animation.mp4
│   ├── multi_orbit_time_dilation.mp4
│   └── position_error_animation.mp4
├── plots/
│   ├── altitude_vs_correction.png
│   └── gnss_comparison_chart.png
├── simulations/
│   ├── altitude_correction_curve.py
│   ├── bounded_effects_animation.py
│   ├── bounded_effects_timeseries.py
│   ├── bounded_utilities.py
│   ├── gnss_comparison_chart.py
│   ├── gps_derivation_printout.py
│   ├── multi_orbit_time_dilation.py
│   └── position_error_animation.py
└── references/
    └── project references and source material
```

## Getting Started

```bash
git clone https://github.com/devNull-bootloader/special-relativity-in-GPS.git
cd special-relativity-in-GPS
```

Install the Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

The simulation scripts can be run directly from the repository root, for example:

```bash
python simulations/altitude_correction_curve.py
python simulations/gnss_comparison_chart.py
```

The derivation document is `derivations/derivations.typ` and can be exported with Typst or Tinymist.

## Next Steps

- Refine the derivation and simulation documentation.
- Add verification scripts and expected numeric results.
- Compare additional GNSS constellations and orbital parameters.

## References

Primary source materials and project planning documents are in `/references`.

## License

MIT License.
