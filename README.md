# Special Relativity in GPS

What happens to GPS if you leave Einstein out? This project works out why satellite clocks need relativistic corrections, derives them from scratch, and simulates what goes wrong without them.

## TL;DR

A GPS satellite clock is pulled in two directions at once:

- Special relativity: the satellite moves fast (about 3.9 km/s), so its clock runs slower.
- General relativity: gravity is weaker up there, so its clock runs faster.

Gravity is stronger. For GPS the net effect is roughly +38.5 µs per day. That sounds tiny, but a clock error of 38.5 µs is a range error of about 11.5 km, and it grows every day. Without the correction, GPS would be useless within hours.

I also look at Galileo, GLONASS and BeiDou, and at the smaller effects that don't pile up over time: the satellite's slightly elliptical orbit (up to about 34 ns for GPS) and the Sagnac effect from the Earth's rotation (about 83 ns for a receiver in Bremen).

## What's in here

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── Important Project Pivot.md
├── data/
│   └── gnss_orbital_parameters.csv
├── derivations/
│   ├── derivations.typ      full derivations (SR, GR, null altitude, bounded effects)
│   ├── appendices.typ       orbital mechanics, constellation data, simulation methods
│   ├── paper.typ            the written project report
│   └── derivations.pdf
├── outputs/                 generated text and animations
├── plots/                   generated figures
├── simulations/
│   ├── altitude_correction_curve.py
│   ├── bounded_effects_animation.py
│   ├── bounded_effects_timeseries.py
│   ├── bounded_utilities.py
│   ├── gnss_comparison_chart.py
│   ├── gps_derivation_printout.py
│   ├── multi_orbit_time_dilation.py
│   └── position_error_animation.py
├── einstein-maps/           the interactive demo (see below)
│   ├── server/
│   │   ├── error_model.py
│   │   └── app.py
│   └── web/
│       ├── index.html
│       ├── app.js
│       └── style.css
└── references/              source material
```

## Running it

```bash
git clone https://github.com/devNull-bootloader/special-relativity-in-GPS.git
cd special-relativity-in-GPS
python -m pip install -r requirements.txt
```

Every script runs from the repository root, for example:

```bash
python simulations/altitude_correction_curve.py
python simulations/gnss_comparison_chart.py
```

The derivations are written in Typst. Open them with Tinymist in VS Code or compile with the Typst CLI.

## Einstein-Maps

A small navigation app for showing the problem to people. You type in a destination and it gives you a route, but the starting point is wrong by exactly the amount the relativistic clock error would cause. You can switch between GPS, Galileo, GLONASS and BeiDou, and between three modes:

- Voll: all corrections applied, no error.
- Nur säkular: only the small bounded effects are left (tens of meters).
- Keine: no correction at all, and the error climbs towards 11.5 km.

Start it with:

```bash
python einstein-maps/server/app.py
```

Then open `http://localhost:5000`.

Some notes on what is real and what is simplified:

- The physics comes straight from the simulation code in this repo. The road network, geocoding and routing come from OpenStreetMap (Nominatim and OSRM).
- Time is sped up so that 1 second is 10 minutes. Otherwise nobody would see an error that grows over a day.
- The real error is a range error for one satellite. The app turns it into a position offset in a fixed direction (45°). A real receiver would combine several satellites and absorb part of this in its own clock.
- The eccentricities are model values, not taken from broadcast ephemerides. Real satellites differ from each other.

## Checking my numbers

My result for the average clock shift is 38.51 µs/day. Ashby (2003) gives 38.57 µs/day, so I'm about 0.2 % off. The gap comes from using a perfectly spherical Earth, which ignores the quadrupole moment and the rotation of the ground clock. The derivations and the paper explain this in more detail.

## Still to do

- Add verification scripts with expected numeric results.
- Compare more orbital parameters and, ideally, real ephemeris data.

## (heavily used) Reference

Ashby, N. (2003). Relativity in the Global Positioning System. Living Reviews in Relativity 6, 1. https://doi.org/10.12942/lrr-2003-1

## License

MIT. See `LICENSE`.
