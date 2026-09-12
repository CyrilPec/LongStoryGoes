"""
027.py — Construction Evolution Experiment

Goal:
    Discover a simple wood-and-nail construction that survives an increasing
    vertical load.

The experiment does not decide what is physically true.
It proposes a construction and asks the authoritative World to evaluate it.

Results:
    027-results/experiments.jsonl
    027-results/best_design.json
    027-results/report.txt

This is intentionally a small experiment.
Future versions can add better material models, tensors, optimization,
PyBullet constraints, structural mechanics, or additional experiments.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any, Dict, List

from importlib.util import module_from_spec, spec_from_file_location


WORLD_FILE = "000-01-01.py"
NUMERICAL_FILE = "027+01.py"
RESULTS_DIR = Path("027-results")
SEED = 2701
CANDIDATES = 100


def load_module(filename: str, name: str):
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {filename}"
        )

    spec = spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Cannot load module: {filename}"
        )

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


world_module = load_module(WORLD_FILE, "world_027")
numerical = load_module(NUMERICAL_FILE, "numerical_027")


def make_candidate(rng: random.Random, number: int) -> Dict[str, Any]:
    plank_length = rng.uniform(0.8, 2.0)
    plank_width = rng.uniform(0.08, 0.20)
    plank_height = rng.uniform(0.04, 0.12)

    nail_count = rng.randint(1, 5)
    nail_length = rng.uniform(0.05, 0.14)
    nail_diameter = rng.uniform(0.002, 0.008)

    hammer_mass = rng.uniform(0.5, 2.0)
    impact_velocity = rng.uniform(2.0, 8.0)

    load = rng.uniform(1.0, 20.0)

    nail_spacing = plank_length / max(nail_count, 1)

    return {
        "candidate": number,
        "plank": {
            "length": plank_length,
            "width": plank_width,
            "height": plank_height,
            "mass": numerical.box_mass(
                plank_length,
                plank_width,
                plank_height,
                600.0,
            ),
        },
        "nails": {
            "count": nail_count,
            "length": nail_length,
            "diameter": nail_diameter,
            "spacing": nail_spacing,
        },
        "hammer": {
            "mass": hammer_mass,
            "impact_velocity": impact_velocity,
        },
        "load_kg": load,
    }


def evaluate_candidate(
    candidate: Dict[str, Any],
) -> Dict[str, Any]:
    world = world_module.World()

    try:
        plank = world.add_physical_object(
            object_id="plank",
            mass=candidate["plank"]["mass"],
            size=(
                candidate["plank"]["length"],
                candidate["plank"]["width"],
                candidate["plank"]["height"],
            ),
            position=(0.0, 0.0, 0.5),
            material="wood",
            dynamic=True,
        )

        if not plank["ok"]:
            return {
                "approved": False,
                "reason": plank["error"],
            }

        total_connection_strength = 0.0
        successful_nails = 0
        nail_results: List[Dict[str, Any]] = []

        for index in range(candidate["nails"]["count"]):
            nail_id = f"nail_{index}"

            nail = world.add_physical_object(
                object_id=nail_id,
                mass=0.002,
                size=(
                    candidate["nails"]["diameter"],
                    candidate["nails"]["diameter"],
                    candidate["nails"]["length"],
                ),
                position=(
                    -candidate["plank"]["length"] / 2.0
                    + candidate["nails"]["spacing"]
                    * (index + 0.5),
                    0.0,
                    0.58,
                ),
                material="steel",
                dynamic=True,
            )

            if not nail["ok"]:
                nail_results.append({
                    "nail": nail_id,
                    "approved": False,
                    "reason": nail["error"],
                })
                continue

            result = world.act(
                "anna",
                "fastener",
                target=nail_id,
                parameters={
                    "other": "plank",
                    "hammer": candidate["hammer"],
                    "contact_limit": 0.15,
                },
            )

            nail_results.append({
                "nail": nail_id,
                "approved": result["ok"],
                "result": result,
            })

            if result["ok"]:
                successful_nails += 1

                connection_id = next(
                    reversed(world.connections)
                )

                total_connection_strength += (
                    world.connections[connection_id].strength
                )

        capacity = numerical.estimate_joint_capacity(
            connection_strength=total_connection_strength,
            nail_count=successful_nails,
            plank_length=candidate["plank"]["length"],
        )

        survives = capacity >= candidate["load_kg"]

        return {
            "approved": survives,
            "capacity_kg": capacity,
            "load_kg": candidate["load_kg"],
            "successful_nails": successful_nails,
            "total_connection_strength": total_connection_strength,
            "nails": nail_results,
            "world_time": world.time,
            "world_state": world.state(),
        }

    finally:
        world.close()


def save_jsonl(
    path: Path,
    records: List[Dict[str, Any]],
) -> None:
    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    sort_keys=True,
                )
                + "\n"
            )


def save_report(
    path: Path,
    records: List[Dict[str, Any]],
) -> None:
    approved = [
        record
        for record in records
        if record["result"]["approved"]
    ]

    if approved:
        best = max(
            approved,
            key=lambda record: record["result"]["capacity_kg"],
        )
    else:
        best = None

    lines = [
        "027 — Construction Evolution Experiment",
        "",
        f"Random seed: {SEED}",
        f"Candidates: {len(records)}",
        f"Approved: {len(approved)}",
        "",
    ]

    if best is not None:
        lines.extend([
            "BEST CANDIDATE",
            f"Candidate: {best['candidate']['candidate']}",
            f"Capacity: "
            f"{best['result']['capacity_kg']:.4f} kg",
            f"Required load: "
            f"{best['result']['load_kg']:.4f} kg",
            f"Successful nails: "
            f"{best['result']['successful_nails']}",
            "",
            "The result was accepted only after the World",
            "evaluated the proposed construction.",
        ])
    else:
        lines.extend([
            "No candidate survived its requested load.",
            "This is a valid experimental result.",
        ])

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rng = random.Random(SEED)
    records: List[Dict[str, Any]] = []

    for number in range(1, CANDIDATES + 1):
        candidate = make_candidate(
            rng,
            number,
        )

        result = evaluate_candidate(
            candidate,
        )

        record = {
            "experiment": "027",
            "candidate": candidate,
            "result": result,
        }

        records.append(record)

        print(
            f"candidate={number:03d} "
            f"approved={result['approved']} "
            f"capacity={result.get('capacity_kg', 0.0):.3f} "
            f"load={result.get('load_kg', candidate['load_kg']):.3f}"
        )

    save_jsonl(
        RESULTS_DIR / "experiments.jsonl",
        records,
    )

    approved = [
        record
        for record in records
        if record["result"]["approved"]
    ]

    if approved:
        best = max(
            approved,
            key=lambda record: record["result"]["capacity_kg"],
        )

        (RESULTS_DIR / "best_design.json").write_text(
            json.dumps(
                best,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    save_report(
        RESULTS_DIR / "report.txt",
        records,
    )

    print()
    print("Experiment complete.")
    print(f"Results: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
