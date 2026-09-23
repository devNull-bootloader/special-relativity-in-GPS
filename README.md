# Special Relativity in GPS

A compact project exploring why GPS satellite clocks require relativistic corrections, and how those corrections emerge from first-principles physics.

## Overview

GPS satellites experience two competing effects:

- **Special Relativity (SR):** orbital speed makes onboard clocks run slower.
- **General Relativity (GR):** weaker gravity at orbital altitude makes onboard clocks run faster.

For GPS, the net correction is about **+38.4 µs/day**. Without applying this correction, position error would grow by roughly **11.5 km per day**.

## Repository Status

This repository currently contains the project structure and source placeholders for derivations and simulations. The physics write-up and implementation scripts are being organized.

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── derivations/
│   ├── sr_derivation.py
│   ├── gr_derivation.py
│   └── null_altitude.py
├── simulations/
│   ├── altitude_curve.py
│   ├── gnss_comparison.py
│   └── animation.py
└── references/
    ├── JF2027_GPS_Einstein_ProjectPlan_Urvish.pdf
    ├── JF2027_JWST_ProjectPlan_Urvish.pdf
    ├── Jugend-Forscht 2026.pdf
    ├── Right Hand Rule.jpg
    └── Zur Elektrodynamik bewegter Körper.pdf
```

## Getting Started

```bash
git clone https://github.com/devNull-bootloader/special-relativity-in-GPS.git
cd special-relativity-in-GPS
```

When dependency requirements are finalized, install them with:

```bash
pip install -r requirements.txt
```

## Planned Work

- Implement SR, GR, and null-altitude derivation scripts.
- Add reproducible simulation outputs and plots.
- Add verification scripts and expected numeric results.
- Expand documentation with equations, assumptions, and data sources.

## References

Primary source materials and project planning documents are in `/references`.

## License

MIT License.
