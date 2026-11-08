# Aerospace GNC Simulation

An educational Python point-mass rocket simulation featuring a vertical proportional-derivative (PD) altitude controller, wind disturbance, aerodynamic drag, fuel use, CSV telemetry, and altitude/3D trajectory plots.

> **Important:** This simplified model is for learning and visualization only. It has not been validated against real vehicle data and must not be used for real vehicle design, guidance, or flight operations. The controller commands vertical thrust only; the wind is modeled as a disturbance acting through drag, not as actively controlled horizontal guidance.

## Project layout

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

## Run the simulation

Python 3.9 or newer is recommended.

```bash
python -m pip install -r requirements.txt
python src/autonomous_rocket.py
```

The script creates `data/` and `results/` as needed, then writes:

- `data/autonomous_flight_log.csv`
- `results/autonomous_flight_altitude.png`

Wind gusts use a fixed random seed, making each run reproducible. Ground contact is detected at the end of a simulation step, so touchdown timing is quantized by the 0.05-second time step.

## Model contents

- Three-axis point-mass position and velocity.
- Exponentially decreasing air density and drag based on velocity relative to wind.
- Altitude-varying sinusoidal wind and seeded random gusts.
- Bounded vertical PD thrust command with gravity compensation and finite fuel.
- CSV telemetry and combined altitude/3D trajectory plot.

These assumptions are intentionally simplified; the outputs illustrate the model's behavior rather than predicting the performance of a real rocket.
