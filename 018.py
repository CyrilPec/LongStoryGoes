"""
018.py — A tiny persistent world

Purpose
-------
This file is an executable proof-of-concept for the core idea of LongStoryGoes:

    The world is authoritative.
    Characters observe the world.
    Characters propose actions.
    The world validates and executes those actions.
    Consequences become persistent state.
    Narrative is an observation of what actually happened.

The example contains:
    - 3 characters
    - 3 locations
    - several objects
    - persistent time
    - movement
    - observation
    - an actual action API
    - an irreversible event
    - leaving and re-entering a location
    - event history
    - deterministic execution
    - a small "agent" interface suitable for an LLM later

No LLM is used here deliberately.

The important property is that an agent cannot directly mutate world state.
It can only call World.act().
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Basic data
# ---------------------------------------------------------------------------


@dataclass
class Item:
    id: str
    name: str
    location: Optional[str] = None
    owner: Optional[str] = None
    state: str = "normal"
    exists: bool = True


@dataclass
class Character:
    id: str
    name: str
    location: str
    alive: bool = True
    inventory: List[str] = field(default_factory=list)


@dataclass
class Location:
    id: str
    name: str
    description: str
    exits: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Event:
    time: int
    actor: str
    action: str
    result: str


# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------


class World:
    """
    The only authority over the simulated world.

    External code should not modify characters, items or locations directly.
    It should use observe() and act().
    """

    def __init__(self) -> None:
        self.time: int = 0

        self.locations: Dict[str, Location] = {}
        self.characters: Dict[str, Character] = {}
        self.items: Dict[str, Item] = {}

        self.history: List[Event] = []

        self._build_world()

    # -----------------------------------------------------------------------
    # World construction
    # -----------------------------------------------------------------------

    def _build_world(self) -> None:
        self.locations["village"] = Location(
            id="village",
            name="Old Village",
            description="A small village beside a dark forest.",
            exits={
                "forest": "forest",
                "house": "house",
            },
        )

        self.locations["forest"] = Location(
            id="forest",
            name="Forest",
            description="A quiet forest. The trees are old and dense.",
            exits={
                "village": "village",
            },
        )

        self.locations["house"] = Location(
            id="house",
            name="Miller's House",
            description="A small wooden house at the edge of the village.",
            exits={
                "village": "village",
            },
        )

        self.characters["anna"] = Character(
            id="anna",
            name="Anna",
            location="village",
        )

        self.characters["boris"] = Character(
            id="boris",
            name="Boris",
            location="house",
        )

        self.characters["mira"] = Character(
            id="mira",
            name="Mira",
            location="forest",
        )

        self.items["lamp"] = Item(
            id="lamp",
            name="Oil Lamp",
            location="house",
        )

        self.items["axe"] = Item(
            id="axe",
            name="Woodcutter's Axe",
            location="forest",
        )

        self.items["bell"] = Item(
            id="bell",
            name="Village Bell",
            location="village",
        )

        self.items["bridge"] = Item(
            id="bridge",
            name="Old Wooden Bridge",
            location="forest",
            state="intact",
        )

    # -----------------------------------------------------------------------
    # Time
    # -----------------------------------------------------------------------

    def tick(self, minutes: int = 1) -> None:
        """
        Advance world time.

        Time is world state, not narrative decoration.
        """

        if minutes < 0:
            raise ValueError("Time cannot move backwards.")

        for _ in range(minutes):
            self.time += 1
            self._world_tick()

    def _world_tick(self) -> None:
        """
        Autonomous world behaviour.

        This is intentionally small, but this is where a larger world could
        simulate fire, weather, machines, NPC routines, decay, etc.
        """

        # The broken bridge does not magically repair itself.
        # This demonstrates persistence through time.

        pass

    # -----------------------------------------------------------------------
    # Observation
    # -----------------------------------------------------------------------

    def observe(self, character_id: str) -> Dict[str, Any]:
        """
        Return what a character can currently observe.

        This is deliberately different from returning the complete world.
        An agent should not automatically know things that are elsewhere.
        """

        character = self._character(character_id)

        location = self.locations[character.location]

        visible_characters = [
            {
                "id": c.id,
                "name": c.name,
                "alive": c.alive,
            }
            for c in self.characters.values()
            if c.location == character.location and c.id != character.id
        ]

        visible_items = [
            {
                "id": item.id,
                "name": item.name,
                "state": item.state,
            }
            for item in self.items.values()
            if (
                item.exists
                and item.location == character.location
                and item.owner is None
            )
        ]

        return {
            "time": self.time,
            "character": {
                "id": character.id,
                "name": character.name,
                "alive": character.alive,
                "inventory": [
                    self.items[item_id].name
                    for item_id in character.inventory
                    if self.items[item_id].exists
                ],
            },
            "location": {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "exits": dict(location.exits),
            },
            "characters": visible_characters,
            "items": visible_items,
        }

    # -----------------------------------------------------------------------
    # Action API
    # -----------------------------------------------------------------------

    def act(
        self,
        actor_id: str,
        action: str,
        target: Optional[str] = None,
        destination: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        The public action API.

        An LLM can eventually be given ONLY this interface.

        It cannot do:

            world.characters["anna"].location = "forest"

        It must do:

            world.act("anna", "move", destination="forest")

        The world decides whether that is legal.
        """

        actor = self._character(actor_id)

        if not actor.alive:
            return self._reject(actor_id, action, "Actor is dead.")

        if action == "wait":
            self.tick(1)
            return self._accept(actor_id, action, "Time advanced by one minute.")

        if action == "move":
            return self._move(actor, destination)

        if action == "take":
            return self._take(actor, target)

        if action == "drop":
            return self._drop(actor, target)

        if action == "ring":
            return self._ring(actor, target)

        if action == "break":
            return self._break(actor, target)

        if action == "look":
            return {
                "ok": True,
                "action": "look",
                "observation": self.observe(actor_id),
            }

        return self._reject(actor_id, action, "Unknown action.")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _move(
        self,
        actor: Character,
        destination: Optional[str],
    ) -> Dict[str, Any]:

        if destination is None:
            return self._reject(actor.id, "move", "No destination supplied.")

        current = self.locations[actor.location]

        if destination not in current.exits:
            return self._reject(
                actor.id,
                "move",
                f"{current.name} has no exit to {destination}.",
            )

        destination_id = current.exits[destination]

        # The bridge is a real world constraint.
        if (
            destination_id == "forest"
            and self.items["bridge"].state == "broken"
        ):
            return self._reject(
                actor.id,
                "move",
                "The bridge is broken. The forest cannot be reached this way.",
            )

        old_location = actor.location
        actor.location = destination_id

        self.tick(1)

        return self._accept(
            actor.id,
            "move",
            f"{actor.name} moved from {old_location} to {destination_id}.",
        )

    def _take(
        self,
        actor: Character,
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target is None:
            return self._reject(actor.id, "take", "No item supplied.")

        item = self.items.get(target)

        if item is None or not item.exists:
            return self._reject(actor.id, "take", "Item does not exist.")

        if item.owner is not None:
            return self._reject(actor.id, "take", "Item is already owned.")

        if item.location != actor.location:
            return self._reject(
                actor.id,
                "take",
                "Item is not at the actor's location.",
            )

        item.location = None
        item.owner = actor.id
        actor.inventory.append(item.id)

        self.tick(1)

        return self._accept(
            actor.id,
            "take",
            f"{actor.name} took {item.name}.",
        )

    def _drop(
        self,
        actor: Character,
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target is None:
            return self._reject(actor.id, "drop", "No item supplied.")

        if target not in actor.inventory:
            return self._reject(
                actor.id,
                "drop",
                "Actor does not possess that item.",
            )

        item = self.items[target]

        actor.inventory.remove(target)
        item.owner = None
        item.location = actor.location

        self.tick(1)

        return self._accept(
            actor.id,
            "drop",
            f"{actor.name} dropped {item.name}.",
        )

    def _ring(
        self,
        actor: Character,
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target != "bell":
            return self._reject(actor.id, "ring", "Only the village bell can ring.")

        if actor.location != "village":
            return self._reject(
                actor.id,
                "ring",
                "The bell is not here.",
            )

        self.tick(1)

        return self._accept(
            actor.id,
            "ring",
            "The village bell rings.",
        )

    def _break(
        self,
        actor: Character,
        target: Optional[str],
    ) -> Dict[str, Any]:

        if target != "bridge":
            return self._reject(
                actor.id,
                "break",
                "That object cannot be broken by this action.",
            )

        bridge = self.items["bridge"]

        if bridge.location != actor.location:
            return self._reject(
                actor.id,
                "break",
                "The bridge is not here.",
            )

        if bridge.state == "broken":
            return self._reject(
                actor.id,
                "break",
                "The bridge is already broken.",
            )

        if "axe" not in actor.inventory:
            return self._reject(
                actor.id,
                "break",
                "An axe is required.",
            )

        # ---------------------------------------------------------------
        # IRREVERSIBLE EVENT
        # ---------------------------------------------------------------

        bridge.state = "broken"

        self.tick(1)

        return self._accept(
            actor.id,
            "break",
            "The old wooden bridge breaks. "
            "This change is irreversible.",
        )

    # -----------------------------------------------------------------------
    # History
    # -----------------------------------------------------------------------

    def _accept(
        self,
        actor_id: str,
        action: str,
        result: str,
    ) -> Dict[str, Any]:

        event = Event(
            time=self.time,
            actor=actor_id,
            action=action,
            result=result,
        )

        self.history.append(event)

        return {
            "ok": True,
            "time": self.time,
            "action": action,
            "result": result,
        }

    def _reject(
        self,
        actor_id: str,
        action: str,
        reason: str,
    ) -> Dict[str, Any]:

        event = Event(
            time=self.time,
            actor=actor_id,
            action=action,
            result=f"REJECTED: {reason}",
        )

        self.history.append(event)

        return {
            "ok": False,
            "time": self.time,
            "action": action,
            "error": reason,
        }

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _character(self, character_id: str) -> Character:
        if character_id not in self.characters:
            raise KeyError(f"Unknown character: {character_id}")

        return self.characters[character_id]

    # -----------------------------------------------------------------------
    # Debug / narrative view
    # -----------------------------------------------------------------------

    def narrative(self) -> str:
        """
        Convert actual world history into a simple narrative.

        Notice that this function does not decide what happened.
        It only describes events that already happened.
        """

        if not self.history:
            return "Nothing has happened yet."

        lines = []

        for event in self.history:
            actor = self.characters[event.actor].name
            lines.append(
                f"[{event.time:03d}] {actor}: {event.result}"
            )

        return "\n".join(lines)

    def state(self) -> Dict[str, Any]:
        """
        Complete state snapshot.

        This is useful for debugging and persistence.
        It is NOT what an ordinary character should automatically observe.
        """

        return {
            "time": self.time,
            "characters": {
                character_id: {
                    "name": character.name,
                    "location": character.location,
                    "alive": character.alive,
                    "inventory": list(character.inventory),
                }
                for character_id, character in self.characters.items()
            },
            "items": {
                item_id: {
                    "name": item.name,
                    "location": item.location,
                    "owner": item.owner,
                    "state": item.state,
                    "exists": item.exists,
                }
                for item_id, item in self.items.items()
            },
            "history": [
                {
                    "time": event.time,
                    "actor": event.actor,
                    "action": event.action,
                    "result": event.result,
                }
                for event in self.history
            ],
        }


# ---------------------------------------------------------------------------
# Agent interface
# ---------------------------------------------------------------------------


class Agent:
    """
    A minimal interface for an LLM-controlled character.

    The important architectural rule:

        Agent -> World.act()

    never:

        Agent -> direct world mutation
    """

    def __init__(self, world: World, character_id: str):
        self.world = world
        self.character_id = character_id

    def observe(self) -> Dict[str, Any]:
        return self.world.observe(self.character_id)

    def act(
        self,
        action: str,
        target: Optional[str] = None,
        destination: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self.world.act(
            self.character_id,
            action,
            target=target,
            destination=destination,
        )


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------


def demo() -> None:
    """
    A complete tiny story.

    Anna:
        starts in the village
        enters the house
        takes the lamp
        leaves the house

    Boris:
        remains in the house

    Mira:
        starts in the forest
        has the axe
        breaks the bridge

    Anna later attempts to enter the forest.

    The important part:
        Anna cannot simply decide that the bridge still exists.
        The world says no.
    """

    world = World()

    anna = Agent(world, "anna")
    boris = Agent(world, "boris")
    mira = Agent(world, "mira")

    print("=" * 72)
    print("INITIAL WORLD")
    print("=" * 72)

    print(anna.observe())

    print("\n" + "=" * 72)
    print("ANNA ENTERS THE HOUSE")
    print("=" * 72)

    print(
        anna.act(
            "move",
            destination="house",
        )
    )

    print("\nAnna observes:")
    print(anna.observe())

    print("\n" + "=" * 72)
    print("ANNA TAKES THE LAMP")
    print("=" * 72)

    print(anna.act("take", target="lamp"))

    print("\n" + "=" * 72)
    print("ANNA LEAVES THE HOUSE")
    print("=" * 72)

    print(
        anna.act(
            "move",
            destination="village",
        )
    )

    print("\nAnna observes:")
    print(anna.observe())

    print("\n" + "=" * 72)
    print("MIRA BREAKS THE BRIDGE")
    print("=" * 72)

    print(
        mira.act(
            "take",
            target="axe",
        )
    )

    print(
        mira.act(
            "break",
            target="bridge",
        )
    )

    print("\nBridge state:")
    print(world.items["bridge"].state)

    print("\n" + "=" * 72)
    print("MIRA LEAVES THE FOREST")
    print("=" * 72)

    print(
        mira.act(
            "move",
            destination="village",
        )
    )

    print("\n" + "=" * 72)
    print("ANNA TRIES TO ENTER THE FOREST")
    print("=" * 72)

    result = anna.act(
        "move",
        destination="forest",
    )

    print(result)

    print("\n" + "=" * 72)
    print("BORIS IS STILL IN THE HOUSE")
    print("=" * 72)

    print(boris.observe())

    print("\n" + "=" * 72)
    print("WORLD NARRATIVE")
    print("=" * 72)

    print(world.narrative())

    print("\n" + "=" * 72)
    print("FINAL AUTHORITATIVE STATE")
    print("=" * 72)

    print(world.state())


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def self_test() -> None:
    """
    Small invariants that should always hold.

    These tests are important because the project is trying to make the
    world itself authoritative.
    """

    world = World()

    anna = Agent(world, "anna")
    mira = Agent(world, "mira")

    # Anna begins in the village.
    assert world.characters["anna"].location == "village"

    # Anna can enter the house.
    result = anna.act("move", destination="house")
    assert result["ok"]
    assert world.characters["anna"].location == "house"

    # Anna can take the lamp.
    result = anna.act("take", target="lamp")
    assert result["ok"]
    assert "lamp" in world.characters["anna"].inventory

    # Anna leaves.
    result = anna.act("move", destination="village")
    assert result["ok"]
    assert world.characters["anna"].location == "village"

    # Mira takes the axe.
    result = mira.act("take", target="axe")
    assert result["ok"]

    # Mira breaks the bridge.
    result = mira.act("move", destination="village")
    assert result["ok"]

    # Mira cannot break the bridge from the village.
    result = mira.act("move", destination="forest")
    assert result["ok"]

    result = mira.act("break", target="bridge")
    assert result["ok"]

    assert world.items["bridge"].state == "broken"

    # Leaving and re-entering does not restore the bridge.
    result = mira.act("move", destination="village")
    assert result["ok"]

    result = mira.act("move", destination="forest")
    assert not result["ok"]

    # The bridge remains broken.
    assert world.items["bridge"].state == "broken"

    # Time only moves forward.
    old_time = world.time
    world.tick(10)
    assert world.time == old_time + 10

    print("self_test: OK")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    self_test()
    print()
    demo()
