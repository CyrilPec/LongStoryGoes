```python
"""
STORY NODE 008
==============
THE OTHER SIDE OF THE WINDOW
This node continues from 006.py and 007.py.
The boy remains in the hallway.
The hallway window is an unstable boundary.
The reflection is no longer behaving as a passive reflection.
"""
story_time = {
    "start": world.time,
    "end": None
}
The boy stood with his hand against the glass, while the figure on the other side kept its hand in exactly the same place.
boy.state = "observing"
reflection.state["hand_position"] = "against_glass"
window.state["boundary"] = "unstable"
The glass was still transparent, but transparency no longer meant that the two spaces were separate.
window.relationships["separates"] = False
window.relationships["connects"] = [hallway, room]
The reflection looked directly at him.
reflection.look_at(boy)
boy.state = "uncertain"
It was not the movement that frightened him, but the fact that he had not made it happen.
reflection.state["attention"] = boy
The boy moved his hand away from the glass.
boy.lower_hand()
world.time = world.time + seconds(1)
The reflection did not move.
reflection.state["hand_position"] = "against_glass"
world.history.append({
    "time": world.time,
    "event": "reflection_did_not_follow_boy",
    "location": hallway,
    "actors": [boy, reflection]
})
He took one step backward.
boy.move(
    to=hallway,
    speed=0.5
)
The reflection remained where it was.
reflection.state["position"] = "at_window"
For the first time, the boy could see the difference between an image and a thing.
boy.knowledge.add("The reflection can occupy its own state.")
The reflection placed its other hand against the glass.
reflection.touch(window)
world.time = world.time + seconds(1)
Both hands were now pressed against the same surface from opposite sides.
window.state["boundary"] = "active"
window.state["pressure"] = "matched"
The glass did not crack. Instead, the surface between them became strangely shallow, as if there were no depth inside it at all.
window.geometry["depth"] = 0.001
The boy reached toward it again, but this time the glass felt warm.
boy.touch(window)
window.state["touched_by"] = [boy, reflection]
Something answered from the other side.
reflection.touch(window)
reflection.state["response"] = "immediate"
The window was no longer only showing the room. It was accepting contact between the two spaces.
window.relationships["boundary_between"] = [hallway, room]
window.relationships["contact"] = [boy, reflection]
world.history.append({
    "time": world.time,
    "event": "window_became_contact_boundary",
    "location": hallway,
    "actors": [boy, reflection],
    "objects": [window]
})
The boy looked toward the room beyond the glass.
boy.look_at(room)
The desk and screen were exactly where he had left them, but the room now seemed deeper than it had been before.
room.properties["depth"] = "unknown"
screen.state = "active"
sentence.state = "alive"
The sentence remained on the screen: "The door was open."
screen.contains = [sentence]
The words had not changed, but the boy suddenly understood that they were not describing the past.
sentence.properties["meaning"] = "current"
The reflection turned toward the screen.
reflection.look_at(screen)
boy.state = "still"
For a moment, both sides of the window were looking at the same sentence.
reflection.knowledge.add("The sentence is current.")
The boy did not know how the reflection could understand the words.
boy.knowledge.add("The reflection can perceive the sentence.")
The reflection raised one finger and pointed toward the screen.
reflection.point_to(sentence)
world.time = world.time + seconds(1)
The boy followed the gesture.
boy.look_at(sentence)
The sentence was unchanged, but a new space appeared beneath it on the screen.
screen.state["new_space"] = True
A cursor began blinking below the sentence.
cursor = Object(
    id="screen_cursor",
    type="cursor",
    location=screen,
    geometry={
        "shape": "line",
        "width": 0.02,
        "height": 0.18,
        "depth": 0.001
    },
    appearance={
        "material": "light"
    },
    state={
        "visible": True,
        "blinking": True
    },
    relationships={
        "screen": screen,
        "sentence": sentence
    }
)
screen.contains.append(cursor)
The boy had not touched the keyboard.
boy.state = "waiting"
The cursor continued blinking.
cursor.state["active"] = True
The reflection moved closer to the screen.
reflection.move(
    to=screen,
    speed=0.5
)
world.time = world.time + seconds(2)
The hallway behind the boy remained unchanged, but the way back through the window no longer felt like the same journey.
hallway.state = "changed"
hallway.properties["return_path"] = "uncertain"
The boy understood that the window had become a choice rather than an object.
window.state["function"] = "passage"
world.history.append({
    "time": world.time,
    "event": "window_became_possible_passage",
    "location": hallway,
    "actors": [boy, reflection],
    "objects": [window]
})
He stepped closer to the glass.
boy.move(
    to=window,
    speed=0.5
)
The reflection waited on the other side.
reflection.state["waiting_for"] = boy
The distance between them was now only the thickness of the glass.
window.state["crossing_possible"] = True
The boy raised his hand once more.
boy.raise_hand()
The reflection raised its hand first.
reflection.raise_hand()
world.time = world.time + seconds(1)
Their hands met at the boundary.
boy.state = "contact"
reflection.state = "contact"
window.state["boundary"] = "open"
The glass did not disappear. The boundary simply stopped behaving like glass.
window.state["material_behavior"] = "passable"
The boy stepped forward.
boy.enter(window)
boy.location = room
world.time = world.time + seconds(2)
The hallway remained behind him.
hallway.state = "behind"
The room was around him again, but it was no longer the room he had left.
room.state = "entered_again"
room.properties["entry_method"] = "through_window"
world.history.append({
    "time": world.time,
    "event": "boy_crossed_window_boundary",
    "location": room,
    "actors": [boy],
    "objects": [window]
})
The reflection was no longer visible in the glass.
reflection.location = room
reflection.state["position"] = "beside_screen"
The boy turned toward it.
boy.look_at(reflection)
The reflection stood beside the screen, facing him without moving.
reflection.state["independent"] = True
The sentence remained between them.
sentence.state = "alive"
screen.contains = [sentence, cursor]
The cursor blinked once.
cursor.state["blink_count"] = cursor.state.get("blink_count", 0) + 1
Then the screen displayed a new empty line.
screen.state["input_available"] = True
The boy understood that the story had not ended when he entered the room.
boy.knowledge.add("The story can continue from inside the written world.")
next_scene = Link(
    id="room_to_next",
    source=room,
    target="009.py",
    condition="boy is inside the room and the reflection is independent",
    reason="The written world has become an active place",
    time=world.time
)
story_time["end"] = world.time
world.history.append({
    "time": world.time,
    "event": "node_008_completed",
    "location": room,
    "actors": [boy, reflection],
    "links": [next_scene]
})
"""
CONTINUITY
----------
Persistent objects:
    boy
    door
    room
    desk
    screen
    sentence
    hallway
    window
    reflection
    cursor
Important world changes:
    - the reflection is independently active
    - the window became a passable boundary
    - the boy crossed from the hallway back into the room
    - the room is no longer identical to the room he originally left
    - the sentence remains alive
    - the screen can now accept new input
    - the reflection is inside the room with the boy
    - the journey continues toward 009.py
"""
```
