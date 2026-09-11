"""
023 — The Wrong Story
A boy fight, seen from the wrong side.
"""

narrator = Narrator()

mara = Human("Mara")
sam = Human("Sam")
daniel = Human("Daniel")

classroom = Place("classroom")
corridor = Place("corridor")
desk = Object("desk")
backpack = Object("Daniel's backpack")
notebook = Object("notebook")
window = Object("window")

mara.enter(classroom)
sam.enter(classroom)
daniel.enter(classroom)

narrator.say("""
The last bell had already rung.
Only three people remained in the school.

Sam was putting his books into his bag.
Daniel had returned for something he had forgotten.

Neither boy expected the other to be there.
""")

daniel.look_at(backpack)
sam.look_at(notebook)

narrator.say("""
Sam recognized the notebook immediately.

He had found it the day before beneath his desk.
Daniel had never asked for it back.
""")

sam.take(notebook)
daniel.reaches_for(notebook)

narrator.say("""
Daniel did not explain.

Sam saw his hand moving toward the notebook
and understood the movement as an accusation.
""")

sam.pull_back(notebook)
daniel.grabs(sam)
sam.push(daniel)
daniel.push(sam)
sam.hits(desk)
desk.moves()
daniel.stumbles()
daniel.hits(window)
window.shakes()

mara.enter(classroom)
mara.separates(sam, daniel)

narrator.say("""
Mara arrived in time to see Daniel against the window
and Sam holding the notebook.

She saw the end.

The end looked simple.
""")

mara.look_at(sam)
mara.look_at(daniel)

sam.says("He attacked me.")
daniel.says("He took my notebook.")

narrator.say("""
Both boys were telling the truth.

Neither boy was telling the whole truth.
""")

mara.look_at(notebook)
mara.look_at(daniel)

daniel.points_at(notebook)

narrator.say("""
Daniel pointed to a name written inside the cover.

It was his name.

Sam looked at it for the first time.
""")

sam.read(notebook)

narrator.say("""
The notebook had been lying under Sam's desk yesterday.

Sam had assumed Daniel had abandoned it.

Daniel had spent the morning looking for it.

A misunderstanding had been growing quietly for a whole day.
""")

sam.remembers(yesterday)
daniel.remembers(yesterday)

narrator.say("""
Then Sam remembered something else.

Yesterday, Daniel had stood beside his desk
and looked underneath it.

Sam had thought Daniel was watching him.

Daniel had been looking for the notebook.
""")

sam.remembers(daniel.looked_under_desk)

narrator.say("""
The boys looked at each other.

The fight suddenly had a different beginning.
""")

sam.apologizes()
daniel.apologizes()

mara.look_at(both)

narrator.say("""
Mara still did not know who pushed first.

For once, she decided that knowing everything
was not necessary to understand something.

The boys had fought because each had mistaken
the other's actions for something they were not.
""")

sam.return(notebook)
daniel.take(notebook)

sam.leave(classroom)
daniel.leave(classroom)
mara.leave(classroom)

narrator.say("""
In the corridor, the boys walked in the same direction.

They were not friends.

But they were no longer carrying the same story.
""")

world.save()
