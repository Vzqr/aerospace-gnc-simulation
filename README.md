# Weather-Adaptive Autonomous Rocket GNC Flight Simulation

An educational Python point-mass simulation of rocket flight with vertical proportional-derivative (PD) altitude control, altitude-dependent air density, wind disturbances, aerodynamic drag, and finite fuel. The program exports flight telemetry and generates altitude-versus-time and 3D trajectory plots.

This simplified model is intended for learning and visualization. It has not been validated against real vehicle data and must not be used for real-world vehicle design, guidance, or flight operations.

## Project framework and tool-use disclosure

AI tools were used to assist with drafting, refining, and organizing parts of the code and project documentation. The project owner should review and understand the implementation and follow any applicable school, application, or portfolio rules for disclosing AI assistance. Do not represent AI-generated work as exclusively human-authored.

This software is provided as-is for educational and demonstration purposes, without warranties. It is not certified or suitable for operational aviation use.

## Features

- Three-axis point-mass position and velocity model
- Exponentially decreasing air density with altitude
- Altitude-varying sinusoidal wind and repeatable random gusts
- Wind-relative aerodynamic drag
- Gravity-compensated, bounded vertical PD thrust command
- Finite fuel tracking and touchdown handling
- CSV telemetry export and combined altitude/3D trajectory visualization

The controller commands vertical thrust only. Wind affects the simulated vehicle through drag; the model does not actively control horizontal drift or demonstrate validated wind-adaptive stability.

## Project structure

```text
.
├── data/                         # Generated telemetry CSV
├── results/                      # Generated visualization
├── src/
│   └── autonomous_rocket.py      # Simulation entry point
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

Python 3.9 or newer is recommended.

```bash
python -m pip install -r requirements.txt
```

## Run the simulation

From the repository root:

```bash
python src/autonomous_rocket.py
```

The script creates the output directories as needed and writes:

- `data/autonomous_flight_log.csv`
- `results/autonomous_flight_altitude.png`

The telemetry sample count depends on when the simulated flight ends; check the generated CSV before stating a specific number of data rows.

## Model overview and limitations

The simulation uses a simple point-mass model, a fixed time step, a basic vertical PD controller, and simplified atmospheric and wind assumptions. Its plots illustrate the behavior of this implementation and are not predictions of real rocket performance.
