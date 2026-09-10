```python
"""
JOURNEY UPDATE 007
==================

The architecture defined in 000.py remains the foundation.

This update adds an important requirement discovered during the journey:

THE PYTHON WORLD MUST BE READABLE BY BLENDER 3D
------------------------------------------------

The Python files are not only narrative files.

They are structured descriptions of the world.

A future Blender importer must be able to read the Python world
representation and create a corresponding 3D scene.

Blender is therefore not the world itself.

The Python world model is authoritative.
Blender is one possible representation of that world.

WORLD OBJECTS
-------------

Objects should be defined as real world objects, not only as names
mentioned by the story.

A significant object may contain:

    - id
    - type
    - location
    - geometry
    - transform
    - appearance
    - properties
    - state
    - relationships
    - actions
    - physical rules

Example:

window = Object(
    id="hallway_window",
    type="window",
    location=hallway,
    geometry={
        "shape": "rectangle",
        "width": 1.2,
        "height": 1.8,
        "depth": 0.08
    },
    transform={
        "position": (0, 0, 1.4),
        "rotation": (0, 0, 0),
        "scale": (1, 1, 1)
    },
    appearance={
        "material": "glass",
        "transparent": True
    },
    state={
        "open": False,
        "broken": False
    }
)

The object has a stable identity.

The geometry describes what it is physically.

The transform describes where it exists.

The appearance describes how it may be represented.

The state describes its current condition.

The relationships connect it to the rest of the world.

BLENDER REPRESENTATION
----------------------

A future Blender importer may translate world objects into:

    Object       -> Blender Object
    geometry     -> Mesh / primitive geometry
    transform    -> location / rotation / scale
    appearance   -> Material
    location     -> Scene / Collection
    relationships -> references between Blender objects
    state        -> custom properties or runtime state

The story files themselves should not contain bpy code.

The world description must remain independent from Blender.

This keeps the world model usable by other future systems as well.

PERSISTENT OBJECTS
------------------

Objects created in earlier story nodes may continue to exist.

A later story file should reference an existing object when appropriate
instead of redefining the whole object.

A new object introduced by the current node should be explicitly defined.

The identity of an object must remain stable across story files.

Example:

boy
door
room
screen
sentence

may continue from earlier nodes.

A new object such as:

hallway_window

must receive its own definition.

TIME
----

The world continues to exist independently of observation.

Each story node should preserve world time.

A node may define:

    story_time = {
        "start": "...",
        "end": "..."
    }

Actions that consume time should change the world time.

Important events should become part of world history.

The world state at the end of one node becomes part of the
starting state available to later nodes.

ENGLISH + PYTHON
----------------

The hybrid language remains unchanged.

Python defines what the world can do.

English describes what the world means.

English should not simply repeat the Python statement.

For example:

boy.open(door)

should not be followed by:

"The boy opened the door."

Instead, English should add information that Python alone does not express:

The darkness beyond the doorway seemed deeper than the hallway behind him.

The next Python statement may then describe a consequence of that
observation.

The two languages therefore carry different but connected information.

OBJECTS AS PROGRAMMING-LANGUAGE OBJECTS
----------------------------------------

An object is more than a description.

It behaves like an object in a programming language.

An object may have:

    properties
    state
    functions
    relationships
    dependencies
    physical behavior
    history
    representation

The same object may therefore be understood simultaneously as:

    a thing in the world
    a story element
    a program object
    a persistent world entity
    a future 3D object

This is an important part of the LongStoryGoes architecture.

DISTRIBUTED WORLD
-----------------

The new Blender requirement does not change the distributed-world rule.

There should still be no giant manually constructed world file.

The journey continues to create the world one node at a time.

Each story file adds only the objects, relationships, events and
locations required by that part of the journey.

The resulting world is a graph.

Files are nodes in the journey.

Objects and relationships connect the nodes.

The future Blender representation is generated from this accumulated
world structure.

CORE PRINCIPLE
--------------

The story file is not a screenplay for Blender.

It is a world definition written in a hybrid language.

English gives meaning.

Python gives structure and behavior.

World state gives continuity.

Relationships create the graph.

Time creates history.

A future importer can transform that world into 3D.

Therefore:

    Story -> World Model -> Blender Representation

and not:

    Story -> Blender

The world comes first.

The representation comes second.

NEXT DEVELOPMENT
-----------------

The next architectural task is to define a small and stable object
model that story files can use consistently.

The core model should probably define concepts such as:

    World
    Location
    Object
    Character
    Relationship
    Action
    Event
    Link

Story files should then instantiate these concepts rather than
inventing a different structure for every scene.

However, the model should remain small.

Do not build the entire engine in advance.

The journey continues to define the architecture through actual story.

The world should emerge from the story.
"""
```
