"""
025.py — Initial Condition Experiment
Question:
How strongly can two nearly identical double pendulums diverge?
The experiment uses the concrete object from 001+01.py and PyBullet.
"""

from pathlib import Path
import importlib.util
import json
import math
import sys


def load_double_pendulum():
    path = Path(__file__).with_name("025+01.py")
    spec = importlib.util.spec_from_file_location("double_pendulum", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.DoublePendulum


DoublePendulum = load_double_pendulum()

TIME_STEP = 1 / 240
STEPS = 2400
INITIAL_ANGLE = math.radians(120)
INITIAL_DIFFERENCE = 1e-6


def distance(first, second):
    """Measure angular separation between two systems."""
    return math.sqrt(
        (first.state()[0] - second.state()[0]) ** 2
        + (first.state()[1] - second.state()[1]) ** 2
    )


def run():
    first = DoublePendulum(INITIAL_ANGLE, INITIAL_ANGLE)
    second = DoublePendulum(
        INITIAL_ANGLE,
        INITIAL_ANGLE + INITIAL_DIFFERENCE,
    )
    measurements = []
    try:
        for step in range(STEPS + 1):
            if step % 120 == 0:
                measurements.append({
                    "time": step * TIME_STEP,
                    "state_distance": distance(first, second),
                    "position_first": first.position(),
                    "position_second": second.position(),
                })
                print(
                    f"time={step * TIME_STEP:6.2f}s "
                    f"distance={measurements[-1]['state_distance']:.8e}"
                )
            first.step(TIME_STEP)
            second.step(TIME_STEP)
    finally:
        first.close()
        second.close()
    return measurements


def analyze(measurements):
    initial = measurements[0]["state_distance"]
    final = measurements[-1]["state_distance"]
    maximum = max(x["state_distance"] for x in measurements)
    return {
        "initial_distance": initial,
        "final_distance": final,
        "maximum_distance": maximum,
        "growth_factor": final / initial if initial else None,
    }


def main():
    print("LONGSTORYGOES — EXPERIMENT 025")
    print("Question: sensitivity to initial conditions")
    print()
    try:
        measurements = run()
    except KeyboardInterrupt:
        print("\nExperiment stopped by user.")
        return 130
    analysis = analyze(measurements)
    result = {
        "experiment": "025",
        "object": "DoublePendulum",
        "question": "How strongly can nearly identical systems diverge?",
        "initial_difference": INITIAL_DIFFERENCE,
        "time_step": TIME_STEP,
        "steps": STEPS,
        "analysis": analysis,
        "measurements": measurements,
    }
    output = Path(__file__).with_name("025_results.json")
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print()
    print("Initial distance:", analysis["initial_distance"])
    print("Final distance:", analysis["final_distance"])
    print("Growth factor:", analysis["growth_factor"])
    print(f"Evidence saved to {output.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
