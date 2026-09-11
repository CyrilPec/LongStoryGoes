teacher = Human("Mara")
anna = Human("Anna")
leo = Human("Leo")
classroom = Place("classroom")
chair = Object("chair")
chalk = Object("chalk")

teacher.move_to(classroom)
anna.move_to(classroom)
leo.move_to(classroom)

"""
The lesson was almost over.
Mara was writing on the board.
"""

anna.push(leo)
leo.step_back()
leo.hit(chair)
chair.fall()

teacher.separate(anna, leo)

"""
Neither pupil agrees about who started the fight.
Mara saw only the end.
"""

anna.remember(anna.push(leo))
leo.remember(anna.push(leo))

teacher.look_at(chair)
teacher.pick_up(chalk)

"""
There was blue chalk dust beneath the chair.
Mara did not know why.
"""

leo.look_at(chair)
leo.remember(leo.saw(chair))

teacher.leave(classroom)
anna.leave(classroom)

"""
The chair remained where it had fallen.
"""
