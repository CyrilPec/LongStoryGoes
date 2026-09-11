# LongStoryGoes Architecture

## Purpose

LongStoryGoes defines a world once, then allows stories to create and use that world through reusable concepts.

The same story/world should eventually be representable as text, TUI, audio, or 3D without changing the underlying concepts.

## Layers

```text
Concepts
   ↓
Story
   ↓
World
   ↓
Events / State / Time
   ↓
Renderer / Importer
   ↓
Text / TUI / Audio / Blender

Concept Layer

The 000-XX.py files define reusable concepts.

000.py       Project philosophy / foundation
000-01.py    World
000-02.py    Human
000-03.py    Animal
000-04.py    PhysicalObject
000-05.py    Narrator
000-06.py    Observer
000-07.py    Time
000-08.py    Place
000-09.py    Event
000-10.py    Relationship
000-11.py    Action
000-12.py    State
000-13.py    Memory


Concept files define what something is and what it can do.

They should not contain a particular story.

They should not depend on Blender.

World

World is the common state of the fictional universe.

It contains or provides access to:

time
entities
places
objects
events


The World is the bridge between the conceptual story model and presentation systems.

The World must remain independent of Blender, TUI, audio, and other renderers.

Entities

Examples of entities include:

Human
Animal
PhysicalObject


Concrete instances are created by stories.

For example:

bird = Animal("Little Bird")
ball = PhysicalObject("Red Ball")


The concept is defined once; stories create instances of it.

Observer

An Observer perceives the world from a particular perspective.

observer.observe(thing)


Observation is not narration.

An observer may have limited knowledge and memory.

Humans and animals may eventually inherit or compose Observer behavior.

Narrator

A Narrator communicates the story to an audience.

narrator.observe(...)


Narration is not the same as perception.

The long-term goal is for narration to operate on world events and concepts rather than requiring English text as the underlying representation.

The same story should eventually support:

English
other languages
text
TUI
audio
visual presentation

Time

Time provides a shared progression for the World.

Events can have a temporal position.

Time should initially remain abstract.

Calendars, clocks, dates, and other representations can be added later.

Place

A Place represents where entities, objects, and events can exist.

Examples:

garden
house
forest
city

Event

An Event represents something that happens in the World.

An Event can contain:

type
time
place
actor
target
data


The distinction is important:

Action → something an entity does
Event  → something that happened in the World

Action

An Action describes something an entity can do.

Examples:

walk
fly
eat
observe
play
sleep


An Action can result in an Event and changes to World state.

State

A State describes the condition of an entity or object.

Examples:

awake
sleeping
happy
flying
broken
open
closed


State can change as Events occur.

Relationship

A Relationship describes a connection between two things.

Examples:

owns
knows
follows
near
contains
loves


Relationships belong to the World model, not to a renderer.

Memory

Memory allows an Observer or other entity to retain information from the past.

Memory can contain observations, experiences, or Events.

Stories

Story files such as:

014.py
015.py
016.py


create concrete instances of the concepts and describe what happens.

Stories should be small examples and tests of the conceptual system.

They should use the concepts rather than redefine them.

Presentation

Presentation is separate from the World.

Current direction:

World
  ↓
v1_importer.py
  ↓
Blender 3.6


v1_importer.py translates World concepts into Blender representations.

For example:

Animal          → Blender character/object
PhysicalObject  → Blender object
Place           → Blender environment
Event           → animation/event
Time            → animation timeline
State           → visual state


The concepts themselves must not contain Blender code.

Future presentation systems may include:

Text
TUI
Audio
Blender

Development Rules
Define a reusable concept once in a 000-XX.py file.
Keep concepts independent from presentation systems.
Create concrete instances in story files.
Use World as the common world-state bridge.
Keep Observer and Narrator conceptually separate.
Keep Action and Event conceptually separate.
Keep Time independent from real-world calendar representations.
Do not rewrite all old stories when a concept changes.
Update individual files when the architecture requires it.
Prefer small working examples over premature complexity.
Add a new concept when a story demonstrates a real need for it.
Keep Blender integration in v1_importer.py, not in the concepts.
Current Development Direction

The current conceptual progression is:

World
Human
Animal
PhysicalObject
Narrator
Observer
Time
Place
Event
Relationship
Action
State
Memory


The next step is to continue creating small stories that exercise these concepts.

When a story exposes a weakness in a concept, improve that concept individually and continue.

Core Principle

The story is not the presentation.

The World is not Blender.

The concepts describe what exists and what happens.

The story creates concrete instances and events.

The narrator communicates those events.

Renderers decide how the audience experiences them.

        CONCEPTS
           ↓
         WORLD
           ↓
         STORY
           ↓
        EVENTS
           ↓
      PRESENTATION
      ↙     ↓      ↘
   TEXT    TUI    BLENDER
                   ↓
                AUDIO/3D

:::

This is the document I'd commit now. It gives another AI enough context to **continue the project rather than redesign it**.

Story-local concepts

A story may define its own specialized classes when a behavior is
needed only for that story or is still experimental.

A story-local class does not automatically become a global concept.

If the same abstraction proves useful across multiple stories, it may
later be promoted into a reusable 000-XX.py concept.

Promotion is evolutionary, not mandatory.

Example:

    012.py
        Character
        Location
        PhysicsAdapter

These are currently story-level implementations/experiments.

They may later become reusable concepts if future stories demonstrate
that they belong in the general model.

