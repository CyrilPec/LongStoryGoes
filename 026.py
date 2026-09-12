"""
026.py — First Workshop Experiment
Tests whether the authoritative physical World can create and connect objects.

The experiment proposes actions.
The World decides whether those actions are real.
"""

from importlib.util import module_from_spec, spec_from_file_location

from pathlib import Path

from workshop_026 import Workshop


def load_world():
    path = Path(__file__).with_name("000-01-01.py")
    spec = spec_from_file_location("physical_world", path)

    if spec is None or spec.loader is None:
        raise ImportError("Cannot load 000-01-01.py")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.World


def run_experiment() -> None:
    World = load_world()

    world = World()
    workshop = Workshop()

    try:
        print("=" * 72)
        print("026 — FIRST WORKSHOP EXPERIMENT")
        print("=" * 72)

        print("\nCreating first plank through the World.")

        result = world.act(
            "anna",
            "create_physical",
            target="plank_01",
            parameters=workshop.create_spec(
                "wood_plank",
                "plank_01",
                (0.0, 0.0, 1.0),
            ),
        )

        print(result)

        print("\nCreating second plank through the World.")

        result = world.act(
            "anna",
            "create_physical",
            target="plank_02",
            parameters=workshop.create_spec(
                "wood_plank",
                "plank_02",
                (0.0, 0.0, 1.21),
            ),
        )

        print(result)

        print("\nAttempting physical connection.")

        result = world.act(
            "anna",
            "connect_physical",
            target="plank_01",
            parameters={
                "other": "plank_02",
                "max_distance": 0.25,
            },
        )

        print(result)

        print("\nAuthoritative physical state:")

        print(world.state())

        print("\nExperiment history:")

        for event in world.history:
            print(event)

        print("\nThe experiment does not decide whether the connection happened.")
        print("The World decides.")

    finally:
        world.close()


if __name__ == "__main__":
    run_experiment()
