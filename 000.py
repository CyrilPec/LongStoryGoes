"""
JOURNEY RULE 000
================
This is the first file of the journey.
It defines the fundamental architecture of the world.
CORE IDEA
---------
The world is a main character, always alive.
Stories happen in this world and are made of connected files.
The languages of the world are English and Python.
Each file represents one small place, scene, chapter, or situation.
A file may contain:
    - locations
    - objects
    - characters
    - relationships
    - physical rules
    - actions
    - consequences
    - links to other story files
Files may contain one location or several closely connected locations.
The story itself creates the map.
There is no requirement for one giant central world file.
THE WORLD MAP
-------------
Files are nodes.
Links between files are edges.
Example:
    chat_001.py
         |
         +----> chat_002.py
                    |
                    +----> chat_003.py
Another branch may exist, including links to previous files:
    chat_001.py
         |
         +----> chat_004.py
                    |
                    +----> chat_001.py
The world is therefore a living graph created by the journey.
LOCAL WORLDS
------------
Each file should describe only the place and situation necessary for
that part of the journey.
A file should be readable as a small D&D scene or manual page.
Example:
    location = "Old Tavern"
    door = Door(...)
    bartender = Character(...)
    story("""
    The bartender points toward the locked cellar door.
    """)
The next location can be reached through a story link.
PYTHON + ENGLISH
----------------
Python defines what the world CAN DO.
English describes what the world MEANS.
Do not add unnecessary empty lines.
Code should be written compactly where possible, like sentences,
to reduce scrolling without sacrificing readability.
Python should be used for:
    - state
    - relationships
    - physical behavior
    - rules
    - calculations
    - actions
    - consequences
    - inheritance
    - parameters
    - dependencies
English should be used for:
    - descriptions
    - intentions
    - narrative
    - explanations
    - discovered knowledge
    - context
OBJECTS
-------
Objects are not merely descriptions.
An object may contain its own behavior, values, parameters,
relationships, and physical rules.
Example:
    class Door:
        """
        A heavy wooden door.
        It rotates around two hinges.
        Fire weakens the wood.
        Excessive force can damage the hinges.
        """
        def pull(self, force):
            ...
Objects may inherit properties and behavior from other objects.
Example:
    class WoodenDoor(Door):
        material = "oak"
RELATIONSHIPS
-------------
Objects may reference other objects.
Examples:
    sword.belongs_to = player
    key.opens = cellar_door
    tavern.contains = [bartender, door]
    cellar.connected_to = underground_passage
Relationships are part of the world state and may change through play.
STORY LINKS
-----------
A story link connects one file to another.
Example:
    jump("002_cellar.py", reason="The player opens the cellar door")
Links may have conditions.
Example:
    jump("003_castle.py", condition="player possesses the silver key")
The links form the world map dynamically.
Objects and relationships may travel across story links when relevant.
PERSISTENCE
-----------
The journey is continuous even though it is divided into files.
A later file may receive relevant objects, characters, relationships,
knowledge, and consequences from previous files.
The author should not need to rewrite the entire world when creating
a new location.
A new location should be able to connect to the existing journey
through a story link.
The history of the journey is part of the world.
DESIGN PRINCIPLE
----------------
Keep the world distributed.
Keep locations small.
Keep objects meaningful and connected to the real world.
Keep relationships explicit.
Keep physics executable.
Keep descriptions understandable to humans and AI.
Use Python libraries and other dependencies when they improve the world.
Do not create abstractions merely for appearance.
Let the story create the map.
THE WORLD
---------
The world is not a passive container for stories.
The world itself is a main character.
It has state, history, relationships, physical rules, changes,
and consequences.
The world continues to exist beyond any single character or scene.
Characters may die.
Objects may be destroyed.
Locations may change.
Relationships may change.
Events may have permanent consequences.
THE AI
------
The AI is an agent inside this world.
It should be able to:
    1. Read the current story node.
    2. Understand its objects and relationships.
    3. Observe the situation.
    4. Choose an action.
    5. Execute or request the appropriate Python behavior.
    6. Observe the consequence.
    7. Continue the story.
    8. Follow links into new nodes.
The AI should not be restricted to a fixed menu of actions when
a physically plausible action can be expressed.
AI can attempt anything that can be meaningfully represented in the world.
The world decides the consequences.
FIRST RULE
----------
Do not build the entire world in advance.
Build the journey one connected file at a time.
AI can do anything.
Characters may die.
The world is a main character.
The map emerges from the story.
"""

 """



LongStoryGoes
=============

000 — The idea


This project starts with a simple question:

Can a story be written so that it is both ordinary English for a human
to read and Python that a computer can understand and use?

This is not meant to be a normal game engine.

It is an experiment.

The important part is the combination of English and Python in the same
file.

The English tells us what the world means.

Python tells us what the world can do.

Neither should completely replace the other.


THE CENTRAL IDEA
----------------

A LongStoryGoes file should still feel like a story when a human opens it.

For example:

    The old door stood at the end of the corridor.

    door = PhysicalObject("old door")

    The door was closed.

    Anna walked toward the door.

The exact Python syntax may change as the project develops.

What matters is the idea:

    English describes the story.
    Python gives the story structure, behaviour, memory and possibility.

The goal is NOT to turn the English into a collection of database records.

The goal is to discover how much of a living story can naturally exist
inside a Python file.


IMPORTANT
---------

LongStoryGoes is an experiment in writing stories that are simultaneously
readable English and executable Python.

The English is not merely output from the program, and Python is not merely
a game engine underneath it.

They are two views of the same story/world.


PLEASE DO NOT TURN THIS INTO A NORMAL GAME ENGINE
-------------------------------------------------

Do not replace the readable story with dictionaries, JSON-like schemas,
databases, or a separate simulation merely because they are easier to
program.

Do not assume that every piece of English must become a structured object.

Do not assume that everything needs to be formalised before a story can
be written.

Do not assume that the current concepts are the final architecture.

The project should remain free to discover better ideas in later files.

If a later story needs something that does not exist yet, that is useful.

The new file can experiment.

A concept can be changed.

A new concept can appear.

The idea is more important than the current architecture.


FIVE SIMPLE CONCEPTS
--------------------

The following five concepts are a useful way to understand the project.

They are NOT a rigid architecture.

They are simply a map.

1. WORLD

The World is the fictional reality shared by the story.

It contains whatever actually exists in that story:

people, animals, objects, places, time, relationships, events and states.

The World is not Blender.

The World is not the console.

The World is not the narrator's prose.

Those are ways of experiencing or presenting the World.


2. ENTITY

An Entity is something that exists in the World.

A human can be an Entity.

An animal can be an Entity.

A physical object can be an Entity.

A place can be treated as an Entity when the story needs to refer to it.

The exact boundaries are intentionally open to experimentation.


3. STATE

An Entity can have a State.

A door can be closed.

A person can be tired.

A fire can be burning.

A bridge can be broken.

State is what is true about something at a particular moment.

A story becomes interesting when states can change.


4. EVENT

An Event is something that actually happens in the World.

Anna may attempt to open a door.

If she succeeds, the door opening is an Event.

The Event can change State.

An Event can have a time, a place, an actor and a target.

An Action and an Event should not automatically be treated as the same thing.

An Action can be an attempt.

An Event is something that actually happened.

This distinction may become important later for a PC or AI.


5. OBSERVER

An Observer is something that experiences or knows only some part of
the World.

A human reader, a character, or a future PC may have an observation.

The World may contain more information than one Observer knows.

This makes it possible for two characters to exist in the same World while
having different knowledge of it.

The Narrator can then describe the story for the reader.

Narration is not necessarily the same thing as reality.

Observation is not necessarily the same thing as the whole World.


THE FIVE CONCEPTS ARE A LENS, NOT A CAGE
----------------------------------------

World, Entity, State, Event and Observer are useful because they simplify
the way we think about the project.

But later files are allowed to challenge this model.

For example:

    Is Time part of the World or something different?

    Is a Relationship an Entity or a fact between Entities?

    Is Memory part of an Observer?

    Is an Action a special kind of Event, or something that exists before
    an Event?

These questions are not mistakes.

They are part of the experiment.

The concept files 000-01.py, 000-02.py and so on explore such questions.

They should be read as experiments and thoughts, not as a rigid specification.


NARRATOR
--------

The Narrator communicates the story to the reader.

The Narrator does not have to be the World.

The Narrator can describe:

    what happened,
    what is happening,
    what an Observer sees,
    what a character remembers,
    or what the story means.

This distinction allows the same World to eventually be presented in
different ways:

    English
    another language
    console text
    TUI
    audio
    visualisation
    or something not yet imagined.


HUMAN AND PC
------------

A long-term question of LongStoryGoes is whether a human and a PC/AI
can participate in the same story.

They should not need separate realities.

The human reads the story.

The PC reads the story.

The World underneath them is the same.

The PC may observe, remember, reason, propose an Action, or participate
in an Event.

But the PC should not simply be allowed to declare a new reality because
its generated text says that something happened.

What actually happens must remain consistent with the World and its history.

This does NOT mean building a conventional game engine.

It means exploring what happens when a story itself becomes partly
executable.


THE PYTHON FILE
---------------

The .py file is an important part of the experiment.

It is simultaneously:

    a text file,
    a story,
    Python code,
    a possible World description,
    and potentially input for other tools.

A person should be able to open it and read the English.

Python should be used where it gives the story something useful:

    identity,
    behaviour,
    state,
    time,
    relationships,
    memory,
    events,
    actions,
    persistence,
    or visual information.

But there should be no requirement that every sentence become Python.

Freedom of expression is part of the experiment.


CONSOLE
-------

When a story file is run directly, the console can be a simple reader.

For example:

    $ python 016.py

    Rain tapped softly against the old window.

    Luna wandered into the quiet room.

    She curled up beside the window and listened to the rain.

The console is not necessarily a debugging tool.

It can simply be another way to experience the story.

The same underlying story may later be visualised.


VISUALISATION
-------------

v1_importer.py is one possible bridge from the Python story to a visual
representation.

It should not become the definition of what a story is.

The World should not exist merely because Blender can display it.

Instead:

    Story / World
          |
          +---- human reading
          |
          +---- console
          |
          +---- PC / AI
          |
          +---- visualisation
          |
          +---- future forms of presentation


HOW TO READ THE REST OF THE REPOSITORY
--------------------------------------

Start here.

Then read the concept files.

Then read the numbered story experiments.

Do not assume that the newest file is automatically more correct.

A later experiment may discover that an earlier idea was better.

A small story that exposes a weakness is valuable.

A new concept should appear because a story needs it, not because an
architecture diagram says that it should exist.


THE MOST IMPORTANT RULE
-----------------------

Keep the idea alive.

Do not optimise it away.

Do not make it conventional merely because conventional software
architecture is easier.

The project is trying to discover something.

The discovery is more important than having a perfect architecture today.


ONE LAST EXAMPLE
----------------

Imagine a story says:

    The glass fell from Anna's hand and shattered on the floor.

For a human, this is simply a sentence.

For LongStoryGoes, it may also mean:

    an Event happened,
    the glass changed State,
    Anna was the actor,
    the floor was the Place,
    time advanced,
    Anna may remember it,
    another Observer may have seen it,
    and the broken glass may still exist when the story continues.

The interesting question is not:

    "How do we build a game engine that handles this?"

The interesting question is:

    "How much of this can remain a natural story while Python gives
     the computer enough understanding to make it real?"


That is LongStoryGoes.
"""
