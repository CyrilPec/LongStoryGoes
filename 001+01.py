"""
001+01.py — PhysicalObject

A PhysicalObject is not merely something that exists in the world.

It is something whose physical state can:
    - be observed
    - be measured
    - be changed by interaction
    - be simulated
    - acquire experimental history

This concept deliberately keeps the physics implementation small.
The purpose is to establish the ontology needed by later experiments.

Evolution:
    001+00.py  -> conceptual PhysicalObject
    001+01.py  -> PhysicalObject becomes measurable/experimentable

The important distinction is:

    state       = what is currently happening
    properties  = what we believe/define about the object
    measurements = what an experiment actually observed
    history     = what happened over time
"""

from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from math import sqrt
from typing import Any, Dict, List, Optional


@dataclass
class Measurement:
    """
    A recorded observation of a physical quantity.

    Measurements are historical evidence.
    They do not silently change the object's physical state.
    """

    quantity: str
    value: Any
    step: int
    time: float
    source: str = "observation"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "quantity": self.quantity,
            "value": self.value,
            "step": self.step,
            "time": self.time,
            "source": self.source,
            "metadata": deepcopy(self.metadata),
        }


@dataclass
class PhysicalObject:
    """
    Minimal physical entity.

    The object deliberately does not know about:
        - Blender
        - PyBullet
        - NumPy
        - a particular renderer
        - a particular simulation engine

    A later simulation adapter can calculate consequences for it.
    """

    id: str
    name: str

    # Physical state
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    velocity: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    acceleration: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    # Described physical properties
    properties: Dict[str, Any] = field(default_factory=dict)

    # Current arbitrary state
    state: Dict[str, Any] = field(default_factory=dict)

    # Experimental knowledge
    measurements: List[Measurement] = field(default_factory=list)

    # Historical events/changes
    history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.position = list(self.position)
        self.velocity = list(self.velocity)
        self.acceleration = list(self.acceleration)

        if len(self.position) != 3:
            raise ValueError("position must contain exactly 3 values")

        if len(self.velocity) != 3:
            raise ValueError("velocity must contain exactly 3 values")

        if len(self.acceleration) != 3:
            raise ValueError("acceleration must contain exactly 3 values")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    def set_property(self, name: str, value: Any, *, reason: str = "") -> None:
        """
        Define or update a physical property.

        This is intentionally recorded in history.
        Later versions may distinguish between:
            known
            measured
            estimated
            assumed
        properties.
        """
        old_value = self.properties.get(name)

        self.properties[name] = value

        self.history.append(
            {
                "type": "property_changed",
                "property": name,
                "old": old_value,
                "new": value,
                "reason": reason,
            }
        )

    def get_property(self, name: str, default: Any = None) -> Any:
        return self.properties.get(name, default)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    def set_state(self, name: str, value: Any, *, reason: str = "") -> None:
        old_value = self.state.get(name)
        self.state[name] = value

        self.history.append(
            {
                "type": "state_changed",
                "state": name,
                "old": old_value,
                "new": value,
                "reason": reason,
            }
        )

    # ------------------------------------------------------------------
    # Measurements
    # ------------------------------------------------------------------

    def measure(
        self,
        quantity: str,
        value: Any,
        *,
        step: int = 0,
        time: float = 0.0,
        source: str = "observation",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Measurement:
        """
        Record evidence without changing the object.
        """
        measurement = Measurement(
            quantity=quantity,
            value=deepcopy(value),
            step=step,
            time=time,
            source=source,
            metadata=metadata or {},
        )

        self.measurements.append(measurement)

        return measurement

    def latest_measurement(self, quantity: str) -> Optional[Measurement]:
        for measurement in reversed(self.measurements):
            if measurement.quantity == quantity:
                return measurement

        return None

    # ------------------------------------------------------------------
    # Basic physical calculations
    # ------------------------------------------------------------------

    def speed(self) -> float:
        """Return the magnitude of velocity."""
        return sqrt(sum(component * component for component in self.velocity))

    def kinetic_energy(self) -> Optional[float]:
        """
        Calculate kinetic energy if mass is known.

            E = 1/2 m v²
        """
        mass = self.get_property("mass")

        if mass is None:
            return None

        return 0.5 * float(mass) * self.speed() ** 2

    # ------------------------------------------------------------------
    # Time evolution
    # ------------------------------------------------------------------

    def integrate(self, dt: float) -> None:
        """
        Perform a simple Euler integration step.

        This is intentionally basic.

        A sophisticated simulator should eventually live outside the
        object and calculate the consequences of interactions.

        Here the object merely provides a minimal executable physical
        behavior for early experiments.
        """
        if dt <= 0:
            raise ValueError("dt must be positive")

        old_position = self.position.copy()
        old_velocity = self.velocity.copy()

        for i in range(3):
            self.position[i] += self.velocity[i] * dt
            self.velocity[i] += self.acceleration[i] * dt

        self.history.append(
            {
                "type": "integration",
                "dt": dt,
                "old_position": old_position,
                "new_position": self.position.copy(),
                "old_velocity": old_velocity,
                "new_velocity": self.velocity.copy(),
            }
        )

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        """
        Return the current experimentally relevant state.
        """
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "acceleration": self.acceleration.copy(),
            "properties": deepcopy(self.properties),
            "state": deepcopy(self.state),
        }

    def __repr__(self) -> str:
        return (
            f"PhysicalObject("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"position={self.position!r}, "
            f"velocity={self.velocity!r})"
        )


if __name__ == "__main__":
    # Tiny concept test.
    object_ = PhysicalObject(
        id="object-001",
        name="Test Object",
        position=[0.0, 0.0, 0.0],
        velocity=[1.0, 0.0, 0.0],
    )

    object_.set_property("mass", 2.0, reason="initial assumption")

    object_.measure(
        "initial_speed",
        object_.speed(),
        source="calculation",
    )

    object_.integrate(1.0)

    object_.measure(
        "speed_after_1s",
        object_.speed(),
        step=1,
        time=1.0,
        source="calculation",
    )

    print(object_)
    print("Kinetic energy:", object_.kinetic_energy())
    print("Measurements:", len(object_.measurements))
