# LongStoryGoes — Development Log

## Current Architecture

Repository:

`CyrilPec/LongStoryGoes`

[LongStoryGoes on GitHub](https://github.com/CyrilPec/LongStoryGoes?utm_source=chatgpt.com)

Current files:

* `000.py` — fundamental world architecture
* `001.py` — time and continuity
* `002.py` and later files will be created as the story develops.

The project is **not intended to contain a complete world designed in advance**.

The world should grow through the journey:

`000 → 001 → 002 → 003 → ...`

Each new file adds another piece of the world, another situation, place, event, character, object, relationship, rule, or consequence.

---

## Story Concept

The story should begin as an ordinary situation.

For example:

A boy is in his room.

He begins writing a story.

But the important idea is that **the story he writes becomes connected to the world he is in**.

As he continues writing, the boundary between:

* the real room,
* the written story,
* the described world,
* and the world experienced by the character

can gradually disappear.

The boy does not simply tell the reader a story.

**He enters the story.**

The journey itself creates the world.

The later files should therefore not be treated as independent fictional chapters. They are successive states/nodes of one growing world.

---

## Important Rule

Do not write a predetermined large story outline.

Do not decide in advance what the entire journey will be.

Instead:

**Start small.**

Create the first situation.

Then allow the next event to determine what needs to exist next.

Then create the next file.

Then the next.

The structure of the world should emerge from the journey.

---

## File Philosophy

Each story file is a world node.

A file may describe:

* a location
* characters
* objects
* relationships
* physical conditions
* actions
* events
* consequences
* knowledge
* time
* connections to other files

Python can define what exists and what can happen.

English can describe what those things mean.

The files together form a growing world graph.

```text
001
 |
002
 |
003
 |
004
 |
...
```

But the graph does not have to remain linear.

Later the journey may produce:

```text
        002
       /   \
     003   004
      |     |
     005   006
       \   /
        007
```

The story creates its own map.

---

## Character Journey

The protagonist should be able to move from being:

**observer → writer → participant → character inside the world**

The transition should happen naturally through the story.

The world should not simply announce:

> "You are now inside the story."

Instead, the distinction between writing and reality should gradually become questionable through actual events.

The written description can begin affecting what exists.

What the protagonist writes may become a description of a place.

That place may become accessible.

Objects described in the story may acquire existence.

Relationships described in the story may become real relationships.

Eventually the protagonist can discover that he is no longer merely writing about the world.

**He is inside it.**

---

## World Continuity

Time is part of the world.

Events have consequences.

Characters and objects persist.

A later file must inherit the relevant state established by earlier files.

Nothing important should disappear simply because the story moved to another file.

The world continues to exist even when the protagonist is not observing it.

---

## Future 3D Realization

The story is also intended to become a source for real 3D scenes.

The long-term direction is:

```text
Story files
     ↓
World / scene interpretation
     ↓
Blender importer
     ↓
Real 3D scene
```

A future **Blender 3.6 add-on** will import the story files.

Possible mappings:

```text
story location       → Blender scene / collection
story object         → Blender object
object parameters    → transforms / geometry / materials / properties
relationships        → spatial or logical connections
world state          → scene state
```

The story system itself must remain independent of Blender.

Blender is a **realization layer**, not the foundation of the world model.

The long-term goal is that a description written in the story can eventually become something that actually exists visually and spatially in Blender.

---

## Future Design Principle

As the project develops, we should distinguish between:

1. **Narrative meaning**
2. **World structure**
3. **Executable behavior**
4. **3D realization**

This may eventually lead to objects having programming-language-like structures:

```text
Object
 ├── properties
 ├── state
 ├── relationships
 ├── functions / actions
 └── physical representation
```

But this structure should emerge gradually rather than being over-designed at the beginning.

---

## Current Next Step

Do not modify the whole architecture unnecessarily.

Continue the journey with:

`002.py`

Then add `003.py`, `004.py`, etc. as required by what happens.

The story should determine what the next file needs to contain.

**The world is built by the journey.**
