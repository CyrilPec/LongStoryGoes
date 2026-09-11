"""
017.py — The Stone by the Old Tree

Elias and the wolf meet near an old tree.

Elias discovers a strange black stone.
The wolf notices Elias, but does not notice the stone.

Later, the stone is gone.

Elias remembers what he saw.
The wolf remembers Elias standing near the tree.

The narrator knows what actually happened.

This story demonstrates that:

    World reality
        ↓
    Observation
        ↓
    Memory
        ↓
    Knowledge

Different observers can have different knowledge of the same event.
"""

from pathlib import Path
import importlib.util


ROOT = Path(__file__).parent


def load_concept(filename):
    path = ROOT / filename

    spec = importlib.util.spec_from_file_location(
        path.stem,
        path,
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


human_module = load_concept("000-02.py")
animal_module = load_concept("000-03.py")
observer_module = load_concept("000-06.py")
narrator_module = load_concept("000-05.py")
knowledge_module = load_concept("000-14.py")


Human = human_module.Human
Animal = animal_module.Animal
Observer = observer_module.Observer
Narrator = narrator_module.Narrator
Knowledge = knowledge_module.Knowledge


# ============================================================
# Characters
# ============================================================

elias = Human("Elias")
wolf = Animal("Wolf")

elias.knowledge = Knowledge()
wolf.knowledge = Knowledge()

elias.observer = Observer("Elias")
wolf.observer = Observer("Wolf")

narrator = Narrator()


# ============================================================
# The place
# ============================================================

old_tree = "the old tree"
forest_path = "the forest path"

stone = "a strange black stone"


# ============================================================
# Beginning
# ============================================================

narrator.narrate(
    "Late in the afternoon, Elias walked along the forest path."
)

narrator.narrate(
    "The path ended beside an old tree that stood alone in a clearing."
)

narrator.narrate(
    "Elias stopped beneath the tree when something dark caught his eye."
)


# ============================================================
# Elias discovers the stone
# ============================================================

elias_observation = elias.observer.observe(
    f"{stone} lies beneath {old_tree}."
)

elias.memory.append(elias_observation)

elias.knowledge.learn(
    f"{stone} lies beneath {old_tree}."
)

narrator.narrate(
    "Beneath the tree, Elias found a small black stone."
)

narrator.narrate(
    "It was unusually smooth and cold, although the afternoon was warm."
)


# ============================================================
# The wolf arrives
# ============================================================

narrator.narrate(
    "A wolf appeared at the edge of the clearing."
)

wolf_observation = wolf.observer.observe(
    "Elias is standing beneath the old tree."
)

wolf.memory.append(wolf_observation)

wolf.knowledge.learn(
    "Elias is standing beneath the old tree."
)

narrator.narrate(
    "The wolf watched Elias carefully."
)

narrator.narrate(
    "It saw Elias, but it did not see the small black stone."
)


# The wolf knows Elias is there.

assert wolf.knowledge.knows(
    "Elias is standing beneath the old tree."
)

# But the wolf does not know about the stone.

assert not wolf.knowledge.knows(
    f"{stone} lies beneath {old_tree}."
)


# ============================================================
# Elias leaves the stone
# ============================================================

narrator.narrate(
    "Elias placed the stone back beneath the tree."
)

elias.memory.append(
    f"{stone} was placed beneath {old_tree}."
)

elias.knowledge.learn(
    f"{stone} was placed beneath {old_tree}."
)

narrator.narrate(
    "He decided to return the next morning and look at it again."
)

narrator.narrate(
    "Then Elias left the clearing and continued down the forest path."
)


# ============================================================
# The wolf approaches the tree
# ============================================================

narrator.narrate(
    "After Elias disappeared along the path, the wolf entered the clearing."
)

wolf_observation = wolf.observer.observe(
    f"Elias has left {old_tree}."
)

wolf.memory.append(wolf_observation)

wolf.knowledge.learn(
    f"Elias has left {old_tree}."
)

narrator.narrate(
    "The wolf walked around the old tree."
)

narrator.narrate(
    "It sniffed the ground where Elias had been standing."
)


# ============================================================
# The stone disappears
# ============================================================

narrator.narrate(
    "A crow landed on a branch above the tree."
)

narrator.narrate(
    "The crow noticed the black stone on the ground."
)

narrator.narrate(
    "It flew down, picked up the stone, and disappeared into the forest."
)


# The narrator knows what happened.

narrator.narrate(
    "Neither Elias nor the wolf saw the crow take the stone."
)


# ============================================================
# The next morning
# ============================================================

narrator.narrate(
    "The next morning, Elias returned to the old tree."
)

elias_observation = elias.observer.observe(
    f"{stone} is no longer beneath {old_tree}."
)

elias.memory.append(elias_observation)

elias.knowledge.learn(
    f"{stone} is no longer beneath {old_tree}."
)

narrator.narrate(
    "The stone was gone."
)


# ============================================================
# Elias interprets what he knows
# ============================================================

narrator.narrate(
    "Elias searched the ground but found nothing."
)

narrator.narrate(
    "He remembered leaving the stone there the previous afternoon."
)

narrator.narrate(
    "He wondered whether the wolf had taken it."
)


# Important:
#
# Elias knows:
#     the stone was there
#     he left it beneath the tree
#     the stone is now gone
#
# Elias does NOT know:
#     the crow took it


assert elias.knowledge.knows(
    f"{stone} was placed beneath {old_tree}."
)

assert elias.knowledge.knows(
    f"{stone} is no longer beneath {old_tree}."
)

assert not elias.knowledge.knows(
    "The crow took the stone."
)


# ============================================================
# The wolf returns
# ============================================================

narrator.narrate(
    "The wolf appeared again at the edge of the clearing."
)

wolf_observation = wolf.observer.observe(
    "Elias is searching beneath the old tree."
)

wolf.memory.append(wolf_observation)

wolf.knowledge.learn(
    "Elias is searching beneath the old tree."
)

narrator.narrate(
    "The wolf watched Elias search the ground."
)


# The wolf also does not know about the crow.

assert not wolf.knowledge.knows(
    "The crow took the stone."
)


# ============================================================
# End
# ============================================================

narrator.narrate(
    "Elias looked at the wolf for a long moment."
)

narrator.narrate(
    "The wolf looked back at him."
)

narrator.narrate(
    "Neither of them knew what had happened to the stone."
)

narrator.narrate(
    "Only the narrator knew that a crow had carried it away."
)
