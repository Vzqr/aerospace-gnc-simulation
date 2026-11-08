"""Educational wind-affected rocket flight simulation.

This simplified point-mass model is intended for learning and visualization,
not real vehicle design, guidance, or flight operations.
"""

import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt

GRAVITY = 9.81  # m/s²
AIR_DENSITY_SEA = 1.225  # kg/m³
SCALE_HEIGHT = 8_500.0  # m
TARGET_ALTITUDE = 1_200.0  # m
TIME_STEP = 0.05  # s
MISSION_DURATION = 120.0  # s
RANDOM_SEED = 42

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"


class AutonomousRocket:
    """Point-mass rocket with vertical PD control and wind-relative drag."""

    def __init__(self):
        self.mass_empty = 50.0  # kg
        self.mass_fuel = 120.0  # kg
        self.max_thrust = 4_500.0  # N
        self.burn_rate_per_n = 0.0015  # kg/(N·s)
        self.drag_coeff = 0.42
        self.cross_section = 0.05  # m²

        self.x = self.y = self.z = 0.0
        self.vx = self.vy = self.vz = 0.0
        self.landed = False

    @property
    def total_mass(self):
        """Current vehicle mass, in kilograms."""
        return self.mass_empty + self.mass_fuel

    def calculate_gnc_autopilot(self, target_altitude):
        """Calculate bounded vertical PD thrust with gravity compensation."""
        altitude_error = target_altitude - self.z
        kp, kd = 8.5, 14.0
        requested_thrust = (
            kp * altitude_error - kd * self.vz + self.total_mass * GRAVITY
        )
        return max(0.0, min(requested_thrust, self.max_thrust))

    def update_physics(self, dt, target_altitude, rng):
        """Advance one step; return a state dictionary or ``None`` if landed.

        Ground contact is detected at the end of a numerical integration step,
        so the event timing is limited by ``dt`` (50 ms by default).
        """
        if dt <= 0.0:
            raise ValueError("dt must be greater than zero")
        if self.landed:
            return None

        wind_x = 4.0 * math.sin(self.z / 300.0) + rng.uniform(-1.5, 1.5)
        wind_y = -2.0 * math.cos(self.z / 400.0) + rng.uniform(-1.5, 1.5)

        thrust = 0.0
        if self.mass_fuel > 0.0:
            thrust = self.calculate_gnc_autopilot(target_altitude)
            requested_fuel = thrust * self.burn_rate_per_n * dt
            if requested_fuel >= self.mass_fuel:
                thrust = self.mass_fuel / (self.burn_rate_per_n * dt)
                self.mass_fuel = 0.0
            else:
                self.mass_fuel -= requested_fuel

        density = AIR_DENSITY_SEA * math.exp(-max(self.z, 0.0) / SCALE_HEIGHT)
        relative_velocity = (self.vx - wind_x, self.vy - wind_y, self.vz)
        relative_speed = math.sqrt(sum(component**2 for component in relative_velocity))
        drag_magnitude = (
            0.5 * density * relative_speed**2 * self.drag_coeff * self.cross_section
        )
        drag = tuple(
            -drag_magnitude * component / relative_speed if relative_speed else 0.0
            for component in relative_velocity
        )

        mass = self.total_mass
        ax = drag[0] / mass
        ay = drag[1] / mass
        az = (thrust + drag[2] - mass * GRAVITY) / mass

        # Semi-implicit Euler integration.
        self.vx += ax * dt
        self.vy += ay * dt
        self.vz += az * dt
        previous_z = self.z
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # Ignore the initial ground state; stop at the first subsequent descent
        # through ground level and include this touchdown state in the log.
        if previous_z > 0.0 and self.z <= 0.0 and self.vz < 0.0:
            self.z = 0.0
            self.vx = self.vy = self.vz = 0.0
            self.landed = True

        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "vx": self.vx,
            "vy": self.vy,
            "vz": self.vz,
            "fuel": self.mass_fuel,
            "wind_x": wind_x,
            "wind_y": wind_y,
        }


def run_mission():
    """Run the seeded simulation and save telemetry and plots in project folders."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rocket = AutonomousRocket()
    rng = random.Random(RANDOM_SEED)
    telemetry = []
    max_steps = int(MISSION_DURATION / TIME_STEP)

    print(f"Starting educational GNC simulation; target altitude: {TARGET_ALTITUDE:g} m.")
    for step in range(max_steps):
        state = rocket.update_physics(TIME_STEP, TARGET_ALTITUDE, rng)
        if state is None:
            break

        telemetry.append(
            {
                "time": round((step + 1) * TIME_STEP, 2),
                "x": round(state["x"], 3),
                "y": round(state["y"], 3),
                "z": round(state["z"], 3),
                "velocity_z": round(state["vz"], 2),
                "fuel": round(state["fuel"], 2),
                "wind_x": round(state["wind_x"], 2),
                "wind_y": round(state["wind_y"], 2),
            }
        )
        if rocket.landed:
            print("Touchdown detected; stopping the simulation.")
            break

    fields = ["time", "x", "y", "z", "velocity_z", "fuel", "wind_x", "wind_y"]
    csv_path = DATA_DIR / "autonomous_flight_log.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(telemetry)

    times = [row["time"] for row in telemetry]
    xs = [row["x"] for row in telemetry]
    ys = [row["y"] for row in telemetry]
    zs = [row["z"] for row in telemetry]

    fig = plt.figure(figsize=(14, 6))
    altitude_ax = fig.add_subplot(121)
    altitude_ax.plot(times, zs, color="teal", linewidth=2.2, label="Simulated altitude")
    altitude_ax.axhline(
        TARGET_ALTITUDE, color="crimson", linestyle="--", label="Target altitude"
    )
    altitude_ax.set(title="Altitude vs. Time", xlabel="Time (s)", ylabel="Altitude (m)")
    altitude_ax.grid(True, alpha=0.3)
    altitude_ax.legend()

    trajectory_ax = fig.add_subplot(122, projection="3d")
    trajectory_ax.plot(xs, ys, zs, color="teal", linewidth=2, label="Flight path")
    trajectory_ax.scatter([0], [0], [0], color="green", s=60, label="Launch point")
    trajectory_ax.set_title("3D Flight Trajectory")
    trajectory_ax.set_xlabel("East displacement (m)")
    trajectory_ax.set_ylabel("North displacement (m)")
    trajectory_ax.set_zlabel("Altitude (m)")
    trajectory_ax.legend()

    fig.tight_layout()
    plot_path = RESULTS_DIR / "autonomous_flight_altitude.png"
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Telemetry saved to: {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"Plot saved to: {plot_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    run_mission()
