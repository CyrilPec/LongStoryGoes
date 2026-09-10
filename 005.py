"""
STORY NODE 005
==============

The hallway beyond the door.

This node continues directly from 003.py.
The world time continues from the previous node.
Objects introduced here are explicitly defined before they are used.
"""

story_time = {
"start": world.time,
"end": world.time
}
The hallway was narrower than the boy remembered, although he could no longer remember having been there before.
hallway = Location(
name="hallway",
properties={
"width": "narrow",
"light": "dim",
"sound": "absorbed",
"exists": True
},
state="quiet"
)
There were no pictures on the walls, only a single window at the far end.
window = Object(
name="window",
type="window",
location=hallway,
properties={
"transparent": True,
"state": "closed",
"view": None
}
)
The boy remained connected to the room he had left, even though the room itself was no longer behind him.
boy.location = hallway
boy.state = "alert"
boy.relationships["inside"] = hallway
He walked forward, and his footsteps became quieter instead of returning from the walls.
boy.move(to=window)
hallway.properties["sound"] = "absorbed"
hallway.state = "silent"
The silence was not the absence of sound. It seemed to take the sound away.
world.time = world.time + minutes(1)
world.history.append({
"time": world.time,
"event": "The boy entered the hallway and discovered that sound was absorbed by it.",
"location": hallway,
"actors": [boy]
})
He stopped beside the window and looked through the glass.
boy.look_at(window)
window.properties["view"] = room
Beyond the glass was the room he had just left.
room.location = "beyond_window"
room.relationships["visible_from"] = window
The desk was still there, but the boy was not sitting beside it anymore.
desk.state = "empty"
desk.location = room
The screen remained on.
screen.state = "active"
screen.relationships["contains"] = [sentence]
The sentence was still there, exactly as he had written it.
sentence.state = "alive"
sentence.properties["text"] = "The door was open."
He understood that the room was not behind him anymore. It had become somewhere else.
window.relationships["shows"] = room
window.properties["view_type"] = "displaced_room"
The glass reflected his face.
reflection = Object(
name="reflection",
type="reflection",
location=window,
properties={
"state": "sitting",
"delay": seconds(0),
"independent": False,
"source": boy
}
)
The reflection was not standing where he was standing.
reflection.location = room
reflection.relationships["source"] = boy
reflection.state = "sitting"
He raised his hand.
boy.raise_hand()
reflection.properties["delay"] = seconds(1)
The reflection raised its hand one second later.
reflection.respond_to(boy)
world.time = world.time + seconds(1)
reflection.state = "raised_hand"
For a moment neither of them moved.
boy.state = "waiting"
reflection.state = "still"
The boy lowered his hand, but the reflection did not.
boy.lower_hand()
reflection.state = "still"
The difference between them had become part of the room.
world.history.append({
"time": world.time,
"event": "The reflection acted independently of the boy.",
"location": hallway,
"actors": [boy, reflection]
})
He wondered whether he had entered the story or whether the story had entered him.
boy.knowledge.add("The reflection can behave independently.")
The hallway remained connected to the door behind him.
hallway.relationships["connected_to"] = door
door.relationships["leads_to"] = hallway
But the window offered another direction, and that direction led back to the room.
window.relationships["leads_to"] = room
The boy placed his hand against the glass.
boy.touch(window)
window.state = "touched"
Something on the other side touched the glass at exactly the same place.
reflection.touch(window)
reflection.state = "touching"
The two sides of the window were no longer behaving as separate spaces.
window.properties["boundary"] = "unstable"
world.history.append({
"time": world.time,
"event": "The window became an unstable boundary between the hallway and the room.",
"location": hallway,
"actors": [boy, reflection]
})
The boy did not open the window.
boy.state = "observing"
The story had given him another direction, but it had not yet decided what was beyond it.
next_scene = Link(
target="006.py",
condition="boy touches the window",
reason="The window has become an unstable boundary between two spaces",
time=world.time
)
story_time["end"] = world.time
world.history.append({
"time": world.time,
"event": "Story node 005 completed.",
"location": hallway,
"actors": [boy],
"links": [next_scene]
})
"""

# CONTINUITY

# The following objects persist into later nodes when they remain relevant:

# boy

# door

# room

# desk

# screen

# sentence

# hallway

# window

# reflection

#

# The world remembers:

# - the boy left his original room

# - the original room is visible through the hallway window

# - the sentence "The door was open." remains alive on the screen

# - the reflection is capable of independent behavior

# - the window has become an unstable boundary

# - world time has advanced

"""
