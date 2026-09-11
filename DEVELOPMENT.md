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
