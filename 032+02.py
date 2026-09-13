"""
032+02.py
=========

GEOMETRY + CUTTING FORCE + PYBULLET
===================================

This is the next layer after 032+01.

Architecture:

    WORKPIECE GRAPH
          |
          v
    GEOMETRIC ENGAGEMENT
          |
          v
      CHIP AREA
          |
          v
      CUTTING FORCE
          |
          v
    FORCE VECTOR
          |
          +------------------+
          |                  |
          v                  v
       PyBullet          tool mechanics
          |                  |
          v                  v
       motion             moment/stress


PyBullet is NOT responsible for calculating the metal
cutting force.

Our machining model calculates it.

PyBullet receives that force and simulates the mechanical
response.

---------------------------------------------------------------

CURRENT SIMPLIFICATIONS
-----------------------

1. Cylindrical workpiece.
2. Simplified radial turning.
3. Simplified cutting-force coefficient.
4. Rigid PyBullet tool.
5. Force applied at the cutting point.
6. No plastic deformation.
7. No realistic chip formation yet.
8. No thermal model yet.
9. No friction calibration yet.

The purpose is to establish the interface between:

    machining mathematics

and:

    rigid-body mechanics.


---------------------------------------------------------------

DEPENDENCIES
------------

    pip install numpy matplotlib pybullet


---------------------------------------------------------------

COORDINATES
-----------

PyBullet:

    X = spindle axis
    Y = radial direction
    Z = vertical

The workpiece rotates around X.

The cutting point is approximately:

    (x, y, z)

with the cutter approaching in the radial direction.


---------------------------------------------------------------
"""

import math
import time

from dataclasses import dataclass

import numpy as np
import pybullet as p
import pybullet_data


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

SIMULATION_FPS = 240

MM = 0.001


# ============================================================
# UNIT CONVERSION
# ============================================================

def m(mm_value):
    return mm_value * MM


# ============================================================
# WORKPIECE GRAPH
# ============================================================

class WorkpieceGraph:

    def __init__(
        self,
        diameter_mm,
        length_mm,
        points=1001,
    ):

        self.z = np.linspace(
            0.0,
            length_mm,
            points,
        )

        self.original_radius = np.full_like(
            self.z,
            diameter_mm / 2.0,
        )

        self.radius = self.original_radius.copy()

    # --------------------------------------------------------
    # Remove radial material
    # --------------------------------------------------------

    def remove(
        self,
        z_start,
        z_end,
        depth,
    ):

        mask = (
            (self.z >= z_start)
            &
            (self.z <= z_end)
        )

        self.radius[mask] = np.maximum(
            self.radius[mask] - depth,
            0.01,
        )

    # --------------------------------------------------------
    # Removed profile area
    # --------------------------------------------------------

    def removed_area(
        self,
        z_start,
        z_end,
    ):

        mask = (
            (self.z >= z_start)
            &
            (self.z <= z_end)
        )

        depth = (
            self.original_radius[mask]
            - self.radius[mask]
        )

        return np.trapezoid(
            depth,
            self.z[mask],
        )

    # --------------------------------------------------------
    # Local diameter
    # --------------------------------------------------------

    def local_diameter(
        self,
        z_position,
    ):

        i = np.argmin(
            np.abs(
                self.z
                - z_position
            )
        )

        return (
            2.0
            * self.radius[i]
        )


# ============================================================
# CUTTING MODEL
# ============================================================

@dataclass
class CuttingResult:

    area_mm2: float

    force_N: float

    Ft_N: float

    Fr_N: float

    Fa_N: float

    rpm: float

    torque_Nm: float

    power_W: float


class CuttingModel:

    def __init__(
        self,
        kc_N_mm2,
    ):

        self.kc = kc_N_mm2

    def calculate(
        self,
        area_mm2,
        diameter_mm,
    ):

        # ----------------------------------------------------
        # Cutting force
        # ----------------------------------------------------

        force = (
            self.kc
            * area_mm2
        )

        # ----------------------------------------------------
        # First force decomposition.
        #
        # We initially assume:
        #
        #       Ft = Fc
        #
        # and smaller radial/axial components.
        #
        # These coefficients should eventually come from
        # the actual tool geometry and experiments.
        # ----------------------------------------------------

        Ft = force

        Fr = 0.30 * force

        Fa = 0.10 * force

        # Resultant
        resultant = math.sqrt(
            Ft**2
            + Fr**2
            + Fa**2
        )

        # ----------------------------------------------------
        # RPM
        # ----------------------------------------------------

        rpm = (
            1000.0
            * CUTTING_SPEED_M_MIN
            / (
                math.pi
                * diameter_mm
            )
        )

        # ----------------------------------------------------
        # Torque
        # ----------------------------------------------------

        radius_m = (
            diameter_mm
            / 2.0
            / 1000.0
        )

        torque = (
            Ft
            * radius_m
        )

        # ----------------------------------------------------
        # Power
        # ----------------------------------------------------

        power = (
            Ft
            * CUTTING_SPEED_M_MIN
            / 60.0
        )

        return CuttingResult(
            area_mm2=area_mm2,
            force_N=resultant,
            Ft_N=Ft,
            Fr_N=Fr,
            Fa_N=Fa,
            rpm=rpm,
            torque_Nm=torque,
            power_W=power,
        )


# ============================================================
# PYBULLET LATHE
# ============================================================

class BulletLathe:

    def __init__(self):

        self.client = p.connect(
            p.GUI
        )

        p.setAdditionalSearchPath(
            pybullet_data.getDataPath()
        )

        p.resetSimulation()

        p.setGravity(
            0,
            0,
            0,
        )

        p.setTimeStep(
            1.0 / SIMULATION_FPS
        )

        # ----------------------------------------------------
        # Camera
        # ----------------------------------------------------

        p.resetDebugVisualizerCamera(
            cameraDistance=0.13,
            cameraYaw=45,
            cameraPitch=-25,
            cameraTargetPosition=[
                0,
                0,
                0,
            ],
        )

        # ----------------------------------------------------
        # Workpiece
        # ----------------------------------------------------

        self.workpiece_radius = m(
            STOCK_DIAMETER_MM / 2.0
        )

        self.workpiece_length = m(
            STOCK_LENGTH_MM
        )

        collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=self.workpiece_radius,
            height=self.workpiece_length,
        )

        visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=self.workpiece_radius,
            length=self.workpiece_length,
            rgbaColor=[
                0.55,
                0.58,
                0.62,
                1,
            ],
        )

        self.workpiece = p.createMultiBody(
            baseMass=5.0,
            baseCollisionShapeIndex=collision,
            baseVisualShapeIndex=visual,
            basePosition=[
                0,
                0,
                0,
            ],
            baseOrientation=p.getQuaternionFromEuler(
                [0, math.pi / 2, 0]
            ),
        )

        # ----------------------------------------------------
        # Tool
        # ----------------------------------------------------

        half = m(
            TOOL_WIDTH_MM / 2.0
        )

        tool_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[
                half,
                half,
                half,
            ],
        )

        tool_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[
                half,
                half,
                half,
            ],
            rgbaColor=[
                0.95,
                0.55,
                0.10,
                1,
            ],
        )

        # Tool location:
        #
        # X = near the cutting region
        # Y = radial direction
        # Z = vertical

        self.tool_position = [
            m(40.0),
            self.workpiece_radius
            + m(TOOL_WIDTH_MM / 2.0)
            - m(DEPTH_OF_CUT_MM),
            0,
        ]

        self.tool = p.createMultiBody(
            baseMass=0.5,
            baseCollisionShapeIndex=tool_collision,
            baseVisualShapeIndex=tool_visual,
            basePosition=self.tool_position,
        )

        # ----------------------------------------------------
        # Force visualization IDs
        # ----------------------------------------------------

        self.debug_lines = []

    # ========================================================
    # CONTACT POINT
    # ========================================================

    def contact_point(
        self,
        z_position_mm,
        diameter_mm,
    ):

        radius = m(
            diameter_mm / 2.0
        )

        return [
            m(z_position_mm),
            radius,
            0,
        ]

    # ========================================================
    # DRAW VECTOR
    # ========================================================

    def draw_force_vector(
        self,
        point,
        Ft,
        Fr,
        Fa,
    ):

        # Delete old vectors.
        for line in self.debug_lines:

            try:
                p.removeUserDebugItem(
                    line
                )
            except Exception:
                pass

        self.debug_lines.clear()

        # Visualization scale.
        #
        # Real forces are much larger than the dimensions
        # of this demonstration.

        scale = 0.000005

        # Tangential: X
        Ft_end = [
            point[0] + Ft * scale,
            point[1],
            point[2],
        ]

        # Radial: Y
        Fr_end = [
            point[0],
            point[1] + Fr * scale,
            point[2],
        ]

        # Axial: Z
        Fa_end = [
            point[0],
            point[1],
            point[2] + Fa * scale,
        ]

        self.debug_lines.append(
            p.addUserDebugLine(
                point,
                Ft_end,
                lineColorRGB=[
                    1,
                    0,
                    0,
                ],
                lineWidth=4,
            )
        )

        self.debug_lines.append(
            p.addUserDebugLine(
                point,
                Fr_end,
                lineColorRGB=[
                    0,
                    1,
                    0,
                ],
                lineWidth=4,
            )
        )

        self.debug_lines.append(
            p.addUserDebugLine(
                point,
                Fa_end,
                lineColorRGB=[
                    0,
                    0.5,
                    1,
                ],
                lineWidth=4,
            )
        )

    # ========================================================
    # APPLY FORCE
    # ========================================================

    def apply_force(
        self,
        point,
        result,
    ):

        # ----------------------------------------------------
        # Force vector in WORLD coordinates.
        #
        # X = tangential / cutting direction
        # Y = radial
        # Z = axial
        # ----------------------------------------------------

        force = [
            result.Ft_N,
            result.Fr_N,
            result.Fa_N,
        ]

        p.applyExternalForce(
            objectUniqueId=self.tool,
            linkIndex=-1,
            forceObj=force,
            posObj=point,
            flags=p.WORLD_FRAME,
        )

        self.draw_force_vector(
            point,
            result.Ft_N,
            result.Fr_N,
            result.Fa_N,
        )

    # ========================================================
    # SPINDLE
    # ========================================================

    def rotate_workpiece(
        self,
        rpm,
    ):

        omega = (
            rpm
            * 2.0
            * math.pi
            / 60.0
        )

        angle = (
            omega
            / SIMULATION_FPS
        )

        position, orientation = (
            p.getBasePositionAndOrientation(
                self.workpiece
            )
        )

        rotation = p.getQuaternionFromEuler(
            [
                angle,
                0,
                0,
            ]
        )

        new_orientation = p.multiplyTransforms(
            [0, 0, 0],
            rotation,
            [0, 0, 0],
            orientation,
        )[1]

        p.resetBasePositionAndOrientation(
            self.workpiece,
            position,
            new_orientation,
        )

    # ========================================================
    # SIMULATION STEP
    # ========================================================

    def step(
        self,
        point,
        result,
    ):

        self.apply_force(
            point,
            result,
        )

        self.rotate_workpiece(
            result.rpm
        )

        p.stepSimulation()


# ============================================================
# TOOL MECHANICS
# ============================================================

def calculate_tool_stress(
    force_N,
):

    L = TOOL_OVERHANG_MM

    b = TOOL_WIDTH_MM

    h = TOOL_HEIGHT_MM

    # Cantilever moment
    M = (
        force_N
        * L
    )

    # Rectangular section
    I = (
        b
        * h**3
        / 12.0
    )

    c = h / 2.0

    sigma = (
        M
        * c
        / I
    )

    return M, sigma


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("032+02 — GEOMETRY + FORCE + PYBULLET")
    print("=" * 70)

    # --------------------------------------------------------
    # Geometry
    # --------------------------------------------------------

    graph = WorkpieceGraph(
        STOCK_DIAMETER_MM,
        STOCK_LENGTH_MM,
    )

    # --------------------------------------------------------
    # Cutting model
    # --------------------------------------------------------

    cutting = CuttingModel(
        KC_N_MM2
    )

    # --------------------------------------------------------
    # PyBullet
    # --------------------------------------------------------

    simulation = BulletLathe()

    # --------------------------------------------------------
    # Simulate progressive cut
    # --------------------------------------------------------

    positions = np.linspace(
        CUT_START_MM,
        CUT_END_MM,
        300,
    )

    for z_position in positions:

        # ----------------------------------------------------
        # Update geometry
        # ----------------------------------------------------

        graph.remove(
            CUT_START_MM,
            z_position,
            DEPTH_OF_CUT_MM,
        )

        # ----------------------------------------------------
        # Current local diameter
        # ----------------------------------------------------

        diameter = (
            graph.local_diameter(
                z_position
            )
        )

        # ----------------------------------------------------
        # Geometric engagement
        # ----------------------------------------------------

        area = graph.removed_area(
            CUT_START_MM,
            z_position,
        )

        # ----------------------------------------------------
        # Cutting physics
        # ----------------------------------------------------

        result = cutting.calculate(
            area,
            diameter,
        )

        # ----------------------------------------------------
        # Contact point
        # ----------------------------------------------------

        point = simulation.contact_point(
            z_position,
            diameter,
        )

        # ----------------------------------------------------
        # Apply force to PyBullet
        # ----------------------------------------------------

        simulation.step(
            point,
            result,
        )

        # ----------------------------------------------------
        # Console status
        # ----------------------------------------------------

        if int(z_position) % 5 == 0:

            print(
                f"\rz={z_position:6.2f} mm | "
                f"A={area:8.3f} mm² | "
                f"F={result.force_N:9.1f} N | "
                f"RPM={result.rpm:7.1f}",
                end="",
            )

        time.sleep(
            1.0 / SIMULATION_FPS
        )

    # --------------------------------------------------------
    # Final mechanics
    # --------------------------------------------------------

    final = result

    moment, stress = (
        calculate_tool_stress(
            final.force_N
        )
    )

    print()
    print()
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(
        f"Cutting area:       "
        f"{final.area_mm2:.3f} mm²"
    )

    print(
        f"Resultant force:    "
        f"{final.force_N:.2f} N"
    )

    print(
        f"Ft:                 "
        f"{final.Ft_N:.2f} N"
    )

    print(
        f"Fr:                 "
        f"{final.Fr_N:.2f} N"
    )

    print(
        f"Fa:                 "
        f"{final.Fa_N:.2f} N"
    )

    print(
        f"RPM:                "
        f"{final.rpm:.2f}"
    )

    print(
        f"Torque:             "
        f"{final.torque_Nm:.4f} N*m"
    )

    print(
        f"Power:              "
        f"{final.power_W:.2f} W"
    )

    print(
        f"Tool moment:        "
        f"{moment / 1000.0:.4f} N*m"
    )

    print(
        f"Tool stress:        "
        f"{stress:.2f} MPa"
    )

    print()
    print("=" * 70)

    print(
        """
PyBullet is now receiving the calculated cutting force.

RED   = tangential force
GREEN = radial force
BLUE  = axial force

The next improvement should NOT be more arbitrary physics.

The next improvement should be:

    actual cutter geometry
            ↓
    actual workpiece/cutter intersection
            ↓
    instantaneous contact area
            ↓
    instantaneous force vector

Then we can make the force vary naturally as the tool moves.
"""
    )

    # Keep simulation open.
    while p.isConnected():

        p.stepSimulation()

        time.sleep(
            1.0 / SIMULATION_FPS
        )


if __name__ == "__main__":
    main()
