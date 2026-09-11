"""
024 — The Last Rain
A mystery about a Maya city that slowly disappears.
"""
narrator = Narrator()
ix = Human("Ix")
balam = Human("Balam")
ahau = Human("Ahau")
nim = Human("Nim")
elena = Human("Elena")
city = Place("Maya city")
temple = Place("temple")
reservoir = Object("stone reservoir")
stela = Object("ancient stela")
maize = Object("maize field")
jar = Object("water jar")
door = Object("temple door")
ix.enter(city)
balam.enter(temple)
ahau.enter(temple)
nim.enter(city)
narrator.say("""
The rains had come late for three years.
The city still looked prosperous from the temple steps.
""")
ix.walk_to(reservoir).slowly()
ix.look_at(reservoir).closely()
ix.lower(jar).carefully()
jar.touches(reservoir)
ix.shakes(jar).gently()
narrator.say("""
The jar was empty.
""")
ahau.enters(temple)
ahau.look_at(reservoir).closely()
ahau.says("Open it.")
balam.opens(reservoir).slowly()
balam.look_inside(reservoir).carefully()
narrator.say("""
There was water at the bottom.
A thin reflection of the sky moved in it.
""")
ahau.look_inside(reservoir).closely()
ahau.closes(reservoir).quietly()
narrator.say("""
He closed the stone cover before anyone else could see.
""")
ix.look_at(ahau).closely()
ix.look_at(jar).quietly()
narrator.say("""
That evening, Ix carried her empty jar to the temple.
""")
ix.knocks_on(door).softly()
door.opens()
ix.enters(temple).quietly()
balam.looks_at(ix).carefully()
ix.walks_to(stela).slowly()
ix.touches(stela).gently()
balam.follows(ix).silently()
narrator.say("""
The newest inscription covered most of the old stone.
""")
balam.cleans(stela).carefully()
balam.look_at(stela).closely()
balam.stops()
narrator.say("""
Under the dust was a symbol he had never seen in the new records.
""")
balam.traces(symbol).slowly()
ix.points_at(stela)
narrator.say("""
The symbol appeared beside the ancient sign for water.
""")
balam.look_at(ix).sharply()
ix.look_at(door).quickly()
door.closes()
narrator.say("""
Someone was standing outside.
""")
balam.opens(door).quickly()
nobody.is_there()
balam.looks_down()
balam.sees(wet_footprints)
narrator.say("""
The footprints crossed the temple floor and disappeared at the stairs.
""")
balam.follows(footprints).quietly()
footprints.end_at(reservoir)
balam.look_at(reservoir).closely()
narrator.say("""
The stone cover was slightly open.
""")
balam.opens(reservoir).carefully()
balam.look_inside(reservoir).closely()
narrator.say("""
The water was lower than before.
""")
balam.looks_at(ahau).slowly()
ahau.stands_behind(balam)
ahau.says("You should forget what you saw.")
balam.looks_at(ahau).silently()
narrator.say("""
Balam did not answer.
""")
world.time.pass_days(20)
narrator.say("""
The fields became yellow.
The market became quiet.
The temple fires became fewer.
""")
nim.carries(jar).slowly()
nim.looks_at(maize).sadly()
nim.touches(maize).gently()
maize.breaks()
nim.looks_at(ahau)
ahau.looks_away()
narrator.say("""
People began leaving before the rulers announced that anyone should leave.
""")
ix.carries(jar)
balam.carries(stela_fragment)
nim.carries(seeds)
ix.leaves(city).slowly()
balam.leaves(city).quietly()
nim.leaves(city).quickly()
ahau.stays(temple)
narrator.say("""
The last people did not destroy the city.
They simply stopped living in it.
""")
world.time.pass_years(800)
elena.enters(city).carefully()
elena.stops()
elena.looks_at(temple).closely()
elena.walks_to(reservoir).slowly()
elena.touches(reservoir).gently()
elena.opens(reservoir).carefully()
elena.looks_inside(reservoir).closely()
narrator.say("""
There was no water.
Only dust and a small stone vessel at the bottom.
""")
elena.picks_up(stela).carefully()
elena.cleans(stela).slowly()
elena.looks_at(stela).closely()
narrator.say("""
Beneath centuries of dust, the old symbol was still there.
Beside it was another mark.
A line pointing west.
""")
elena.looks_west()
elena.walks_toward(hills).slowly()
narrator.say("""
She followed the direction until the ruins disappeared behind her.
""")
elena.stops()
elena.looks_back().quietly()
narrator.say("""
The city had not vanished in one disaster.

The people had left.

Why?

The stones could tell her that the water failed.
They could show her that the rulers knew.
They could show her that someone had prepared to leave.

But they could not tell her whether drought,
war, hunger, or something else had finally made the decision.

Perhaps the greatest mystery was not why the city died.

It was how many people escaped before it did.
""")
world.save()
