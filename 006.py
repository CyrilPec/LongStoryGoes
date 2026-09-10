story_time = {
    "start": world.time,
    "end": None
}

hallway = Location(
    id="hallway",
    name="Hallway",
    geometry={
        "shape": "corridor",
        "width": 2.0,
        "length": 8.0,
        "height": 2.6
    },
    transform={
        "position": (0, 0, 0),
        "rotation": (0, 0, 0)
    },
    properties={
        "light": "dim",
        "sound": "absorbed"
    }
)
The hallway was narrow and dim, extending away from the door.
hallway.contains = []
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
        "position": (0, 7.5, 1.4),
        "rotation": (0, 0, 0)
    },
    appearance={
        "material": "glass",
        "transparent": True
    },
    state={
        "open": False,
        "boundary": "stable"
    }
)
The window stood at the far end of the hallway.
hallway.contains.append(window)
boy.location = hallway
boy.transform.position = (0, 0, 0)
boy.state = "alert"
He walked toward the window.
boy.move(
    to=window,
    speed=1.2
)
world.time = world.time + minutes(6)
world.history.append({
    "time": world.time,
    "event": "boy_reached_window",
    "location": hallway,
    "actors": [boy]
})
He looked through the glass and saw the room he had left.
boy.look_at(window)
window.view = room
window.state["boundary"] = "unstable"
room.relationships["visible_from"] = window
The desk was still beside the screen.
desk.location = room
screen.location = room
screen.state = "active"
sentence.state = "alive"
The words remained on the screen.
screen.contains = [sentence]
world.history.append({
    "time": world.time,
    "event": "original_room_visible_through_window",
    "location": hallway,
    "objects": [room, window, screen, sentence]
})
He placed his hand against the glass.
boy.touch(window)
world.time = world.time + seconds(1)
window.state["touched"] = True
Something touched the glass from the other side.
reflection = Object(
    id="boy_reflection",
    type="reflection",
    location=window,
    geometry={
        "shape": "human_silhouette"
    },
    appearance={
        "material": "reflection"
    },
    state={
        "independent": False,
        "motion_delay": 1.0
    },
    relationships={
        "source": boy
    }
)
window.contains = [reflection]
reflection.state["independent"] = True
reflection.respond_to(boy)
world.time = world.time + seconds(1)
world.history.append({
    "time": world.time,
    "event": "reflection_became_independent",
    "location": hallway,
    "actors": [boy, reflection]
})
The boy lowered his hand, but the reflection remained with its hand against the glass.
boy.lower_hand()
reflection.state["hand_position"] = "against_glass"
window.state["boundary"] = "unstable"
The hallway and the room were no longer completely separated.
window.relationships["connects"] = [hallway, room]
next_scene = Link(
    id="hallway_to_window",
    source=hallway,
    target="006.py",
    condition="boy touches the unstable window",
    time=world.time
)
story_time["end"] = world.time
world.history.append({
    "time": world.time,
    "event": "node_005_completed",
    "location": hallway,
    "actors": [boy],
    "links": [next_scene]
})
