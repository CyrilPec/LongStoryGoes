"""
LongStoryGoes — 021

THE FLOWER

This is a small experiment with:

    Entity
    Time
    State
    Story

A flower is an Entity.

The story can move forward by different periods of time.

The flower does not have to behave the same way for every period.

The kind of Entity can determine how it changes as time passes.

This is not an aging framework.

It is an experiment:

    What happens when a story simply says that time has passed?

The important thing is that the story remains readable.
"""


from datetime import date, timedelta


# ---------------------------------------------------------------------------
# A small Entity
# ---------------------------------------------------------------------------


class Flower:
    def __init__(self, name, species, planted):
        self.name = name
        self.species = species
        self.planted = planted
        self.age = timedelta(0)
        self.state = "alive"

    def time_passes(self, period):
        self.age += period

        # The rules belong to this particular kind of Entity.
        #
        # A poppy is short-lived.
        # The story does not need to know this in advance.

        if self.species == "poppy":
            if self.age >= timedelta(days=120):
                self.state = "gone"
            elif self.age >= timedelta(days=7):
                self.state = "flowering"

        elif self.species == "oak":
            if self.age >= timedelta(days=365 * 30):
                self.state = "large tree"
            elif self.age >= timedelta(days=365 * 3):
                self.state = "young tree"


# ---------------------------------------------------------------------------
# The story begins.
# ---------------------------------------------------------------------------


today = date(2026, 9, 11)

anna = "Anna"

flower = Flower(
    name="Red flower",
    species="poppy",
    planted=today,
)


print("The Flower")
print()
print("It was a warm morning.")
print()
print("Anna planted a red flower beside the garden wall.")
print()


# ---------------------------------------------------------------------------
# One day passes.
# ---------------------------------------------------------------------------


period = timedelta(days=1)

today += period
flower.time_passes(period)

print("One day passed.")
print()

print(f"The flower was still {flower.state}.")
print()


# ---------------------------------------------------------------------------
# A longer period passes.
# ---------------------------------------------------------------------------


period = timedelta(days=10)

today += period
flower.time_passes(period)

print("Ten more days passed.")
print()

print(f"The flower was now {flower.state}.")
print()


# ---------------------------------------------------------------------------
# A much longer period passes.
#
# The same Entity continues to exist in the story,
# but time has changed its state.
# ---------------------------------------------------------------------------


period = timedelta(days=120)

today += period
flower.time_passes(period)

print("One hundred and twenty days passed.")
print()

print(f"The flower was now {flower.state}.")
print()


# ---------------------------------------------------------------------------
# Anna returns.
# ---------------------------------------------------------------------------


print("Anna returned to the garden.")
print()


if flower.state == "gone":
    print("The flower was no longer there.")
else:
    print("The flower was still growing beside the wall.")


print()
print("Anna remembered planting it.")
