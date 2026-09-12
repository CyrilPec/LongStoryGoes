"""
026.py — Nail and Wood Experiment
Tests the first material interaction in the Workshop.

The experiment proposes physical actions.
The World validates and executes them.

A successful connection must be supported by physical state and
material interaction rules. The experiment itself cannot declare success.
"""

import importlib.util
from pathlib import Path


def load_module(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {filename}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_experiment() -> None:
    world_module = load_module("000-01-01.py", "physical_world")
    workshop_module = load_module("026+01.py", "workshop")

    World = world_module.World
    Workshop = workshop_module.Workshop

    world = World()
    workshop = Workshop()

    try:
        print("=" * 72)
        print("026 — NAIL AND WOOD EXPERIMENT")
        print("=" * 72)

        plank = workshop.make_plank("plank_01")
        nail = workshop.make_nail("nail_01")

        print("\nMaterial properties:")
        print(workshop.material_properties("wood"))
        print(workshop.material_properties("steel"))

        print("\nCreating wood through the authoritative World:")

        result = world.act(
            "anna",
            "create_physical",
            target=plank.id,
            parameters=workshop.object_spec(
                plank.id,
                (0.0, 0.0, 1.0),
            ),
        )

        print(result)

        print("\nCreating nail through the authoritative World:")

        result = world.act(
            "anna",
            "create_physical",
            target=nail.id,
            parameters=workshop.object_spec(
                nail.id,
                (0.0, 0.0, 1.12),
            ),
        )

        print(result)

        print("\nAttempting to connect nail and wood:")

        result = world.act(
            "anna",
            "connect_physical",
            target=nail.id,
            parameters={
                "other": plank.id,
                "max_distance": 0.15,
                "interaction": "fastener",
                "tool": "hammer",
                "material_properties": {
                    "fastener_material": workshop.material_properties("steel"),
                    "target_material": workshop.material_properties("wood"),
                    "tool": workshop.tool_properties("hammer"),
                },
            },
        )

        print(result)

        print("\nAuthoritative physical state:")
        print(world.state())

        print("\nHistory:")
        for event in world.history:
            print(event)

        print("\nExperiment conclusion:")
        if result["ok"]:
            print("The World accepted the proposed physical interaction.")
        else:
            print("The World rejected the proposed physical interaction.")

    finally:
        world.close()


if __name__ == "__main__":
    run_experiment()
