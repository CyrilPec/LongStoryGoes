"""
LongStoryGoes — 020
===================

A SMALL EXPERIMENT WITH RANDOMNESS

This story uses Python's standard `random` library.

The library is not hidden behind a LongStoryGoes framework.

It is simply part of the story.

The question:

    Can a normal Python library become part of the fictional world
    while the file remains readable as a story?

Run:

    python 020.py

The console is the reader.

The same file can also be inspected by another program.

This is a sandbox experiment, not a new architecture.
"""


from random import choice


# ---------------------------------------------------------------------------
# The story
# ---------------------------------------------------------------------------


print("The Last Apple")
print()
print("It was late afternoon in the village.")
print()
print("Anna came to the old orchard.")
print("Only one apple remained on the tree.")
print()


# ---------------------------------------------------------------------------
# A little Python enters the story.
#
# The tree has three possible branches.
#
# The story does not know beforehand which branch will give Anna the apple.
# ---------------------------------------------------------------------------


branches = ["left branch", "middle branch", "right branch"]

apple_branch = choice(branches)


print("Anna looked at the tree.")
print("She wondered which branch held the apple.")
print()


# ---------------------------------------------------------------------------
# Anna makes a choice.
# ---------------------------------------------------------------------------


anna_choice = "middle branch"

print(f"Anna reached toward the {anna_choice}.")
print()


# ---------------------------------------------------------------------------
# Python decides what is true.
# ---------------------------------------------------------------------------


if anna_choice == apple_branch:
    apple_found = True

    print("Her hand found the apple.")
    print("She smiled.")
    print("The last apple was hers.")

else:
    apple_found = False

    print("There was nothing there.")
    print("Anna looked up at the other branches.")
    print("The last apple was still somewhere in the tree.")


print()


# ---------------------------------------------------------------------------
# The result becomes part of the story.
# ---------------------------------------------------------------------------


if apple_found:
    apple_state = "in Anna's hand"
else:
    apple_state = "still in the tree"


print(f"The apple was {apple_state}.")
print()


# ---------------------------------------------------------------------------
# A little history.
#
# We are not building a framework here.
# We are simply keeping the fact that happened.
# ---------------------------------------------------------------------------


event = {
    "type": "apple_search",
    "actor": "Anna",
    "choice": anna_choice,
    "result": "found" if apple_found else "not_found",
}


# ---------------------------------------------------------------------------
# Anna remembers what happened.
# ---------------------------------------------------------------------------


memory = (
    "Anna remembered finding the last apple."
    if apple_found
    else "Anna remembered reaching for the wrong branch."
)


print(memory)
print()


# ---------------------------------------------------------------------------
# End of story
# ---------------------------------------------------------------------------


print("The sun was getting lower.")
print("Anna left the orchard.")
print()


# ---------------------------------------------------------------------------
# Tiny inspection section.
#
# This is useful when another Python program imports or examines the file.
# ---------------------------------------------------------------------------


WORLD = {
    "apple": {
        "state": apple_state,
    },
    "anna": {
        "choice": anna_choice,
        "memory": memory,
    },
    "event": event,
}


if __name__ == "__main__":
    print("---")
    print("Story state:")
    print(WORLD)
