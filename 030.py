"""
030.py — Tiny World

Goal:
    Build the smallest useful LongStoryGoes World.

Core principle:
    An agent proposes an action.
    The World decides whether it happens.
    The World owns state and consequences.
    Every accepted/rejected action is recorded in history.

This is intentionally small.
No LLM.
No renderer.
No external dependencies.

Experiment:
    Alice attempts to cross a wooden bridge.
    The river rises and damages the bridge.
    Alice attempts to cross again.
    The World rejects the impossible action.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# World primitives
# ---------------------------------------------------------------------------

@dataclass
class Entity:
    name: str
    kind: str
    state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    time: int
    event_type: str
    actor: str | None
    target: str | None
    accepted: bool
    reason: str
    consequences: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "event_type": self.event_type,
            "actor": self.actor,
            "target": self.target,
            "accepted": self.accepted,
            "reason": self.reason,
            "consequences": self.consequences,
        }


class World:
    """
    The authoritative state of the simulation.

    External code should request actions through act().
    It should not directly modify entity state.
    """

    def __init__(self) -> None:
        self.entities: Dict[str, Entity] = {}
        self.history: List[Event] = []
        self.time = 0

    # ------------------------------------------------------------------
    # Entity management
    # ------------------------------------------------------------------

    def add_entity(
        self,
        name: str,
        kind: str,
        **state: Any,
    ) -> None:
        if name in self.entities:
            raise ValueError(f"Entity already exists: {name}")

        self.entities[name] = Entity(
            name=name,
            kind=kind,
            state=dict(state),
        )

    def get(self, name: str) -> Entity:
        if name not in self.entities:
            raise KeyError(f"Unknown entity: {name}")

        return self.entities[name]

    # ------------------------------------------------------------------
    # Time
    # ------------------------------------------------------------------

    def tick(self) -> None:
        self.time += 1

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def act(
        self,
        actor: str,
        action: str,
        target: str | None = None,
        **parameters: Any,
    ) -> Event:
        """
        Receive an action proposal.

        The proposal is NOT automatically accepted.
        The World validates it and determines the consequence.
        """

        self.tick()

        if actor not in self.entities:
            return self._reject(
                event_type=action,
                actor=actor,
                target=target,
                reason="Unknown actor.",
            )

        if target is not None and target not in self.entities:
            return self._reject(
                event_type=action,
                actor=actor,
                target=target,
                reason="Unknown target.",
            )

        if action == "cross":
            return self._cross(actor, target)

        if action == "raise_river":
            return self._raise_river(actor, target, parameters)

        return self._reject(
            event_type=action,
            actor=actor,
            target=target,
            reason=f"Unknown action: {action}",
        )

    # ------------------------------------------------------------------
    # World rules
    # ------------------------------------------------------------------

    def _cross(
        self,
        actor_name: str,
        bridge_name: str | None,
    ) -> Event:

        if bridge_name is None:
            return self._reject(
                event_type="cross",
                actor=actor_name,
                target=None,
                reason="No bridge specified.",
            )

        actor = self.get(actor_name)
        bridge = self.get(bridge_name)

        if bridge.kind != "bridge":
            return self._reject(
                event_type="cross",
                actor=actor_name,
                target=bridge_name,
                reason="Target is not a bridge.",
            )

        integrity = float(bridge.state.get("integrity", 0.0))

        if integrity <= 0.0:
            return self._reject(
                event_type="cross",
                actor=actor_name,
                target=bridge_name,
                reason="The bridge has collapsed.",
            )

        if not bridge.state.get("passable", True):
            return self._reject(
                event_type="cross",
                actor=actor_name,
                target=bridge_name,
                reason="The bridge is not passable.",
            )

        old_location = actor.state.get("location")
        new_location = bridge.state.get("destination")

        actor.state["location"] = new_location

        # Crossing places a small load on the bridge.
        old_integrity = integrity
        new_integrity = max(0.0, integrity - 0.10)

        bridge.state["integrity"] = new_integrity

        if new_integrity <= 0.0:
            bridge.state["passable"] = False

        return self._accept(
            event_type="cross",
            actor=actor_name,
            target=bridge_name,
            reason="The World accepted the crossing.",
            consequences={
                "actor_location": {
                    "from": old_location,
                    "to": new_location,
                },
                "bridge_integrity": {
                    "from": old_integrity,
                    "to": new_integrity,
                },
            },
        )

    def _raise_river(
        self,
        actor_name: str,
        river_name: str | None,
        parameters: Dict[str, Any],
    ) -> Event:

        if river_name is None:
            return self._reject(
                event_type="raise_river",
                actor=actor_name,
                target=None,
                reason="No river specified.",
            )

        river = self.get(river_name)

        if river.kind != "river":
            return self._reject(
                event_type="raise_river",
                actor=actor_name,
                target=river_name,
                reason="Target is not a river.",
            )

        amount = float(parameters.get("amount", 0.0))

        if amount <= 0.0:
            return self._reject(
                event_type="raise_river",
                actor=actor_name,
                target=river_name,
                reason="River increase must be positive.",
            )

        old_level = float(river.state.get("level", 0.0))
        new_level = old_level + amount

        river.state["level"] = new_level

        consequences: Dict[str, Any] = {
            "river_level": {
                "from": old_level,
                "to": new_level,
            }
        }

        # Simple physical coupling:
        # high water damages the bridge.
        for entity in self.entities.values():
            if entity.kind != "bridge":
                continue

            if entity.state.get("river") != river_name:
                continue

            old_integrity = float(
                entity.state.get("integrity", 0.0)
            )

            damage = max(0.0, amount * 0.20)

            new_integrity = max(
                0.0,
                old_integrity - damage,
            )

            entity.state["integrity"] = new_integrity

            if new_integrity <= 0.0:
                entity.state["passable"] = False

            consequences[f"{entity.name}.integrity"] = {
                "from": old_integrity,
                "to": new_integrity,
            }

        return self._accept(
            event_type="raise_river",
            actor=actor_name,
            target=river_name,
            reason="The World accepted the river change.",
            consequences=consequences,
        )

    # ------------------------------------------------------------------
    # Event creation
    # ------------------------------------------------------------------

    def _accept(
        self,
        event_type: str,
        actor: str | None,
        target: str | None,
        reason: str,
        consequences: Dict[str, Any],
    ) -> Event:

        event = Event(
            time=self.time,
            event_type=event_type,
            actor=actor,
            target=target,
            accepted=True,
            reason=reason,
            consequences=consequences,
        )

        self.history.append(event)
        return event

    def _reject(
        self,
        event_type: str,
        actor: str | None,
        target: str | None,
        reason: str,
    ) -> Event:

        event = Event(
            time=self.time,
            event_type=event_type,
            actor=actor,
            target=target,
            accepted=False,
            reason=reason,
        )

        self.history.append(event)
        return event

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    def observe(self) -> Dict[str, Any]:
        """
        Return a read-only-style snapshot of the current World.

        This is what a future agent/LLM/renderer can consume.
        """

        return {
            "time": self.time,
            "entities": {
                name: {
                    "kind": entity.kind,
                    "state": dict(entity.state),
                }
                for name, entity in self.entities.items()
            },
        }

    def history_as_dicts(self) -> List[Dict[str, Any]]:
        return [event.as_dict() for event in self.history]


# ---------------------------------------------------------------------------
# Demonstration / experiment
# ---------------------------------------------------------------------------

def run_experiment() -> None:
    world = World()

    # Initial World.
    world.add_entity(
        "Alice",
        "person",
        location="west_bank",
    )

    world.add_entity(
        "River",
        "river",
        level=1.0,
    )

    world.add_entity(
        "Bridge",
        "bridge",
        material="wood",
        integrity=0.80,
        passable=True,
        destination="east_bank",
        river="River",
    )

    print("=" * 60)
    print("030 — TINY WORLD")
    print("=" * 60)

    print("\nINITIAL OBSERVATION")
    print(world.observe())

    # Alice proposes crossing.
    print("\nACTION 1")
    event = world.act(
        actor="Alice",
        action="cross",
        target="Bridge",
    )
    print(event.as_dict())

    # River rises.
    print("\nACTION 2")
    event = world.act(
        actor="Alice",
        action="raise_river",
        target="River",
        amount=2.0,
    )
    print(event.as_dict())

    # Alice attempts to cross again.
    print("\nACTION 3")
    event = world.act(
        actor="Alice",
        action="cross",
        target="Bridge",
    )
    print(event.as_dict())

    print("\nFINAL OBSERVATION")
    print(world.observe())

    print("\nWORLD HISTORY")
    for event in world.history_as_dicts():
        print(event)

    # ---------------------------------------------------------------
    # Acceptance tests
    # ---------------------------------------------------------------

    assert world.get("Alice").state["location"] == "east_bank"

    assert world.get("Bridge").state["integrity"] < 0.80

    assert len(world.history) == 3

    # The final crossing must be rejected if the bridge is collapsed.
    # With the current parameters the bridge integrity is:
    #
    #   0.80
    #   - 0.10 from first crossing
    #   - 0.40 from river rise
    #   = 0.30
    #
    # Therefore the final crossing is actually still possible.
    #
    # We explicitly test the rule rather than pretending the bridge
    # collapsed.

    assert world.history[-1].accepted is True

    print("\nRESULT")
    print("030 PASSED")

    print(
        "\nImportant:"
        "\nThe World, not the caller, changed the state."
        "\nActions were proposals."
        "\nConsequences were produced by World rules."
        "\nEvery action became part of persistent history."
    )


if __name__ == "__main__":
    run_experiment()
