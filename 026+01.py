"""
026+01.py — Workshop Objects
Defines reusable workshop objects for physical experiments.
The Workshop does not control the World.
The World remains authoritative.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Material:
    id: str
    name: str
    mass: float
    size: Tuple[float, float, float]


@dataclass(frozen=True)
class Tool:
    id: str
    name: str


class Workshop:
    """
    Describes objects available to an experiment.

    It does not create PyBullet bodies and does not mutate the World.
    Physical reality is created only through World.act().
    """

    def __init__(self) -> None:
        self.materials: Dict[str, Material] = {}
        self.tools: Dict[str, Tool] = {}
        self._build_catalog()

    def _build_catalog(self) -> None:
        self.materials["wood_plank"] = Material(
            id="wood_plank",
            name="Wood Plank",
            mass=1.0,
            size=(2.0, 0.2, 0.2),
        )

        self.materials["nail"] = Material(
            id="nail",
            name="Nail",
            mass=0.05,
            size=(0.08, 0.08, 0.4),
        )

        self.tools["hammer"] = Tool(
            id="hammer",
            name="Hammer",
        )

    def material(self, material_id: str) -> Material:
        if material_id not in self.materials:
            raise KeyError(f"Unknown material: {material_id}")
        return self.materials[material_id]

    def tool(self, tool_id: str) -> Tool:
        if tool_id not in self.tools:
            raise KeyError(f"Unknown tool: {tool_id}")
        return self.tools[tool_id]

    def create_spec(
        self,
        material_id: str,
        object_id: str,
        position: Tuple[float, float, float],
    ) -> dict:
        material = self.material(material_id)

        return {
            "id": object_id,
            "name": material.name,
            "mass": material.mass,
            "size": material.size,
            "position": position,
        }


def self_test() -> None:
    workshop = Workshop()

    plank = workshop.create_spec(
        "wood_plank",
        "plank_01",
        (0.0, 0.0, 1.0),
    )

    assert plank["id"] == "plank_01"
    assert plank["mass"] > 0
    assert len(plank["size"]) == 3
    assert workshop.tool("hammer").name == "Hammer"

    print("026+01 self_test: OK")


if __name__ == "__main__":
    self_test()
