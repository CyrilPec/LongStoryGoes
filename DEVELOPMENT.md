LongStoryGoes is developed incrementally.

An AI assistant working on this repository must:

1. Read ARCHITECTURE.md before changing concepts.

2. Preserve existing concepts unless explicitly instructed otherwise.

3. Prefer adding a new concept over replacing an existing one.

4. Preserve existing files and examples.

5. Do not remove working behavior merely to simplify the architecture.

6. Do not introduce a framework or dependency without a demonstrated need.

7. Keep concepts independent from presentation systems.

8. Keep stories separate from reusable concepts.

9. When adding a concept, create a small example demonstrating it.

10. When modifying an existing concept, verify that previous examples
    still work.

11. Treat old files as compatibility requirements.

12. Prefer backward-compatible additions.

13. Document architectural decisions that affect future development.

14. Never assume that a future developer knows the reasoning behind
    an existing concept.

15. Before changing architecture, explain what existing behavior would
    be affected.

    When a story requires behavior that does not belong to a general concept, the story may extend or specialize an existing concept rather than modifying the base concept. If the specialization proves generally useful across multiple stories, it may later be promoted into a reusable concept.

Improve existing concepts when the improvement is genuinely general.

Add a new concept when the behavior represents a reusable concept.

Let stories subclass/extend concepts when behavior is specific to that story.

Promote story-specific extensions into reusable concepts only when experience shows that they belong in the general model.

Reusable concept
        vs
Story-local implementation
        vs
External adapter

Use 017.py to improve Observer, Memory, and Knowledge so the concepts—not the story—own more of the behavior, while keeping every existing story working.

 Story Files

A story file should remain a story.

Keep story files short, readable, and executable. Prefer natural world actions such as:

teacher.enter(classroom)
anna.push(leo)
leo.fall(chair)
teacher.look_at(chair)


Do not repeat executable actions in English:

"""
Anna pushes Leo.
"""
anna.push(leo)


The Python action is already the sentence.

English remains useful for meaning that is not an executable action: description, context, thought, uncertainty, atmosphere, memory, and narrative.

The complexity required to execute an action belongs in the LongStoryGoes concepts and engine, not inside the story file.

A story author should not need to write Action, Event, validation, renderer, Blender, API, or other infrastructure code merely to tell a story.

The goal is:

short story
    ↓
readable Python
    ↓
LongStoryGoes world
    ↓
optional presentation


Story files should become simpler as the engine becomes more capable, not more complicated.

When a new story requires a new capability, improve the underlying concept or engine and keep the story itself simple.
