"""
025.py — Numerical Flow Experiment

LONGSTORYGOES EXPERIMENT 025

Question
--------
How does a simulated two-dimensional fluid flow change as numerical
resolution changes?

Scientific motivation
---------------------
The three-dimensional Navier–Stokes regularity problem is open.

This experiment does NOT attempt to solve that problem.

Instead, it creates a small computational laboratory in which the world
can:

    1. create a physical system
    2. define initial conditions
    3. simulate the system
    4. measure quantities
    5. repeat the experiment at different resolutions
    6. compare the observations
    7. refuse to call numerical evidence a proof

The experiment is intentionally dependency-free.

That gives LongStoryGoes a reproducible first scientific baseline before
introducing NumPy/SciPy/PyBullet in later experiments.

Model
-----
A simple 2-D incompressible vorticity equation is evolved:

    dω/dt + u·∇ω = ν∇²ω

where:

    ω = vorticity
    u = velocity
    ν = viscosity

For the velocity field we use a stream function ψ satisfying:

    ∇²ψ = -ω

Periodic boundaries are used.

This is a computational experiment, not a claim of high-fidelity
physical simulation.

Important epistemic rule
------------------------
A result that changes substantially with numerical resolution is NOT
treated as established physical behavior.

The experiment therefore measures:

    - maximum vorticity
    - mean absolute vorticity
    - kinetic-energy proxy
    - numerical stability
    - resolution sensitivity

Possible conclusions:

    CONSISTENT
    SENSITIVE_TO_RESOLUTION
    UNSTABLE
    INCONCLUSIVE

The world is allowed to say:

    "I do not know."

That is a feature, not a failure.
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple


# ----------------------------------------------------------------------
# PhysicalObject concept
# ----------------------------------------------------------------------

try:
    # The filename contains a '+', so normal import syntax cannot be used.
    # The experiment therefore contains the small physical-world object
    # it needs when executed directly.
    from importlib.util import module_from_spec, spec_from_file_location

    _concept_path = Path(__file__).with_name("001+01.py")
    _spec = spec_from_file_location("longstory_physical_object", _concept_path)

    if _spec is not None and _spec.loader is not None:
        _module = module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        PhysicalObject = _module.PhysicalObject
    else:
        raise ImportError("Unable to load 001+01.py")

except Exception:
    # A fallback keeps 025.py executable if copied somewhere without the
    # concept file. The repository version should normally use 001+01.py.
    @dataclass
    class PhysicalObject:
        id: str
        name: str


# ----------------------------------------------------------------------
# Experiment configuration
# ----------------------------------------------------------------------

@dataclass
class ExperimentConfig:
    resolution: int
    viscosity: float
    steps: int
    dt: float
    measurement_interval: int = 20


@dataclass
class ExperimentResult:
    resolution: int
    viscosity: float
    steps: int
    dt: float

    stable: bool
    max_vorticity: float
    final_max_vorticity: float
    mean_abs_vorticity: float
    initial_energy: float
    final_energy: float
    energy_change: float

    measurements: int

    def as_dict(self):
        return asdict(self)


# ----------------------------------------------------------------------
# Numerical utilities
# ----------------------------------------------------------------------

def zeros(n: int) -> List[List[float]]:
    return [[0.0 for _ in range(n)] for _ in range(n)]


def periodic_index(i: int, n: int) -> int:
    return i % n


def laplacian(field: List[List[float]], i: int, j: int, h: float) -> float:
    n = len(field)

    center = field[i][j]

    return (
        field[(i + 1) % n][j]
        + field[(i - 1) % n][j]
        + field[i][(j + 1) % n]
        + field[i][(j - 1) % n]
        - 4.0 * center
    ) / (h * h)


def central_x(field: List[List[float]], i: int, j: int, h: float) -> float:
    n = len(field)

    return (
        field[(i + 1) % n][j]
        - field[(i - 1) % n][j]
    ) / (2.0 * h)


def central_y(field: List[List[float]], i: int, j: int, h: float) -> float:
    n = len(field)

    return (
        field[i][(j + 1) % n]
        - field[i][(j - 1) % n]
    ) / (2.0 * h)


# ----------------------------------------------------------------------
# Flow simulator
# ----------------------------------------------------------------------

class FlowWorld:
    """
    Small computational world.

    The world contains one physical fluid object and numerical fields
    describing its current state.
    """

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.n = config.resolution
        self.h = 1.0 / self.n

        self.fluid = PhysicalObject(
            id=f"fluid-{self.n}",
            name="Periodic Fluid",
        )

        self.fluid.set_property(
            "viscosity",
            config.viscosity,
            reason="experiment configuration",
        )

        self.fluid.set_property(
            "resolution",
            self.n,
            reason="experiment configuration",
        )

        self.vorticity = zeros(self.n)
        self.stream = zeros(self.n)
        self.u = zeros(self.n)
        self.v = zeros(self.n)

        self.time = 0.0
        self.step = 0

        self._initialize_vorticity()

    # ------------------------------------------------------------------
    # Initial condition
    # ------------------------------------------------------------------

    def _initialize_vorticity(self) -> None:
        """
        Two opposite smooth vortical regions.

        This creates a non-trivial flow while remaining deterministic.
        """

        n = self.n

        for i in range(n):
            x = (i + 0.5) / n

            for j in range(n):
                y = (j + 0.5) / n

                a = self._periodic_gaussian(
                    x, y,
                    0.32, 0.50,
                    0.08,
                )

                b = self._periodic_gaussian(
                    x, y,
                    0.68, 0.50,
                    0.08,
                )

                self.vorticity[i][j] = 5.0 * (a - b)

        self._solve_stream_function()

    @staticmethod
    def _periodic_distance(a: float, b: float) -> float:
        d = abs(a - b)
        return min(d, 1.0 - d)

    @classmethod
    def _periodic_gaussian(
        cls,
        x: float,
        y: float,
        cx: float,
        cy: float,
        width: float,
    ) -> float:
        dx = cls._periodic_distance(x, cx)
        dy = cls._periodic_distance(y, cy)

        return math.exp(
            -(dx * dx + dy * dy) / (2.0 * width * width)
        )

    # ------------------------------------------------------------------
    # Poisson solve
    # ------------------------------------------------------------------

    def _solve_stream_function(self, iterations: int = 80) -> None:
        """
        Jacobi iteration for:

            ∇²ψ = -ω

        The mean stream function is constrained to zero.
        """

        n = self.n
        h2 = self.h * self.h

        psi = self.stream
        new_psi = zeros(n)

        for _ in range(iterations):
            for i in range(n):
                for j in range(n):
                    new_psi[i][j] = 0.25 * (
                        psi[(i + 1) % n][j]
                        + psi[(i - 1) % n][j]
                        + psi[i][(j + 1) % n]
                        + psi[i][(j - 1) % n]
                        + h2 * self.vorticity[i][j]
                    )

            psi, new_psi = new_psi, psi

        self.stream = psi

        # u = dψ/dy
        # v = -dψ/dx
        for i in range(n):
            for j in range(n):
                self.u[i][j] = central_y(self.stream, i, j, self.h)
                self.v[i][j] = -central_x(self.stream, i, j, self.h)

    # ------------------------------------------------------------------
    # Advection + diffusion
    # ------------------------------------------------------------------

    def _advect_diffuse(self) -> None:
        n = self.n
        h = self.h
        dt = self.config.dt
        viscosity = self.config.viscosity

        new_field = zeros(n)

        for i in range(n):
            for j in range(n):
                omega = self.vorticity[i][j]

                dwdx = central_x(self.vorticity, i, j, h)
                dwdy = central_y(self.vorticity, i, j, h)

                diffusion = laplacian(
                    self.vorticity,
                    i,
                    j,
                    h,
                )

                advection = (
                    self.u[i][j] * dwdx
                    + self.v[i][j] * dwdy
                )

                new_field[i][j] = (
                    omega
                    + dt * (
                        -advection
                        + viscosity * diffusion
                    )
                )

        self.vorticity = new_field

    # ------------------------------------------------------------------
    # Measurements
    # ------------------------------------------------------------------

    def max_abs_vorticity(self) -> float:
        return max(
            abs(value)
            for row in self.vorticity
            for value in row
        )

    def mean_abs_vorticity(self) -> float:
        values = [
            abs(value)
            for row in self.vorticity
            for value in row
        ]

        return statistics.fmean(values)

    def kinetic_energy_proxy(self) -> float:
        """
        Approximate:

            E = 1/2 ∫ (u² + v²) dA

        over the unit periodic domain.
        """

        total = 0.0

        for i in range(self.n):
            for j in range(self.n):
                total += 0.5 * (
                    self.u[i][j] ** 2
                    + self.v[i][j] ** 2
                )

        return total * self.h * self.h

    def measure(self) -> dict:
        max_vorticity = self.max_abs_vorticity()

        measurement = {
            "step": self.step,
            "time": self.time,
            "max_vorticity": max_vorticity,
            "mean_abs_vorticity": self.mean_abs_vorticity(),
            "kinetic_energy": self.kinetic_energy_proxy(),
        }

        self.fluid.measure(
            "max_vorticity",
            max_vorticity,
            step=self.step,
            time=self.time,
            source="simulation",
        )

        return measurement

    # ------------------------------------------------------------------
    # One simulation step
    # ------------------------------------------------------------------

    def step_once(self) -> dict:
        self._solve_stream_function()
        self._advect_diffuse()

        self.step += 1
        self.time += self.config.dt

        return self.measure()


# ----------------------------------------------------------------------
# Experiment
# ----------------------------------------------------------------------

def run_experiment(config: ExperimentConfig) -> ExperimentResult:
    world = FlowWorld(config)

    initial_energy = world.kinetic_energy_proxy()
    max_seen = world.max_abs_vorticity()

    stable = True
    recorded_measurements = 0
    final_measurement = world.measure()

    for step in range(config.steps):
        measurement = world.step_once()

        if (
            step % config.measurement_interval == 0
            or step == config.steps - 1
        ):
            final_measurement = measurement
            recorded_measurements += 1

        max_seen = max(
            max_seen,
            measurement["max_vorticity"],
        )

        values = (
            measurement["max_vorticity"],
            measurement["mean_abs_vorticity"],
            measurement["kinetic_energy"],
        )

        if not all(math.isfinite(value) for value in values):
            stable = False
            break

        # A deliberately conservative numerical alarm.
        if measurement["max_vorticity"] > 1e6:
            stable = False
            break

    final_energy = final_measurement["kinetic_energy"]

    return ExperimentResult(
        resolution=config.resolution,
        viscosity=config.viscosity,
        steps=world.step,
        dt=config.dt,
        stable=stable,
        max_vorticity=max_seen,
        final_max_vorticity=final_measurement["max_vorticity"],
        mean_abs_vorticity=final_measurement["mean_abs_vorticity"],
        initial_energy=initial_energy,
        final_energy=final_energy,
        energy_change=final_energy - initial_energy,
        measurements=recorded_measurements,
    )


# ----------------------------------------------------------------------
# Scientific comparison
# ----------------------------------------------------------------------

def relative_difference(a: float, b: float) -> float:
    denominator = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / denominator


def compare(
    coarse: ExperimentResult,
    fine: ExperimentResult,
) -> Tuple[str, float]:
    """
    Compare two resolutions.

    This is intentionally not a mathematical convergence proof.
    It is an experimental diagnostic.
    """

    differences = [
        relative_difference(
            coarse.final_max_vorticity,
            fine.final_max_vorticity,
        ),
        relative_difference(
            coarse.mean_abs_vorticity,
            fine.mean_abs_vorticity,
        ),
        relative_difference(
            coarse.final_energy,
            fine.final_energy,
        ),
    ]

    sensitivity = statistics.fmean(differences)

    if not coarse.stable or not fine.stable:
        conclusion = "UNSTABLE"

    elif sensitivity < 0.05:
        conclusion = "CONSISTENT"

    elif sensitivity < 0.25:
        conclusion = "SENSITIVE_TO_RESOLUTION"

    else:
        conclusion = "INCONCLUSIVE"

    return conclusion, sensitivity


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

def print_result(result: ExperimentResult) -> None:
    print()
    print(f"Resolution:        {result.resolution} x {result.resolution}")
    print(f"Viscosity:         {result.viscosity}")
    print(f"Steps:             {result.steps}")
    print(f"dt:                {result.dt}")
    print(f"Stable:            {result.stable}")
    print(f"Maximum vorticity: {result.max_vorticity:.8f}")
    print(f"Final vorticity:   {result.final_max_vorticity:.8f}")
    print(f"Mean |vorticity|:  {result.mean_abs_vorticity:.8f}")
    print(f"Initial energy:    {result.initial_energy:.8f}")
    print(f"Final energy:      {result.final_energy:.8f}")
    print(f"Energy change:     {result.energy_change:.8f}")


def save_results(results: List[ExperimentResult], conclusion: str, sensitivity: float) -> Path:
    output = {
        "experiment": 25,
        "question": (
            "How does simulated two-dimensional flow "
            "change with numerical resolution?"
        ),
        "scientific_status": (
            "computational experiment; not a proof "
            "about the 3-D Navier-Stokes regularity problem"
        ),
        "conclusion": conclusion,
        "resolution_sensitivity": sensitivity,
        "results": [result.as_dict() for result in results],
    }

    path = Path(__file__).with_name("025_results.json")

    path.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    return path


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    print("=" * 70)
    print("LONGSTORYGOES — EXPERIMENT 025")
    print("=" * 70)

    print()
    print("Question:")
    print(
        "How does a simulated fluid flow behave as "
        "numerical resolution changes?"
    )

    print()
    print("Important:")
    print(
        "This is a computational experiment, NOT a solution "
        "to the Navier–Stokes Millennium Problem."
    )

    viscosity = 0.01
    steps = 120
    dt = 0.0005

    # Keep the first experiment deliberately small enough to run
    # in ordinary Python without external numerical libraries.
    configurations = [
        ExperimentConfig(
            resolution=16,
            viscosity=viscosity,
            steps=steps,
            dt=dt,
        ),
        ExperimentConfig(
            resolution=32,
            viscosity=viscosity,
            steps=steps,
            dt=dt,
        ),
    ]

    results: List[ExperimentResult] = []

    for index, config in enumerate(configurations, start=1):
        print()
        print("-" * 70)
        print(f"EXPERIMENT {index}")
        print("-" * 70)

        result = run_experiment(config)
        results.append(result)

        print_result(result)

    conclusion, sensitivity = compare(
        results[0],
        results[1],
    )

    print()
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)

    print(f"Resolution sensitivity: {sensitivity:.6f}")
    print(f"Conclusion:             {conclusion}")

    print()
    print("Scientific interpretation:")
    print(
        "The result is evidence about this numerical experiment only."
    )

    if conclusion == "CONSISTENT":
        print(
            "The measured quantities are reasonably consistent "
            "between the tested resolutions."
        )

    elif conclusion == "SENSITIVE_TO_RESOLUTION":
        print(
            "The measured quantities change noticeably with "
            "resolution. More investigation is required."
        )

    elif conclusion == "UNSTABLE":
        print(
            "The numerical experiment became unstable. "
            "No physical conclusion is drawn."
        )

    else:
        print(
            "The experiment does not provide enough evidence "
            "for a reliable conclusion."
        )

    path = save_results(
        results,
        conclusion,
        sensitivity,
    )

    print()
    print(f"Evidence saved to: {path.name}")

    print()
    print("=" * 70)
    print("END OF EXPERIMENT 025")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
