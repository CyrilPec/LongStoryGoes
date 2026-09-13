"""
032+01.py
=========

GEOMETRY-DERIVED TURNING MODEL
==============================

032.py used:

    Ac = ap * f

This version makes the geometry responsible for the cutting
area.

The model is still intentionally simple and 2D.

---------------------------------------------------------------

CORE IDEA
---------

Represent the workpiece profile as:

    radius R(z)

Represent the cutter as a geometric region.

At each tool position:

    engagement = workpiece ∩ cutter

The removed cross-sectional area is calculated from the
intersection.

Then:

    area
      ↓
    force
      ↓
    torque
      ↓
    power
      ↓
    tool moment
      ↓
    stress

The geometry therefore drives the mechanics.

---------------------------------------------------------------

IMPORTANT
---------

This is NOT yet a physical chip-formation model.

It does not calculate:

    plastic deformation
    shear bands
    fracture
    realistic chip curling
    temperature
    friction
    residual stress

Those belong to later models.

This version verifies the geometric/mechanical chain first.

---------------------------------------------------------------

MODEL
-----

Workpiece profile:

    R(z)

Cutter position:

    x_tool(z)

At each z:

    removed radial depth =
        R_original(z) - R_final(z)

For a turning cut:

    dA = [R_original - R_current] dz

Therefore the removed cross-sectional area is obtained
directly from geometry.

For force estimation we still use:

    Fc = Kc * Ac

but now Ac comes from geometry rather than simply:

    ap * f

---------------------------------------------------------------
"""

import math
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PARAMETERS
# ============================================================

STOCK_DIAMETER_MM = 20.0
STOCK_LENGTH_MM = 80.0

CUT_START_MM = 15.0
CUT_END_MM = 65.0

DEPTH_OF_CUT_MM = 2.0

FEED_MM_REV = 0.10
CUTTING_SPEED_M_MIN = 20.0

KC_N_MM2 = 1500.0

TOOL_WIDTH_MM = 10.0
TOOL_HEIGHT_MM = 10.0
TOOL_OVERHANG_MM = 30.0

POINTS = 1001


# ============================================================
# WORKPIECE GRAPH
# ============================================================

@dataclass
class WorkpieceGraph:

    z: np.ndarray
    radius: np.ndarray

    original_radius: np.ndarray

    @classmethod
    def cylindrical(
        cls,
        diameter_mm,
        length_mm,
        points=POINTS,
    ):

        z = np.linspace(
            0.0,
            length_mm,
            points,
        )

        radius = np.full_like(
            z,
            diameter_mm / 2.0,
        )

        return cls(
            z=z,
            radius=radius.copy(),
            original_radius=radius.copy(),
        )

    # --------------------------------------------------------
    # Boolean-like radial removal
    # --------------------------------------------------------

    def remove_radial_layer(
        self,
        z_start_mm,
        z_end_mm,
        depth_mm,
    ):

        mask = (
            (self.z >= z_start_mm)
            &
            (self.z <= z_end_mm)
        )

        self.radius[mask] = np.maximum(
            self.radius[mask] - depth_mm,
            0.01,
        )

    # --------------------------------------------------------
    # Removed area
    # --------------------------------------------------------

    def removed_area(
        self,
        z_start_mm,
        z_end_mm,
    ):

        mask = (
            (self.z >= z_start_mm)
            &
            (self.z <= z_end_mm)
        )

        removed_radius = (
            self.original_radius[mask]
            - self.radius[mask]
        )

        # Cross-sectional area in the radius/z plane.
        #
        # This is a geometric engagement measure.
        #
        # We integrate removed radial depth along z.

        area = np.trapezoid(
            removed_radius,
            self.z[mask],
        )

        return area

    # --------------------------------------------------------
    # Local engagement area
    # --------------------------------------------------------

    def local_removed_depth(
        self,
        z_position_mm,
    ):

        index = np.argmin(
            np.abs(
                self.z
                - z_position_mm
            )
        )

        return (
            self.original_radius[index]
            - self.radius[index]
        )


# ============================================================
# CUTTING MODEL
# ============================================================

class CuttingModel:

    def __init__(
        self,
        kc_N_mm2=KC_N_MM2,
    ):

        self.kc = kc_N_mm2

    def force_from_area(
        self,
        area_mm2,
    ):

        return (
            self.kc
            * area_mm2
        )

    def rpm(
        self,
        diameter_mm,
    ):

        return (
            1000.0
            * CUTTING_SPEED_M_MIN
            / (
                math.pi
                * diameter_mm
            )
        )

    def torque(
        self,
        force_N,
        diameter_mm,
    ):

        radius_m = (
            diameter_mm
            / 2.0
            / 1000.0
        )

        return (
            force_N
            * radius_m
        )

    def power(
        self,
        force_N,
    ):

        velocity_m_s = (
            CUTTING_SPEED_M_MIN
            / 60.0
        )

        return (
            force_N
            * velocity_m_s
        )


# ============================================================
# TOOL MECHANICS
# ============================================================

def tool_second_moment(
    width_mm,
    height_mm,
):

    return (
        width_mm
        * height_mm**3
        / 12.0
    )


def tool_bending_stress(
    force_N,
    overhang_mm,
    width_mm,
    height_mm,
):

    L_mm = overhang_mm

    # M = F L
    M_Nmm = (
        force_N
        * L_mm
    )

    I = tool_second_moment(
        width_mm,
        height_mm,
    )

    c = height_mm / 2.0

    return (
        M_Nmm
        * c
        / I
    )


# ============================================================
# SIMULATION
# ============================================================

def run_simulation():

    graph = WorkpieceGraph.cylindrical(
        STOCK_DIAMETER_MM,
        STOCK_LENGTH_MM,
    )

    cutter = CuttingModel()

    # --------------------------------------------------------
    # Move cutter progressively through the workpiece.
    # --------------------------------------------------------

    positions = np.linspace(
        CUT_START_MM,
        CUT_END_MM,
        100,
    )

    history = []

    for z_tool in positions:

        # The cutter removes material behind its position.
        #
        # This creates a growing machined region.

        graph.remove_radial_layer(
            CUT_START_MM,
            z_tool,
            DEPTH_OF_CUT_MM,
        )

        # ----------------------------------------------------
        # Geometry-derived removed area
        # ----------------------------------------------------

        area = graph.removed_area(
            CUT_START_MM,
            z_tool,
        )

        # ----------------------------------------------------
        # Convert area to force
        # ----------------------------------------------------

        force = cutter.force_from_area(
            area
        )

        # Current local diameter.
        local_depth = (
            graph.local_removed_depth(
                z_tool
            )
        )

        current_diameter = (
            STOCK_DIAMETER_MM
            - 2.0 * local_depth
        )

        current_diameter = max(
            current_diameter,
            0.01,
        )

        rpm = cutter.rpm(
            current_diameter
        )

        torque = cutter.torque(
            force,
            current_diameter,
        )

        power = cutter.power(
            force
        )

        stress = tool_bending_stress(
            force,
            TOOL_OVERHANG_MM,
            TOOL_WIDTH_MM,
            TOOL_HEIGHT_MM,
        )

        history.append({
            "z": z_tool,
            "area": area,
            "force": force,
            "diameter": current_diameter,
            "rpm": rpm,
            "torque": torque,
            "power": power,
            "stress": stress,
        })

    return graph, history


# ============================================================
# REPORT
# ============================================================

def print_report(
    history,
):

    last = history[-1]

    print()
    print("=" * 70)
    print("032+01 — GEOMETRY-DERIVED TURNING")
    print("=" * 70)

    print()
    print("FINAL CUT")
    print("-" * 70)

    print(
        f"Tool position:       "
        f"{last['z']:.2f} mm"
    )

    print(
        f"Removed area:        "
        f"{last['area']:.4f} mm²"
    )

    print(
        f"Cutting force:       "
        f"{last['force']:.2f} N"
    )

    print(
        f"Current diameter:    "
        f"{last['diameter']:.3f} mm"
    )

    print(
        f"RPM:                 "
        f"{last['rpm']:.2f}"
    )

    print(
        f"Torque:              "
        f"{last['torque']:.4f} N*m"
    )

    print(
        f"Power:               "
        f"{last['power']:.2f} W"
    )

    print(
        f"Tool bending stress: "
        f"{last['stress']:.2f} MPa"
    )

    print()
    print("=" * 70)


# ============================================================
# PLOTS
# ============================================================

def plot_results(
    graph,
    history,
):

    z = graph.z

    positions = np.array(
        [x["z"] for x in history]
    )

    forces = np.array(
        [x["force"] for x in history]
    )

    areas = np.array(
        [x["area"] for x in history]
    )

    stresses = np.array(
        [x["stress"] for x in history]
    )

    diameters = np.array(
        [x["diameter"] for x in history]
    )

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8),
    )

    # --------------------------------------------------------
    # Geometry
    # --------------------------------------------------------

    ax = axes[0, 0]

    ax.plot(
        z,
        graph.original_radius,
        "--",
        label="Original",
    )

    ax.plot(
        z,
        graph.radius,
        linewidth=2,
        label="Machined",
    )

    ax.set_title(
        "Workpiece graph"
    )

    ax.set_xlabel(
        "Z [mm]"
    )

    ax.set_ylabel(
        "Radius [mm]"
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend()

    # --------------------------------------------------------
    # Area
    # --------------------------------------------------------

    ax = axes[0, 1]

    ax.plot(
        positions,
        areas,
        color="orange",
        linewidth=2,
    )

    ax.set_title(
        "Geometry-derived removed area"
    )

    ax.set_xlabel(
        "Tool position [mm]"
    )

    ax.set_ylabel(
        "Area [mm²]"
    )

    ax.grid(
        alpha=0.3
    )

    # --------------------------------------------------------
    # Force
    # --------------------------------------------------------

    ax = axes[1, 0]

    ax.plot(
        positions,
        forces,
        color="red",
        linewidth=2,
    )

    ax.set_title(
        "Cutting force"
    )

    ax.set_xlabel(
        "Tool position [mm]"
    )

    ax.set_ylabel(
        "Force [N]"
    )

    ax.grid(
        alpha=0.3
    )

    # --------------------------------------------------------
    # Tool stress
    # --------------------------------------------------------

    ax = axes[1, 1]

    ax.plot(
        positions,
        stresses,
        color="purple",
        linewidth=2,
    )

    ax.set_title(
        "Tool bending stress"
    )

    ax.set_xlabel(
        "Tool position [mm]"
    )

    ax.set_ylabel(
        "Stress [MPa]"
    )

    ax.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# SIMPLE TEST
# ============================================================

def verify_geometry():

    graph = WorkpieceGraph.cylindrical(
        20.0,
        80.0,
    )

    graph.remove_radial_layer(
        20.0,
        60.0,
        2.0,
    )

    area = graph.removed_area(
        20.0,
        60.0,
    )

    # Expected:

    # removed radial depth = 2 mm
    # length = 40 mm
    #
    # area in the profile plane:
    #
    # 2 * 40 = 80 mm²

    expected = 80.0

    assert math.isclose(
        area,
        expected,
        rel_tol=1e-4,
    )

    print(
        "✓ Geometry-area verification passed"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    verify_geometry()

    graph, history = run_simulation()

    print_report(
        history
    )

    plot_results(
        graph,
        history
    )


if __name__ == "__main__":
    main()
