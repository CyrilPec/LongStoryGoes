"""
031+04.py
======

SIMPLEST VERIFIED TURNING MODEL
===============================

Purpose
-------

Verify the basic machining chain:

    geometry
       ↓
    depth of cut
       ↓
    chip area
       ↓
    cutting force
       ↓
    torque
       ↓
    spindle power
       ↓
    tool moment
       ↓
    bending stress

This is intentionally NOT a complete metal-cutting simulator.

It is the smallest model whose individual quantities can be
checked against known equations.

---------------------------------------------------------------

ASSUMPTIONS
-----------

Turning a cylindrical AISI 1040 steel workpiece.

Stock:

    diameter = 20 mm

Tool:

    HSS
    rectangular section = 10 x 10 mm

Machining:

    depth of cut = 2 mm
    feed = 0.10 mm/rev
    cutting speed = 20 m/min

Material:

    illustrative specific cutting force Kc

IMPORTANT:

Kc is an engineering input here, not something calculated
from hardness alone.

For real machining design, use experimentally validated
cutting coefficients for the exact material, tool geometry,
rake angle, chip thickness, etc.

---------------------------------------------------------------

EQUATIONS
---------

RPM:

    N = 1000 Vc / (pi D)

Chip area:

    Ac = ap * f

Cutting force:

    Fc = Kc * Ac

Spindle torque:

    T = Ft * r

Cutting power:

    P = Ft * Vc

Tool bending moment:

    M = F * L

Rectangular section second moment:

    I = b h^3 / 12

Bending stress:

    sigma = M c / I

---------------------------------------------------------------

VERIFICATION
------------

The program prints intermediate quantities so every step
can be independently checked.

It also performs assertions on the basic identities.

---------------------------------------------------------------

NEXT STEP
---------

Once this is verified, 032+01 can add:

    2D workpiece graph
    cutter position
    changing diameter
    changing force with position

Then:

    032+02 -> PyBullet mechanics

Then:

    field model
    temperature
    chip transport
    etc.

"""


import math
from dataclasses import dataclass


# ============================================================
# MATERIAL
# ============================================================

@dataclass
class Material:
    name: str
    specific_cutting_force_N_mm2: float


AISI_1040 = Material(
    name="AISI 1040",
    # Deliberately illustrative.
    #
    # Replace with experimentally validated Kc later.
    specific_cutting_force_N_mm2=1500.0,
)


# ============================================================
# TOOL
# ============================================================

@dataclass
class Tool:
    material: str

    # mm
    width_mm: float
    height_mm: float

    # Distance from support to cutting point.
    #
    # This is an intentionally simple cantilever model.
    overhang_mm: float


HSS_TOOL = Tool(
    material="HSS",
    width_mm=10.0,
    height_mm=10.0,
    overhang_mm=30.0,
)


# ============================================================
# WORKPIECE
# ============================================================

@dataclass
class Workpiece:
    material: Material
    diameter_mm: float


STOCK = Workpiece(
    material=AISI_1040,
    diameter_mm=20.0,
)


# ============================================================
# MACHINING PARAMETERS
# ============================================================

@dataclass
class Machining:
    depth_of_cut_mm: float
    feed_mm_rev: float
    cutting_speed_m_min: float


CUT = Machining(
    depth_of_cut_mm=2.0,
    feed_mm_rev=0.10,
    cutting_speed_m_min=20.0,
)


# ============================================================
# BASIC MACHINING EQUATIONS
# ============================================================

def calculate_rpm(
    cutting_speed_m_min: float,
    diameter_mm: float,
) -> float:

    """
    N = 1000 Vc / (pi D)
    """

    return (
        1000.0
        * cutting_speed_m_min
        / (
            math.pi
            * diameter_mm
        )
    )


def calculate_chip_area(
    depth_of_cut_mm: float,
    feed_mm_rev: float,
) -> float:

    """
    Simplified turning chip cross-sectional area:

        Ac = ap * f

    units:

        mm * mm/rev

    Numerically represented as mm² per revolution.
    """

    return (
        depth_of_cut_mm
        * feed_mm_rev
    )


def calculate_cutting_force(
    chip_area_mm2: float,
    kc_N_mm2: float,
) -> float:

    """
    Fc = Kc * Ac
    """

    return (
        kc_N_mm2
        * chip_area_mm2
    )


def calculate_torque(
    tangential_force_N: float,
    diameter_mm: float,
) -> float:

    """
    T = F * r

    Convert radius from mm to metres.
    """

    radius_m = (
        diameter_mm
        / 2.0
        / 1000.0
    )

    return (
        tangential_force_N
        * radius_m
    )


def calculate_power(
    tangential_force_N: float,
    cutting_speed_m_min: float,
) -> float:

    """
    P = F * V

    Convert m/min -> m/s.
    """

    velocity_m_s = (
        cutting_speed_m_min
        / 60.0
    )

    return (
        tangential_force_N
        * velocity_m_s
    )


# ============================================================
# TOOL MECHANICS
# ============================================================

def calculate_tool_moment(
    force_N: float,
    overhang_mm: float,
) -> float:

    """
    Cantilever approximation:

        M = F L

    result: N*m
    """

    overhang_m = (
        overhang_mm
        / 1000.0
    )

    return (
        force_N
        * overhang_m
    )


def rectangular_second_moment(
    width_mm: float,
    height_mm: float,
) -> float:

    """
    I = b h^3 / 12

    mm^4
    """

    return (
        width_mm
        * height_mm ** 3
        / 12.0
    )


def calculate_bending_stress(
    moment_Nm: float,
    width_mm: float,
    height_mm: float,
) -> float:

    """
    sigma = M c / I

    Convert M from N*m -> N*mm.

    Result: N/mm² = MPa.
    """

    moment_Nmm = (
        moment_Nm
        * 1000.0
    )

    I = rectangular_second_moment(
        width_mm,
        height_mm,
    )

    c = height_mm / 2.0

    return (
        moment_Nmm
        * c
        / I
    )


# ============================================================
# COMPLETE CALCULATION
# ============================================================

def calculate_cut(
    workpiece: Workpiece,
    tool: Tool,
    machining: Machining,
):

    D = workpiece.diameter_mm

    ap = machining.depth_of_cut_mm
    f = machining.feed_mm_rev
    Vc = machining.cutting_speed_m_min

    Kc = (
        workpiece
        .material
        .specific_cutting_force_N_mm2
    )

    # --------------------------------------------------------
    # 1. RPM
    # --------------------------------------------------------

    rpm = calculate_rpm(
        Vc,
        D,
    )

    # --------------------------------------------------------
    # 2. CHIP AREA
    # --------------------------------------------------------

    Ac = calculate_chip_area(
        ap,
        f,
    )

    # --------------------------------------------------------
    # 3. CUTTING FORCE
    # --------------------------------------------------------

    Fc = calculate_cutting_force(
        Ac,
        Kc,
    )

    # For this first model assume the calculated cutting
    # force is tangential.
    Ft = Fc

    # --------------------------------------------------------
    # 4. TORQUE
    # --------------------------------------------------------

    torque = calculate_torque(
        Ft,
        D,
    )

    # --------------------------------------------------------
    # 5. POWER
    # --------------------------------------------------------

    power = calculate_power(
        Ft,
        Vc,
    )

    # --------------------------------------------------------
    # 6. TOOL MOMENT
    # --------------------------------------------------------

    moment = calculate_tool_moment(
        Fc,
        tool.overhang_mm,
    )

    # --------------------------------------------------------
    # 7. BENDING STRESS
    # --------------------------------------------------------

    stress = calculate_bending_stress(
        moment,
        tool.width_mm,
        tool.height_mm,
    )

    # --------------------------------------------------------
    # 8. MATERIAL REMOVAL RATE
    # --------------------------------------------------------

    feed_mm_min = (
        f
        * rpm
    )

    # Q = Ac * feed velocity
    #
    # Here Ac is mm² and feed velocity is mm/min.
    #
    # Therefore Q is mm³/min.

    mrr_mm3_min = (
        Ac
        * feed_mm_min
    )

    return {
        "rpm": rpm,
        "chip_area_mm2": Ac,
        "cutting_force_N": Fc,
        "tangential_force_N": Ft,
        "torque_Nm": torque,
        "power_W": power,
        "feed_mm_min": feed_mm_min,
        "mrr_mm3_min": mrr_mm3_min,
        "tool_moment_Nm": moment,
        "tool_bending_stress_MPa": stress,
    }


# ============================================================
# VERIFICATION
# ============================================================

def verify(
    workpiece: Workpiece,
    machining: Machining,
    result: dict,
):

    print()
    print("=" * 65)
    print("VERIFICATION")
    print("=" * 65)

    # --------------------------------------------------------
    # RPM identity
    # --------------------------------------------------------

    calculated_speed = (
        math.pi
        * workpiece.diameter_mm
        * result["rpm"]
        / 1000.0
    )

    assert math.isclose(
        calculated_speed,
        machining.cutting_speed_m_min,
        rel_tol=1e-10,
    )

    print("✓ RPM equation")

    # --------------------------------------------------------
    # Force identity
    # --------------------------------------------------------

    expected_force = (
        workpiece
        .material
        .specific_cutting_force_N_mm2
        * result["chip_area_mm2"]
    )

    assert math.isclose(
        result["cutting_force_N"],
        expected_force,
        rel_tol=1e-10,
    )

    print("✓ Cutting-force equation")

    # --------------------------------------------------------
    # Power identity
    # --------------------------------------------------------

    expected_power = (
        result["tangential_force_N"]
        * machining.cutting_speed_m_min
        / 60.0
    )

    assert math.isclose(
        result["power_W"],
        expected_power,
        rel_tol=1e-10,
    )

    print("✓ Power equation")

    # --------------------------------------------------------
    # MRR identity
    # --------------------------------------------------------

    expected_mrr = (
        result["chip_area_mm2"]
        * result["feed_mm_min"]
    )

    assert math.isclose(
        result["mrr_mm3_min"],
        expected_mrr,
        rel_tol=1e-10,
    )

    print("✓ Material-removal-rate equation")

    print()
    print("All basic equations verified.")


# ============================================================
# REPORT
# ============================================================

def print_report(
    workpiece,
    tool,
    machining,
    result,
):

    print()
    print("=" * 65)
    print("032 — SIMPLE TURNING MODEL")
    print("=" * 65)

    print()
    print("WORKPIECE")
    print("-" * 65)

    print(
        f"Material:       "
        f"{workpiece.material.name}"
    )

    print(
        f"Diameter:       "
        f"{workpiece.diameter_mm:.2f} mm"
    )

    print()
    print("TOOL")
    print("-" * 65)

    print(
        f"Tool:           "
        f"{tool.material}"
    )

    print(
        f"Section:        "
        f"{tool.width_mm:.1f} x "
        f"{tool.height_mm:.1f} mm"
    )

    print(
        f"Overhang:       "
        f"{tool.overhang_mm:.1f} mm"
    )

    print()
    print("CUTTING PARAMETERS")
    print("-" * 65)

    print(
        f"Depth of cut:   "
        f"{machining.depth_of_cut_mm:.3f} mm"
    )

    print(
        f"Feed:           "
        f"{machining.feed_mm_rev:.3f} mm/rev"
    )

    print(
        f"Cutting speed:  "
        f"{machining.cutting_speed_m_min:.2f} m/min"
    )

    print()
    print("CALCULATED")
    print("-" * 65)

    print(
        f"RPM:             "
        f"{result['rpm']:.2f}"
    )

    print(
        f"Feed velocity:   "
        f"{result['feed_mm_min']:.2f} mm/min"
    )

    print(
        f"Chip area:       "
        f"{result['chip_area_mm2']:.4f} mm²"
    )

    print(
        f"Cutting force:   "
        f"{result['cutting_force_N']:.2f} N"
    )

    print(
        f"Torque:          "
        f"{result['torque_Nm']:.3f} N·m"
    )

    print(
        f"Power:            "
        f"{result['power_W']:.2f} W"
    )

    print(
        f"MRR:              "
        f"{result['mrr_mm3_min']:.2f} mm³/min"
    )

    print()
    print("TOOL MECHANICS")
    print("-" * 65)

    print(
        f"Tool moment:     "
        f"{result['tool_moment_Nm']:.3f} N·m"
    )

    print(
        f"Bending stress:  "
        f"{result['tool_bending_stress_MPa']:.2f} MPa"
    )

    print()
    print("=" * 65)


# ============================================================
# MAIN
# ============================================================

def main():

    result = calculate_cut(
        STOCK,
        HSS_TOOL,
        CUT,
    )

    print_report(
        STOCK,
        HSS_TOOL,
        CUT,
        result,
    )

    verify(
        STOCK,
        CUT,
        result,
    )

    print()
    print("MODEL STATUS")
    print("-" * 65)
    print(
        "Geometry:       analytical"
    )
    print(
        "Chip model:     simplified"
    )
    print(
        "Force model:    Fc = Kc * Ac"
    )
    print(
        "Tool model:     cantilever beam"
    )
    print(
        "Dynamics:       not yet implemented"
    )
    print(
        "PyBullet:       next stage"
    )
    print(
        "Fields:         future stage"
    )


if __name__ == "__main__":
    main()
