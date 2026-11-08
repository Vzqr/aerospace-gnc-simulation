# Portfolio Materials

Use or adapt the copy below for a résumé, application, LinkedIn post, or portfolio website. The descriptions intentionally characterize this as an educational simulation rather than a validated aerospace system.

## Project title

**Weather-Adaptive Autonomous Rocket GNC Flight Simulation**

## GitHub short description

Educational Python rocket-flight simulation with a vertical PD altitude controller, wind disturbances, atmospheric drag, fuel tracking, telemetry export, and trajectory plots.

## Résumé bullet

- Built an educational Python rocket-flight simulation modeling altitude-dependent air density, wind disturbances, aerodynamic drag, and fuel consumption; implemented a gravity-compensated PD controller for vertical altitude commands and generated CSV telemetry plus altitude and 3D trajectory visualizations.

## Application / portfolio summary

Developed a Python point-mass rocket-flight simulation to explore how vertical control responds to simplified atmospheric and wind disturbances. The model combines an altitude-dependent air-density profile, wind-relative aerodynamic drag, finite fuel, and a proportional-derivative (PD) vertical thrust controller with gravity compensation. It exports reproducible telemetry and creates altitude-versus-time and 3D trajectory plots. This project is an educational model, not a validated prediction of real rocket performance.

## LinkedIn post

I built an educational rocket-flight simulation in Python to explore the intersection of aerospace dynamics and control systems.

The model includes altitude-dependent air density, wind disturbances, aerodynamic drag, fuel consumption, and a gravity-compensated PD controller for vertical altitude commands. It also exports flight telemetry to CSV and generates altitude and 3D trajectory visualizations.

This is a simplified point-mass learning project—not a real-world flight model—but it gave me a hands-on way to connect physics, numerical simulation, and feedback control.

Project: https://github.com/Vzqr/aerospace-gnc-simulation

#Python #Aerospace #ControlSystems #Simulation #Engineering

## Portfolio website showcase

### Weather-Adaptive Autonomous Rocket GNC Flight Simulation

A Python learning project for exploring rocket-flight dynamics and feedback control. It simulates a point-mass vehicle under gravity, altitude-varying air density, wind disturbances, aerodynamic drag, and finite fuel. A gravity-compensated PD controller commands vertical thrust toward a target altitude. The program records telemetry and produces altitude-time and 3D trajectory plots.

**Tools:** Python, Matplotlib, CSV, numerical integration, feedback control

**Key concepts:** Point-mass dynamics, atmospheric density model, wind-relative drag, PD control, telemetry visualization

**Outputs:** `data/autonomous_flight_log.csv` and `results/autonomous_flight_altitude.png` after running the simulation.

**Limitations:** The model is simplified and not validated against real vehicle data. The controller commands vertical thrust only; it does not actively steer or stabilize horizontal motion. Wind is a disturbance in the model, not an input used by an adaptive control law.

## Claims and wording to verify before publishing

- Avoid saying the controller actively compensates for wind or controls horizontal drift; the current model uses wind in the drag calculation but only commands vertical thrust.
- Avoid claiming the simulation proves stability or predicts real flight performance.
- Only state a telemetry sample count after checking the generated CSV. With the default 120-second limit and 0.05-second step, the maximum is 2,400 samples, but touchdown may end the run earlier.
- The fixed random seed makes simulated gusts repeatable; it does not make the model experimentally validated.
