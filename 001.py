"""
JOURNEY RULE 001
================
TIME AND CONTINUITY
The world has its own time.
Characters, objects, locations, and events exist within that time.
Characters may be born, live, travel, change, and die.
Events have a time and may permanently change the world.
Story files do not necessarily represent chronological order.
A file represents a location or situation, while world time determines
when that situation exists.
A character who dies remains dead unless the world itself provides
a valid mechanism that changes this condition.
Past events cannot be silently forgotten.
Future events have not happened yet.
The world continues to change even when the player is absent.
TIME
----
Time is part of the world state.
Example:
    world.date = "Day 1"
    world.time = "07:42"
Time may pass because of:
    - travel
    - actions
    - waiting
    - sleep
    - combat
    - physical processes
    - world events
Characters have their own temporal history.
Example:
    character.birth = "Day -7200"
    character.alive = True
    character.location = "Old Station"
If a character dies:
    character.alive = False
    character.death_time = world.time
    character.death_location = character.location
The death becomes part of the world's history.
CONTINUITY
----------
The same character, object, or location may appear in multiple files.
The system must distinguish between:
    - what exists
    - where it exists
    - when it exists
    - what happened to it
A story file describes a point or interval in the world's timeline.
A later file may depend on consequences from an earlier file.
A previous file may be revisited when the story permits it.
WORLD ACTIVITY
--------------
The player is not the center of time.
The world may continue while the player is absent.
Examples:
    - fire continues burning
    - machines continue operating
    - characters travel
    - plants grow
    - weather changes
    - animals move
    - conflicts continue
    - characters may live or die
    - objects may decay or be destroyed
The world is a main character and has its own history.
STORY FILES
-----------
Each story file may define:
    - starting time
    - ending time
    - location
    - local events
    - characters present
    - objects present
    - changes to the world
    - links to other files
Example:
    story_time = {
        "start": "Day 1 07:42",
        "end": "Day 1 08:15"
    }
A link between files may therefore represent movement through
space, time, or both.
Example:
    jump(
        "002_cellar.py",
        reason="The player opens the cellar door",
        time="Day 1 08:16"
    )
HISTORY
-------
Important changes should become part of persistent world history.
Example:
    world.history.append({
        "time": world.time,
        "event": "The cellar door was opened",
        "location": "Old Tavern",
        "actors": [player]
    })
History can be used by future story files and AI agents.
DEATH
-----
Death is a real world event.
A character can die.
Death affects relationships, locations, objects, knowledge,
and future events.
The story should not automatically protect important characters.
No character is guaranteed to survive.
The consequences of death belong to the world.
TIME AND THE AI
---------------
The AI must consider time when reasoning about the world.
It should be able to determine:
    - where a character was
    - where a character is
    - where a character may be later
    - whether a character is alive
    - what events have already happened
    - what events have not happened
    - how much time an action requires
The AI should not know future events unless the world provides
a legitimate reason for that knowledge.
FIRST TEMPORAL PRINCIPLE
------------------------
The world exists before the player observes it.
The world continues after the player leaves it.
Time does not exist merely to measure the player's actions.
Time is a property of the world itself.
"""
