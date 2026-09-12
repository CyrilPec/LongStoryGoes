"""
026+01.py — Workshop Materials and Objects
Defines physical materials, tools, and object specifications.
This module does not change World state.
The World remains authoritative.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Material:
    id: str
    name: str
    density: float
    hardness: float
    stiffness: float
    strength: float


@dataclass(frozen=True)
class PhysicalObject:
    id: str
    name: str
    material: str
    size: Tuple[float, float, float]
    mass: float


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    mass: float
    impact_factor: float


class Workshop:
    """
    A catalog of things that can be proposed to the World.

    The Workshop describes objects.
    It does not create or modify physical reality.
    """

    def __init__(self) -> None:
        self.materials: Dict[str, Material] = {}
        self.objects: Dict[str, PhysicalObject] = {}
        self.tools: Dict[str, Tool] = {}
        self._build_catalog()

    def _build_catalog(self) -> None:
        self.materials["wood"] = Material(
            id="wood",
            name="Wood",
            density=600.0,
            hardness=3.0,
            stiffness=10.0,
            strength=40.0,
        )

        self.materials["steel"] = Material(
            id="steel",
            name="Steel",
            density=7850.0,
            hardness=6.0,
            stiffness=200.0,
            strength=400.0,
        )

        self.tools["hammer"] = Tool(
            id="hammer",
            name="Hammer",
            mass=1.0,
            impact_factor=1.0,
        )

    def make_plank(
        self,
        object_id: str,
        size: Tuple[float, float, float] = (2.0, 0.2, 0.2),
    ) -> PhysicalObject:
        material = self.materials["wood"]
        volume = size[0] * size[1] * size[2]
        mass = material.density * volume

        plank = PhysicalObject(
            id=object_id,
            name="Wood Plank",
            material=material.id,
            size=size,
            mass=mass,
        )

        self.objects[object_id] = plank
        return plank

    def make_nail(
        self,
        object_id: str,
        length: float = 0.08,
        diameter: float = 0.004,
    ) -> PhysicalObject:
        material = self.materials["steel"]
        radius = diameter / 2.0
        volume = 3.141592653589793 * radius * radius * length
        mass = material.density * volume

        nail = PhysicalObject(
            id=object_id,
            name="Steel Nail",
            material=material.id,
            size=(diameter, diameter, length),
            mass=mass,
        )

        self.objects[object_id] = nail
        return nail

    def object_spec(
        self,
        object_id: str,
        position: Tuple[float, float, float],
    ) -> dict:
        if object_id not in self.objects:
            raise KeyError(f"Unknown workshop object: {object_id}")

        obj = self.objects[object_id]

        return {
            "id": obj.id,
            "name": obj.name,
            "material": obj.material,
            "mass": obj.mass,
            "size": obj.size,
            "position": position,
        }

    def material_properties(self, material_id: str) -> dict:
        if material_id not in self.materials:
            raise KeyError(f"Unknown material: {material_id}")

        material = self.materials[material_id]

        return {
            "id": material.id,
            "name": material.name,
            "density": material.density,
            "hardness": material.hardness,
            "stiffness": material.stiffness,
            "strength": material.strength,
        }

    def tool_properties(self, tool_id: str) -> dict:
        if tool_id not in self.tools:
            raise KeyError(f"Unknown tool: {tool_id}")

        tool = self.tools[tool_id]

        return {
            "id": tool.id,
            "name": tool.name,
            "mass": tool.mass,
            "impact_factor": tool.impact_factor,
        }


def self_test() -> None:
    workshop = Workshop()

    plank = workshop.make_plank("plank_01")
    nail = workshop.make_nail("nail_01")

    assert plank.mass > 0
    assert nail.mass > 0
    assert workshop.materials["wood"].density > 0
    assert workshop.materials["steel"].density > workshop.materials["wood"].density

    print("026+01 self_test: OK")


if __name__ == "__main__":
    self_test()
