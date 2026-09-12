"""
029.py — Three Descriptions, One World

Question:
    Can Newtonian, Lagrangian, and Hamiltonian descriptions
    produce the same observable behavior?

This experiment combines ideas developed throughout LongStoryGoes:

    - the World is authoritative
    - an experiment proposes a question
    - models make predictions
    - observations are compared rather than assumed
    - results are deterministic and reproducible
    - YES / NO / UNKNOWN are legitimate conclusions
    - evidence is persisted for future experiments

The first system is deliberately simple:

    V(q) = 1/2 * k * q^2

a one-dimensional harmonic oscillator.

Three independent descriptions are evaluated:

    Newton:
        m q'' = -k q

    Lagrange:
        L = 1/2 m q_dot^2 - 1/2 k q^2
        d/dt(dL/dq_dot) - dL/dq = 0

    Hamilton:
        H = p^2/(2m) + 1/2 k q^2
        q_dot = dH/dp
        p_dot = -dH/dq

The experiment does NOT conclude equivalence from mathematics.

It measures observable trajectories and energy conservation.

Conclusion:

    YES
        models agree within tolerance

    NO
        models disagree beyond tolerance

    UNKNOWN
        the experiment is insufficient to decide
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Dict, List


# ---------------------------------------------------------------------------
# Experiment configuration
# ---------------------------------------------------------------------------

EXPERIMENT = "029"
RESULTS_DIR = Path("029-results")

MASS = 1.0
SPRING_CONSTANT = 4.0

INITIAL_POSITION = 1.0
INITIAL_VELOCITY = 0.0

TOTAL_TIME = 10.0

# All three models use the same observation times.
DT = 0.001

# Agreement tolerance.
POSITION_TOLERANCE = 1e-5
VELOCITY_TOLERANCE = 1e-5
ENERGY_TOLERANCE = 1e-5


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------

class World:
    """
    The World is authoritative over the experimental initial state
    and over the recorded observation.

    Models do not modify World state.
    They only return predictions.
    """

    def __init__(self) -> None:
        self.time = 0.0
        self.history: List[Dict[str, object]] = []

        self.state = {
            "mass": MASS,
            "spring_constant": SPRING_CONSTANT,
            "position": INITIAL_POSITION,
            "velocity": INITIAL_VELOCITY,
        }

    def observe(self) -> Dict[str, float]:
        return {
            "time": self.time,
            "position": self.state["position"],
            "velocity": self.state["velocity"],
        }

    def record(self, event: str, data: Dict[str, object]) -> None:
        self.history.append({
            "time": self.time,
            "event": event,
            "data": data,
        })

    def ask(self, question: str) -> Dict[str, object]:
        """
        The experiment asks the World a question.

        The World does not accept a model's conclusion as truth.
        It records the question and returns the authoritative setup.
        """
        self.record(
            "experiment_question",
            {"question": question},
        )

        return {
            "ok": True,
            "question": question,
            "state": dict(self.state),
        }


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

@dataclass
class State:
    q: float
    v: float


@dataclass
class HamiltonState:
    q: float
    p: float


@dataclass
class Observation:
    time: float
    position: float
    velocity: float
    energy: float


# ---------------------------------------------------------------------------
# Physics
# ---------------------------------------------------------------------------

def potential(q: float) -> float:
    return 0.5 * SPRING_CONSTANT * q * q


def kinetic(v: float) -> float:
    return 0.5 * MASS * v * v


def energy(q: float, v: float) -> float:
    return kinetic(v) + potential(q)


def acceleration(q: float) -> float:
    """
    Newton's equation:

        m q'' = -k q
    """
    return -(SPRING_CONSTANT / MASS) * q


# ---------------------------------------------------------------------------
# Numerical integration
# ---------------------------------------------------------------------------

def rk4_step(
    state: State,
    dt: float,
    derivative: Callable[[State], State],
) -> State:
    """
    Generic RK4 integrator.

    Used independently by the Newton and Lagrange descriptions.
    """

    k1 = derivative(state)

    s2 = State(
        state.q + 0.5 * dt * k1.q,
        state.v + 0.5 * dt * k1.v,
    )
    k2 = derivative(s2)

    s3 = State(
        state.q + 0.5 * dt * k2.q,
        state.v + 0.5 * dt * k2.v,
    )
    k3 = derivative(s3)

    s4 = State(
        state.q + dt * k3.q,
        state.v + dt * k3.v,
    )
    k4 = derivative(s4)

    return State(
        q=state.q + dt * (
            k1.q + 2.0 * k2.q + 2.0 * k3.q + k4.q
        ) / 6.0,
        v=state.v + dt * (
            k1.v + 2.0 * k2.v + 2.0 * k3.v + k4.v
        ) / 6.0,
    )


# ---------------------------------------------------------------------------
# Newton model
# ---------------------------------------------------------------------------

def newton_derivative(state: State) -> State:
    return State(
        q=state.v,
        v=acceleration(state.q),
    )


def simulate_newton() -> List[Observation]:
    state = State(
        q=INITIAL_POSITION,
        v=INITIAL_VELOCITY,
    )

    observations: List[Observation] = []

    steps = int(round(TOTAL_TIME / DT))

    for step in range(steps + 1):
        time = step * DT

        observations.append(
            Observation(
                time=time,
                position=state.q,
                velocity=state.v,
                energy=energy(state.q, state.v),
            )
        )

        if step < steps:
            state = rk4_step(
                state,
                DT,
                newton_derivative,
            )

    return observations


# ---------------------------------------------------------------------------
# Lagrangian model
# ---------------------------------------------------------------------------

def lagrangian(q: float, v: float) -> float:
    """
    L = T - V
    """
    return kinetic(v) - potential(q)


def lagrangian_derivative(state: State) -> State:
    """
    Euler-Lagrange equation:

        d/dt(dL/dq_dot) - dL/dq = 0

    For

        L = 1/2 m q_dot^2 - 1/2 k q^2

    this gives

        m q'' = -k q
    """

    # dL/dq_dot = m * q_dot
    # d/dt(dL/dq_dot) = m * q''
    #
    # dL/dq = -kq
    #
    # m q'' + kq = 0

    acceleration_from_lagrange = (
        -SPRING_CONSTANT * state.q / MASS
    )

    return State(
        q=state.v,
        v=acceleration_from_lagrange,
    )


def simulate_lagrange() -> List[Observation]:
    state = State(
        q=INITIAL_POSITION,
        v=INITIAL_VELOCITY,
    )

    observations: List[Observation] = []

    steps = int(round(TOTAL_TIME / DT))

    for step in range(steps + 1):
        time = step * DT

        observations.append(
            Observation(
                time=time,
                position=state.q,
                velocity=state.v,
                energy=energy(state.q, state.v),
            )
        )

        if step < steps:
            state = rk4_step(
                state,
                DT,
                lagrangian_derivative,
            )

    return observations


# ---------------------------------------------------------------------------
# Hamiltonian model
# ---------------------------------------------------------------------------

def hamiltonian(q: float, p: float) -> float:
    """
    H = p^2/(2m) + V(q)
    """
    return (
        (p * p) / (2.0 * MASS)
        + potential(q)
    )


def simulate_hamilton() -> List[Observation]:
    """
    Hamilton's equations:

        q_dot = dH/dp = p/m
        p_dot = -dH/dq = -kq

    A symplectic Euler step is intentionally used here rather
    than the RK4 implementation used by Newton and Lagrange.

    This gives the Hamiltonian description an independently
    structured numerical evolution.
    """

    q = INITIAL_POSITION
    p = MASS * INITIAL_VELOCITY

    observations: List[Observation] = []

    steps = int(round(TOTAL_TIME / DT))

    for step in range(steps + 1):
        time = step * DT

        v = p / MASS

        observations.append(
            Observation(
                time=time,
                position=q,
                velocity=v,
                energy=hamiltonian(q, p),
            )
        )

        if step < steps:
            # Hamilton's equations.
            #
            # First update momentum:
            #
            # p_dot = -dH/dq = -kq
            #
            p = p - DT * SPRING_CONSTANT * q

            # Then update position:
            #
            # q_dot = dH/dp = p/m
            #
            q = q + DT * p / MASS

    return observations


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

@dataclass
class Comparison:
    model_a: str
    model_b: str
    max_position_error: float
    max_velocity_error: float
    max_energy_error: float
    agrees: bool


def compare(
    name_a: str,
    observations_a: List[Observation],
    name_b: str,
    observations_b: List[Observation],
) -> Comparison:

    if len(observations_a) != len(observations_b):
        raise ValueError(
            "Models produced different numbers of observations."
        )

    max_position_error = 0.0
    max_velocity_error = 0.0
    max_energy_error = 0.0

    for a, b in zip(observations_a, observations_b):
        if not math.isclose(a.time, b.time, abs_tol=1e-12):
            raise ValueError(
                f"Time mismatch: {a.time} != {b.time}"
            )

        max_position_error = max(
            max_position_error,
            abs(a.position - b.position),
        )

        max_velocity_error = max(
            max_velocity_error,
            abs(a.velocity - b.velocity),
        )

        max_energy_error = max(
            max_energy_error,
            abs(a.energy - b.energy),
        )

    agrees = (
        max_position_error <= POSITION_TOLERANCE
        and max_velocity_error <= VELOCITY_TOLERANCE
        and max_energy_error <= ENERGY_TOLERANCE
    )

    return Comparison(
        model_a=name_a,
        model_b=name_b,
        max_position_error=max_position_error,
        max_velocity_error=max_velocity_error,
        max_energy_error=max_energy_error,
        agrees=agrees,
    )


# ---------------------------------------------------------------------------
# World-level conclusion
# ---------------------------------------------------------------------------

def conclude(
    comparisons: List[Comparison],
) -> str:

    if all(comparison.agrees for comparison in comparisons):
        return "YES"

    if any(
        comparison.max_position_error > POSITION_TOLERANCE
        or comparison.max_velocity_error > VELOCITY_TOLERANCE
        for comparison in comparisons
    ):
        return "NO"

    return "UNKNOWN"


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_result(
    world: World,
    comparisons: List[Comparison],
    conclusion: str,
) -> None:

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = {
        "experiment": EXPERIMENT,
        "question": (
            "Do Newtonian, Lagrangian, and Hamiltonian "
            "descriptions produce the same observable behavior?"
        ),
        "system": {
            "type": "harmonic_oscillator",
            "mass": MASS,
            "spring_constant": SPRING_CONSTANT,
            "initial_position": INITIAL_POSITION,
            "initial_velocity": INITIAL_VELOCITY,
            "total_time": TOTAL_TIME,
            "dt": DT,
        },
        "tolerances": {
            "position": POSITION_TOLERANCE,
            "velocity": VELOCITY_TOLERANCE,
            "energy": ENERGY_TOLERANCE,
        },
        "comparisons": [
            asdict(comparison)
            for comparison in comparisons
        ],
        "conclusion": conclusion,
        "world_history": world.history,
    }

    (RESULTS_DIR / "result.json").write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "029 — Three Descriptions, One World",
        "",
        "Question:",
        (
            "Do Newtonian, Lagrangian, and Hamiltonian "
            "descriptions produce the same observable behavior?"
        ),
        "",
        f"Mass: {MASS}",
        f"Spring constant: {SPRING_CONSTANT}",
        f"Initial position: {INITIAL_POSITION}",
        f"Initial velocity: {INITIAL_VELOCITY}",
        f"Total time: {TOTAL_TIME}",
        f"Time step: {DT}",
        "",
        "COMPARISONS",
        "",
    ]

    for comparison in comparisons:
        lines.extend([
            (
                f"{comparison.model_a} vs "
                f"{comparison.model_b}"
            ),
            (
                "  max position error: "
                f"{comparison.max_position_error:.12g}"
            ),
            (
                "  max velocity error: "
                f"{comparison.max_velocity_error:.12g}"
            ),
            (
                "  max energy error: "
                f"{comparison.max_energy_error:.12g}"
            ),
            f"  agrees: {comparison.agrees}",
            "",
        ])

    lines.extend([
        "WORLD CONCLUSION",
        "",
        conclusion,
        "",
        "YES     = agreement within experimental tolerance",
        "NO      = disagreement beyond experimental tolerance",
        "UNKNOWN = experiment was insufficient to decide",
        "",
        "The experiment does not assume equivalence.",
        "It records evidence for or against it.",
    ])

    (RESULTS_DIR / "report.txt").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment() -> None:
    print("=" * 72)
    print("029 — THREE DESCRIPTIONS, ONE WORLD")
    print("=" * 72)

    world = World()

    question = (
        "Can Newtonian, Lagrangian, and Hamiltonian "
        "descriptions produce the same observable behavior?"
    )

    result = world.ask(question)

    print("\nWORLD")
    print(result["state"])

    print("\nQUESTION")
    print(question)

    print("\nRunning Newton model...")
    newton = simulate_newton()

    print("Running Lagrange model...")
    lagrange = simulate_lagrange()

    print("Running Hamilton model...")
    hamilton = simulate_hamilton()

    comparisons = [
        compare(
            "Newton",
            newton,
            "Lagrange",
            lagrange,
        ),
        compare(
            "Newton",
            newton,
            "Hamilton",
            hamilton,
        ),
        compare(
            "Lagrange",
            lagrange,
            "Hamilton",
            hamilton,
        ),
    ]

    conclusion = conclude(comparisons)

    print("\nEVIDENCE")
    print("-" * 72)

    for comparison in comparisons:
        print(
            f"{comparison.model_a} vs "
            f"{comparison.model_b}"
        )
        print(
            "  position error = "
            f"{comparison.max_position_error:.12g}"
        )
        print(
            "  velocity error = "
            f"{comparison.max_velocity_error:.12g}"
        )
        print(
            "  energy error   = "
            f"{comparison.max_energy_error:.12g}"
        )
        print(
            f"  agrees         = {comparison.agrees}"
        )
        print()

    world.record(
        "model_comparison",
        {
            "comparisons": [
                asdict(comparison)
                for comparison in comparisons
            ],
            "conclusion": conclusion,
        },
    )

    print("=" * 72)
    print(f"WORLD ANSWER: {conclusion}")
    print("=" * 72)

    if conclusion == "YES":
        print(
            "The three descriptions agree within "
            "the experimental tolerance."
        )
    elif conclusion == "NO":
        print(
            "At least one description disagrees "
            "with another beyond the tolerance."
        )
    else:
        print(
            "The experiment cannot decide."
        )

    save_result(
        world,
        comparisons,
        conclusion,
    )

    print()
    print(f"Results saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    run_experiment()
