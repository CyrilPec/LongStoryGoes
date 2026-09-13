"""
031+03.py
=========

FROM GRAPHS TO FIELDS
=====================

This file describes the next transformation of the machining model.

Previous stage:

    GRAPH
      ↓
    AREA
      ↓
    FORCE VECTOR
      ↓
    TOOL / MACHINE MECHANICS

This stage asks:

    Can machining quantities be represented as spatial fields?

The answer is yes.

The important mathematical idea is:

    A GRAPH is a discrete representation.

    A FIELD is a value defined throughout space and time.

We therefore have a natural progression:

    graph
      ↓
    sampled graph
      ↓
    discrete field
      ↓
    continuous field
      ↓
    differential equations


===============================================================
1. WHY FIELDS?
===============================================================

A single number such as:

    temperature = 400 °C

does not tell us where the heat is.

A field:

    T(x, y, z, t)

does.

Likewise:

    force = 3000 N

does not describe how mechanical loading is distributed.

A stress field:

    sigma(x, y, z, t)

does.

A velocity field:

    v(x, y, z, t)

describes how material or chips move.

This allows machining to become a spatial and temporal problem.


===============================================================
2. TEMPERATURE FIELD
===============================================================

Temperature becomes a scalar field:

    T(x, y, z, t)

The gradient is:

    grad(T) = ∇T

The gradient tells us the direction and rate of greatest
temperature increase.

The magnitude:

    |∇T|

tells us how rapidly temperature changes in space.

Heat flux follows Fourier's law:

    q = -k ∇T

where:

    q = heat flux vector
    k = thermal conductivity

Therefore:

    TEMPERATURE FIELD
           ↓
        GRADIENT
           ↓
        HEAT FLUX
           ↓
      HEAT EVACUATION

This can eventually describe heat flowing:

    tool
      ↔
    chip
      ↔
    workpiece
      ↔
    environment


===============================================================
3. PRESSURE FIELD
===============================================================

Pressure is a scalar field:

    p(x, y, z, t)

Its gradient is:

    ∇p

In a fluid or continuum formulation, pressure contributes
a force density:

    f_pressure = -∇p

Therefore:

    PRESSURE FIELD
          ↓
       GRADIENT
          ↓
    FORCE DENSITY

IMPORTANT:

A gradient is NOT itself pressure.

A gradient describes spatial change.

A physical law tells us what that gradient produces.


===============================================================
4. SOLID CUTTING: STRESS FIELD
===============================================================

For a cutting tool and workpiece, pressure alone is not enough.

A more general description is the stress tensor:

              σxx  σxy  σxz
    σ =       σyx  σyy  σyz
              σzx  σzy  σzz

The stress field is:

    σ(x, y, z, t)

The divergence of the stress tensor gives internal force
density:

    f = ∇ · σ

Therefore:

    STRESS FIELD
         ↓
      DIVERGENCE
         ↓
    FORCE DENSITY
         ↓
    RESULTANT FORCE

This provides a much deeper connection between our earlier
force-vector model and continuum mechanics.


===============================================================
5. FORCE VECTOR VS FORCE FIELD
===============================================================

Earlier we had:

    F = (Ft, Fr, Fa)

This is a resultant force acting at a contact point.

A field description is more detailed:

    f(x, y, z, t)

Now the resultant force can be obtained by integrating force
density over a volume:

    F = ∫ f dV

Similarly, surface traction can be integrated over a contact
surface.

Thus:

    CONTACT AREA
          ↓
    LOCAL STRESS
          ↓
    FORCE DENSITY / TRACTION
          ↓
    INTEGRATION
          ↓
    RESULTANT FORCE


===============================================================
6. TOOL CONTACT
===============================================================

The cutter/workpiece interface is especially important.

At the contact surface we may eventually have:

    normal stress
    tangential stress
    friction
    temperature
    velocity
    pressure

A simplified conceptual contact field is:

    C(x, y, z, t)

where C describes whether a point is:

    0 = no contact
    1 = contact

or, more realistically, a continuous contact quantity.

Then:

    geometry
       ↓
    contact field
       ↓
    stress / friction field
       ↓
    force


===============================================================
7. CHIP VELOCITY FIELD
===============================================================

The chip is not just removed volume.

It moves.

Represent its velocity as:

    v(x, y, z, t)

This is a vector field.

We can ask:

    Where is the chip moving?

    How fast?

    Is it moving away from the cutting zone?

    Is material accumulating?

This gives a possible future chip-evacuation model.


===============================================================
8. DIVERGENCE AND CHIP EVACUATION
===============================================================

For a velocity field:

    v(x, y, z, t)

the divergence is:

    ∇ · v

Conceptually:

    ∇ · v > 0

means local expansion / outflow.

    ∇ · v < 0

means local convergence / inflow.

    ∇ · v ≈ 0

means approximately incompressible local flow.

For chip transport, divergence alone is not sufficient to
describe evacuation, but it is one useful diagnostic.

Eventually we can combine:

    velocity
    density
    temperature
    pressure
    contact

to model chip transport.


===============================================================
9. INERTIA
===============================================================

Inertia is different from a gradient.

For a material element:

    f_inertia = ρ a

where:

    ρ = density
    a = acceleration

Acceleration is:

    a = dv/dt

For rotating machinery, acceleration can include rotational
effects such as centripetal acceleration.

Therefore:

    VELOCITY FIELD
          ↓
      ACCELERATION
          ↓
        INERTIA


===============================================================
10. ROTATING WORKPIECE
===============================================================

For turning:

    Vc = π D N / 1000

The workpiece has angular velocity:

    ω

and a point at radius r has centripetal acceleration:

    a = ω² r

Therefore the rotating workpiece naturally introduces an
acceleration field.

At high speeds this becomes part of the mechanical model.


===============================================================
11. HEAT GENERATION
===============================================================

Cutting converts mechanical work into heat.

Approximate cutting power:

    P = Ft Vc

The generated heat can be distributed among:

    chip
    tool
    workpiece
    environment

A future model could define:

    Q_tool
    Q_chip
    Q_workpiece

with:

    Q_total ≈ P

subject to the chosen time interval and efficiency model.

Thus:

    CUTTING FORCE
          ↓
       POWER
          ↓
     HEAT GENERATION
          ↓
    TEMPERATURE FIELD
          ↓
      HEAT FLUX


===============================================================
12. GRADIENT AS A GENERAL OPERATOR
===============================================================

The gradient transforms a scalar field into a vector field.

For scalar field:

    φ(x,y,z)

the gradient is:

    ∇φ

For example:

    φ = T

gives:

    ∇T

For:

    φ = p

we get:

    ∇p

So we can think:

    scalar field
         ↓
      gradient
         ↓
     vector field


===============================================================
13. DIVERGENCE AS A GENERAL OPERATOR
===============================================================

Divergence transforms a vector field into a scalar field.

For:

    F = (Fx, Fy, Fz)

the divergence is:

    ∇ · F

Conceptually it measures local net outflow.

For stress, the operation is applied to the tensor:

    ∇ · σ

which produces a vector representing force density.


===============================================================
14. CURL
===============================================================

Another useful field operation is curl:

    ∇ × F

It measures local rotational tendency of a vector field.

This may become useful later for:

    fluid/chip motion
    rotating flows
    vortices
    electromagnetic analogies

But curl is NOT required for the first machining model.


===============================================================
15. THE UNIFIED FIELD PICTURE
===============================================================

Eventually our machining world could contain:

    Geometry field
    Material field
    Temperature field
    Pressure field
    Stress field
    Velocity field
    Force field
    Contact field

For example:

    Geometry
       ↓
    Contact
       ↓
    Stress
       ↓
    Force
       ↓
    Motion
       ↓
    Velocity
       ↓
    Chip transport

At the same time:

    Cutting
       ↓
    Mechanical work
       ↓
    Heat
       ↓
    Temperature
       ↓
    Heat gradient
       ↓
    Heat flux


===============================================================
16. DISCRETE → CONTINUOUS
===============================================================

We do NOT need to immediately solve continuous PDEs.

Start with a grid.

For example:

    x0  x1  x2  x3  x4
     +---+---+---+---+
     |   |   |   |   |
     +---+---+---+---+
     |   |   |   |   |
     +---+---+---+---+

Each cell can store:

    material
    temperature
    pressure
    stress
    velocity
    contact

Then numerical derivatives approximate:

    gradient
    divergence
    curl


===============================================================
17. FINITE DIFFERENCE EXAMPLE
===============================================================

For a one-dimensional temperature field:

    T(x)

the gradient can be approximated by:

    dT/dx ≈ (T[i+1] - T[i-1]) / (2 dx)

This means we can calculate the temperature gradient directly
from sampled graph/field data.

The same idea extends to 2D and 3D.


===============================================================
18. WHY THIS CONNECTS TO OUR GRAPH
===============================================================

Our original graph:

    radius = G(z)

can be sampled:

    G(z0)
    G(z1)
    G(z2)
    ...

That is already a discrete field.

Instead of thinking:

    "a graph"

we can eventually think:

    "a one-dimensional field."

Then the 2D machining geometry becomes a field.

Then the 3D workpiece becomes a 3D field.


===============================================================
19. MULTI-FIELD MACHINING STATE
===============================================================

A future simulation state could be:

    S(x,y,z,t) =

    {
        geometry,
        material,
        temperature,
        pressure,
        stress,
        velocity,
        contact
    }

The simulation evolves:

    S(t) → S(t + dt)


===============================================================
20. FUTURE RL INTERFACE
===============================================================

The RL agent does not need to understand the equations.

It can observe selected field quantities:

    state =
    {
        cutting_area,
        force,
        temperature,
        stress,
        velocity,
        tool_position,
        spindle_speed,
        feed
    }

and choose:

    action =
    {
        feed,
        RPM,
        depth,
        tool_position
    }

The simulator returns:

    new_state
    reward
    done


===============================================================
21. THE FULL TRANSFORMATION
===============================================================

This is the conceptual progression:

    REAL MACHINING
          ↓
       GEOMETRY
          ↓
        GRAPH
          ↓
         AREA
          ↓
       CONTACT
          ↓
    FORCE VECTOR
          ↓
       MECHANICS
          ↓
       DISCRETE FIELDS
          ↓
       GRADIENTS
          ↓
      DIVERGENCE
          ↓
     CONTINUUM FIELDS
          ↓
        PDEs
          ↓
      FULL PHYSICS


===============================================================
22. IMPORTANT PRINCIPLE
===============================================================

We should not start with the most complicated mathematics.

Start with something we can verify:

    graph
    area
    force
    torque
    power

Then add:

    vectors
    moments
    stress

Then:

    temperature
    velocity
    pressure

Then:

    gradients
    divergence
    field equations

Finally:

    coupled PDEs
    FEM / FVM / other numerical methods

Each layer should be testable against the previous layer.

The goal is not to make the model complicated.

The goal is to find the simplest representation that preserves
the physical information we need.


===============================================================
23. CORE IDEA
===============================================================

A difficult physical process can sometimes be transformed into
a sequence of simpler mathematical representations:

    OBJECT
      ↓
    GRAPH
      ↓
    AREA
      ↓
    VECTOR
      ↓
    FIELD
      ↓
    DERIVATIVE
      ↓
    PHYSICAL LAW

The important part is the transformation.

The field description is therefore not a replacement for the
graph model.

It is the next resolution of the same model.
"""


# ============================================================
# SMALL NUMERICAL DEMONSTRATION
# ============================================================

import numpy as np


def demonstrate_temperature_gradient():
    """
    Demonstrate the transition from sampled values to a field
    derivative.

    We create a one-dimensional temperature field:

        T(x)

    and calculate its numerical gradient.

    This is NOT a cutting-temperature model yet.
    It simply demonstrates the mathematical operation.
    """

    x = np.linspace(
        0.0,
        10.0,
        101
    )

    # Example temperature field.
    #
    # Hotter near the cutting zone.
    T = 20.0 + 500.0 * np.exp(
        -((x - 5.0) ** 2) / 2.0
    )

    # Numerical gradient.
    dTdx = np.gradient(
        T,
        x
    )

    print()
    print("=" * 60)
    print("FIELD DEMONSTRATION")
    print("=" * 60)

    print(
        f"Temperature range: "
        f"{T.min():.2f} ... {T.max():.2f} °C"
    )

    print(
        f"Maximum |gradient|: "
        f"{np.max(np.abs(dTdx)):.2f} °C/mm"
    )

    # Fourier-law demonstration.
    #
    # q = -k grad(T)
    #
    # Use an illustrative thermal conductivity.
    k = 40.0

    heat_flux = -k * dTdx

    print(
        f"Maximum |heat flux|: "
        f"{np.max(np.abs(heat_flux)):.2f}"
    )

    return x, T, dTdx, heat_flux


def demonstrate_velocity_divergence():
    """
    Demonstrate the idea of divergence using a 1D velocity field.

    In one dimension:

        div(v) = dv/dx

    Again, this is only a mathematical demonstration.
    """

    x = np.linspace(
        0.0,
        10.0,
        101
    )

    # Example velocity field.
    v = 2.0 * x

    divergence = np.gradient(
        v,
        x
    )

    print()
    print("=" * 60)
    print("VELOCITY / DIVERGENCE DEMONSTRATION")
    print("=" * 60)

    print(
        f"Velocity at start: "
        f"{v[0]:.2f}"
    )

    print(
        f"Velocity at end: "
        f"{v[-1]:.2f}"
    )

    print(
        f"Approx. divergence: "
        f"{np.mean(divergence):.2f}"
    )

    return x, v, divergence


if __name__ == "__main__":

    demonstrate_temperature_gradient()

    demonstrate_velocity_divergence()

    print()
    print("=" * 60)
    print("031+03 COMPLETE")
    print("=" * 60)

    print(
        """
Next conceptual step:

    graph
      ↓
    discrete field
      ↓
    2D / 3D field
      ↓
    gradient + divergence
      ↓
    coupled machining fields
    """
    )
