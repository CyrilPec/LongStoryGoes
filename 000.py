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

