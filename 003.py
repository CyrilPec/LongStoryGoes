The room was quiet, and the boy sat beside the desk.
boy.state = "thinking"
A sentence waited unfinished on the screen.
sentence.state = "unfinished"
He looked at it, then slowly reached for the keyboard.
boy.write("The door was open.")
The words appeared, but something in the room changed.
door.state = "open"
He stopped typing.
boy.state = "listening"
Beyond the desk, the silence became different.
room.sound = "unknown"
He stood and walked toward the door.
boy.move(to=door)
The door was no longer only a sentence on the screen.
door.exists = True
He touched the handle.
boy.touch(door)
And somewhere beyond it, something waited.
door.open()
The room behind him became part of the story.
world.add(room)
He stepped through.
boy.enter(door)
The door closed without anyone touching it.
door.state = "closed"
He turned back, but his room was no longer there.
boy.look_at(door)
Only the sentence remained on the screen: **The door was open.**
sentence.state = "alive"
