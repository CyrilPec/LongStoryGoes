"""
031+02.py
=========

GRAPH -> CONTACT -> FORCE VECTOR -> TOOL MECHANICS
=================================================

This experiment extends 031+01.

The central idea:

    GEOMETRY
       |
       v
    contact region
       |
       v
    chip / cutting area
       |
       v
    cutting force vector
       |
       +----------------+
       |                |
       v                v
    PyBullet         tool mechanics
    reaction         M = r x F
                       |
                       v
                    stress
                       |
                       v
                 allowable load


IMPORTANT
---------

We deliberately separate three layers.

1. GEOMETRY
   What material is being removed?

2. MACHINING MODEL
   What force is produced by that removal?

3. MECHANICS
   What does that force do to the cutter and machine?

This is much more useful than asking PyBullet to "understand"
metal cutting.

PyBullet is a rigid-body mechanics engine.

Our model tells PyBullet:

    where the force acts
    what direction it acts
    how large it is

Later, PyBullet can return:

    reaction forces
    motion
    displacement
    contact information

---------------------------------------------------------------
1. GRAPH REPRESENTATION
---------------------------------------------------------------

For the first experiments, represent a lathe workpiece by:

    G(z) = radius at position z

Example:

    z ---------------------------->

    radius
       |
    10 |===========================   stock Ø20
       |
       |
       +----------------------------

After cutting:

    radius
       |
    10 |=========\
       |          \
     8 |           =================
       |
       +---------------------------->

The graph is the geometry.

---------------------------------------------------------------
2. MATERIAL REMOVAL
---------------------------------------------------------------

The cutter occupies a region C(t).

The workpiece occupies W(t).

At time t:

    R(t) = W(t) ∩ C(t)

where R(t) is the instantaneous contact/removal region.

Then:

    W(t + dt) = W(t) - R(t)

This is our geometric material-removal operation.

Initially we use simple analytical geometry.

Later we can replace it with:

    polygon intersection
    polygon difference
    mesh Boolean
    signed-distance field
    voxel field

without changing the higher-level theory.

---------------------------------------------------------------
3. CHIP AREA
---------------------------------------------------------------

The simplest turning approximation is:

    Ac = ap * f

where:

    Ac = chip cross-sectional area [mm²]
    ap = depth of cut [mm]
    f  = feed per revolution [mm/rev]

But this is only an approximation.

Eventually:

    Ac = area(contact geometry)

should come directly from the graph intersection.

This is an important transition:

    APPROXIMATION
        |
        v
    ap * f
        |
        v
    ACTUAL GEOMETRY
        |
        v
    intersection area

---------------------------------------------------------------
4. MATERIAL MODEL
---------------------------------------------------------------

The geometry alone does not determine force.

We need a material/cutting model.

First approximation:

    Fc = Kc * Ac

where:

    Fc = cutting force [N]
    Kc = specific cutting force [N/mm²]
    Ac = chip area [mm²]

Kc is NOT simply hardness.

It depends on:

    material
    heat treatment
    chip thickness
    rake angle
    tool geometry
    cutting speed
    friction
    etc.

Therefore the model should eventually contain:

    Material
        |
        +-- hardness
        +-- strength
        +-- elastic properties
        +-- thermal properties
        +-- cutting coefficients

---------------------------------------------------------------
5. FORCE MUST BE A VECTOR
---------------------------------------------------------------

Instead of:

    F = 3000 N

we want:

    F = (Ft, Fr, Fa)

where:

    Ft = tangential cutting force
    Fr = radial force
    Fa = axial/feed force

Resultant:

    |F| = sqrt(Ft² + Fr² + Fa²)

The force has a point of application.

Therefore our fundamental object becomes:

    ForceVector(
        position,
        direction,
        magnitude
    )

This maps naturally to PyBullet.

---------------------------------------------------------------
6. LOCAL COORDINATE SYSTEM
---------------------------------------------------------------

For a turning operation:

    axial direction       = a
    radial direction      = r
    tangential direction  = t

At the contact point:

                  radial
                    ^
                    |
                    |
                    o -----> tangential
                   /
                  /
               axial

The actual coordinate system will eventually rotate with
the spindle.

This allows the same cutting model to work while the stock
rotates.

---------------------------------------------------------------
7. FORCE FROM CONTACT
---------------------------------------------------------------

Conceptually:

    contact geometry
          |
          v
        Ac(t)
          |
          v
       material
          |
          v
       F(t)

Therefore:

    F(t) = Model(
        Ac(t),
        material,
        tool,
        speed,
        feed
    )

The force can change every simulation timestep.

This is important.

We do NOT want one constant force for the entire operation.

---------------------------------------------------------------
8. FORCE APPLICATION POINT
---------------------------------------------------------------

Let:

    r

be the vector from the tool support/reference point to
the cutting point.

Then:

    M = r × F

where M is the moment applied to the tool.

This creates bending and torsion.

For a simplified beam model:

    sigma = M*c/I

where:

    sigma = bending stress
    M     = bending moment
    c     = distance from neutral axis
    I     = second moment of area

For a rectangular tool:

    I = b*h³/12

This allows us to ask:

    Is the cutter overloaded?

rather than merely:

    What is the cutting force?

---------------------------------------------------------------
9. PYBULLET'S ROLE
---------------------------------------------------------------

PyBullet represents the mechanical system.

Our model supplies:

    position = cutting point
    force    = cutting force vector

PyBullet then handles:

    rigid-body dynamics
    reactions
    constraints
    motion
    contact
    visualization

Conceptually:

              OUR MODEL
                  |
                  v
        +-------------------+
        | force + position  |
        +-------------------+
                  |
                  v
             PYBULLET
                  |
        +---------+---------+
        |                   |
        v                   v
    tool motion        reactions

---------------------------------------------------------------
10. TORQUE AND POWER
---------------------------------------------------------------

Tangential cutting force produces spindle torque:

    T = Ft * r

where r is the workpiece radius.

Cutting power:

    P = Ft * Vc

where Vc is cutting speed in m/s.

For a spindle:

    P_available >= P_required

and:

    T_available >= T_required

These become machine constraints.

---------------------------------------------------------------
11. RPM
---------------------------------------------------------------

For turning:

    Vc = pi * D * N / 1000

therefore:

    N = 1000 * Vc / (pi * D)

The important observation is:

    D changes
        |
        v
    RPM changes

if constant cutting speed is desired.

Thus RPM can be part of the dynamic machine state.

---------------------------------------------------------------
12. FEED
---------------------------------------------------------------

Feed per revolution:

    f [mm/rev]

Feed velocity:

    Vf = f * N

Therefore:

    material removal rate

    Q = Ac * Vf

So:

    geometry
       |
       v
      Ac
       |
       +---- feed ----+
       |              |
       v              v
    force            MRR
       |
       v
    tool load

---------------------------------------------------------------
13. MACHINE CONSTRAINTS
---------------------------------------------------------------

A physically feasible operation must satisfy several limits:

    F < F_tool

    M < M_tool

    sigma < sigma_allow

    T < T_spindle

    P < P_spindle

    RPM < RPM_max

    feed < feed_max

This creates a feasible region rather than a single answer.

---------------------------------------------------------------
14. ENERGY
---------------------------------------------------------------

Power changes with time.

Therefore machining energy is:

    E = integral(P(t) dt)

Two tool paths can create the same final geometry but consume
different energy.

Therefore an optimization system can prefer:

    less time
    less energy
    less force
    less tool stress
    acceptable surface quality
    acceptable final geometry

---------------------------------------------------------------
15. RL LATER
---------------------------------------------------------------

Once the deterministic simulator works:

    STATE
      |
      +-- geometry
      +-- diameter
      +-- contact area
      +-- force
      +-- torque
      +-- power
      +-- tool stress
      +-- spindle state
      +-- feed
      +-- RPM

        |
        v

      AGENT

        |
        v

    ACTION
      |
      +-- feed
      +-- depth
      +-- RPM
      +-- tool position

        |
        v

    SIMULATOR

        |
        v

    NEW STATE + REWARD

---------------------------------------------------------------
16. FIELD THEORY — FUTURE
---------------------------------------------------------------

This is intentionally NOT implemented yet.

The discrete graph model can eventually be transformed into
a continuous field.

Instead of:

    Ac
    F
    M

we can define spatial fields:

    A(x,y,z,t)
    F(x,y,z,t)
    stress(x,y,z,t)
    temperature(x,y,z,t)
    material(x,y,z,t)

Then spatial derivatives become meaningful:

    gradient
    divergence
    curl

For example, a force field:

    F(x,y,z,t)

can have:

    div(F)

and gradients can describe how quantities change through
space.

But this comes AFTER the graph model.

The progression is therefore:

    GRAPH
      ↓
    AREA
      ↓
    FORCE
      ↓
    VECTOR
      ↓
    MECHANICS
      ↓
    FIELD
      ↓
    PDE / CONTINUOUS PHYSICS

We should not jump to the field description before the
discrete model is working.

---------------------------------------------------------------
17. CORE PRINCIPLE
---------------------------------------------------------------

The whole experiment is an example of transformation.

Instead of directly solving:

    "simulate metal cutting"

transform the problem:

    metal cutting
        ↓
    geometry
        ↓
    intersection
        ↓
    area
        ↓
    material model
        ↓
    force vector
        ↓
    mechanics

Each transformation reduces the complexity of the problem
while preserving the information needed by the next layer.

That is the foundation of this simulator.
"""
