"""
031.py
======

Interactive 2D turning / material-removal experiment.

Idea
----
Transform machining into a sequence of simple representations:

    STOCK GRAPH
         +
    CUTTER GRAPH
         |
         v
    CUTTING AREA
         |
         v
    CUTTING FORCE
         |
         v
    FEED / SPEED / RPM
         |
         v
    FINAL SHAPE

This is deliberately NOT a full FEM or metal-cutting simulator.
The cutting-force model is a first-order approximation:

    Fc = Kc * Ac

where:
    Fc = cutting force [N]
    Kc = specific cutting force [N/mm²]
    Ac = instantaneous chip area [mm²]

For turning:

    Vc = pi * D * RPM / 1000

therefore:

    RPM = 1000 * Vc / (pi * D)

Feed velocity:

    Vf = feed * RPM

Material removal rate:

    Q = Ac * Vf

The geometry is represented by a 2D radius-vs-Z profile.
This is much simpler than starting with a 3D mesh.

Controls
--------
Use the sliders to change:

    Stock diameter
    Depth of cut
    Feed
    Cutting speed
    Kc (specific cutting force)
    Tool width

The plot shows:
    - current stock profile
    - target/current cut
    - tool
    - removed region

The numerical panel shows:
    - diameter
    - RPM
    - feed velocity
    - chip area
    - cutting force
    - torque
    - power
    - material removal rate

Dependencies
------------
    pip install numpy matplotlib
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


# ============================================================
# MATERIALS
# ============================================================

MATERIALS = {
    "AISI 1040": {
        "kc": 1500.0,       # N/mm², illustrative starting value
        "hardness": 180,    # HB, illustrative
    }
}


# ============================================================
# BASIC MACHINING FUNCTIONS
# ============================================================

def rpm_from_cutting_speed(speed_m_min, diameter_mm):
    """
    Calculate spindle RPM.

        Vc = pi * D * N / 1000

        N = 1000 * Vc / (pi * D)
    """
    if diameter_mm <= 0:
        return 0.0

    return 1000.0 * speed_m_min / (math.pi * diameter_mm)


def feed_velocity(feed_mm_rev, rpm):
    """
    Linear feed velocity in mm/min.

        Vf = f * N
    """
    return feed_mm_rev * rpm


def cutting_area(depth_mm, feed_mm_rev):
    """
    First-order chip cross-sectional area.

        Ac = depth * feed

    This is a simplified turning model.
    """
    return max(depth_mm, 0.0) * max(feed_mm_rev, 0.0)


def cutting_force(area_mm2, kc):
    """
    First-order cutting force.

        Fc = Kc * Ac
    """
    return max(area_mm2, 0.0) * max(kc, 0.0)


def cutting_torque(force_n, diameter_mm):
    """
    Approximate spindle torque.

        T = Fc * D / 2

    Units:
        N * mm -> converted to N*m
    """
    return force_n * (diameter_mm / 2.0) / 1000.0


def cutting_power(force_n, speed_m_min):
    """
    Approximate cutting power.

        P = Fc * V

    V must be converted from m/min to m/s.
    """
    velocity_m_s = speed_m_min / 60.0
    return force_n * velocity_m_s


def material_removal_rate(area_mm2, feed_mm_min):
    """
    Material removal rate.

        Q = Ac * Vf

    Result: mm³/min
    """
    return area_mm2 * feed_mm_min


# ============================================================
# GEOMETRY
# ============================================================

def make_stock_profile(
    diameter_mm=20.0,
    length_mm=80.0,
    points=500
):
    """
    Create the initial radius-vs-Z graph of cylindrical stock.
    """

    z = np.linspace(0.0, length_mm, points)
    radius = np.full_like(z, diameter_mm / 2.0)

    return z, radius


def make_turned_profile(
    diameter_mm,
    cut_start,
    cut_length,
    depth_mm,
    points=500
):
    """
    Create a simplified turned region.

    The tool removes material from cut_start to cut_start+cut_length.
    """

    z = np.linspace(
        cut_start,
        cut_start + cut_length,
        points
    )

    original_radius = diameter_mm / 2.0

    final_radius = max(
        0.05,
        original_radius - depth_mm
    )

    radius = np.full_like(z, final_radius)

    return z, radius


def calculate_removed_volume(
    diameter_mm,
    final_diameter_mm,
    length_mm
):
    """
    Volume removed from a cylindrical section.

        V = pi/4 * (D1² - D2²) * L

    Result: mm³
    """

    d1 = max(diameter_mm, 0.0)
    d2 = max(final_diameter_mm, 0.0)

    if d2 > d1:
        d2 = d1

    return (
        math.pi
        / 4.0
        * (d1**2 - d2**2)
        * length_mm
    )


# ============================================================
# TOOL
# ============================================================

def make_tool_shape(
    tool_z,
    tool_radius,
    width=2.0
):
    """
    Simple 2D representation of the cutting edge.

    This is intentionally geometric rather than a physical
    chip simulation.
    """

    z = np.array([
        tool_z,
        tool_z + width,
        tool_z + width,
        tool_z
    ])

    r = np.array([
        tool_radius,
        tool_radius,
        tool_radius + 4.0,
        tool_radius + 4.0
    ])

    return z, r


# ============================================================
# SIMULATION STATE
# ============================================================

class TurningSimulation:

    def __init__(self):

        self.stock_diameter = 20.0
        self.stock_length = 80.0

        self.depth = 2.0
        self.feed = 0.10

        self.cutting_speed = 20.0

        self.kc = MATERIALS["AISI 1040"]["kc"]

        self.tool_width = 2.0

        self.cut_start = 20.0
        self.cut_length = 40.0

    def calculate(self):

        # Diameter after cut
        final_diameter = (
            self.stock_diameter
            - 2.0 * self.depth
        )

        final_diameter = max(
            0.1,
            final_diameter
        )

        # Diameter used for RPM
        # Use current stock diameter as initial approximation.
        diameter_for_rpm = self.stock_diameter

        rpm = rpm_from_cutting_speed(
            self.cutting_speed,
            diameter_for_rpm
        )

        feed_mm_min = feed_velocity(
            self.feed,
            rpm
        )

        area = cutting_area(
            self.depth,
            self.feed
        )

        force = cutting_force(
            area,
            self.kc
        )

        torque = cutting_torque(
            force,
            diameter_for_rpm
        )

        power = cutting_power(
            force,
            self.cutting_speed
        )

        mrr = material_removal_rate(
            area,
            feed_mm_min
        )

        removed_volume = calculate_removed_volume(
            self.stock_diameter,
            final_diameter,
            self.cut_length
        )

        return {
            "final_diameter": final_diameter,
            "rpm": rpm,
            "feed_mm_min": feed_mm_min,
            "area": area,
            "force": force,
            "torque": torque,
            "power": power,
            "mrr": mrr,
            "removed_volume": removed_volume,
        }


# ============================================================
# INTERACTIVE VISUALIZATION
# ============================================================

class TurningGUI:

    def __init__(self):

        self.sim = TurningSimulation()

        self.fig = plt.figure(
            figsize=(13, 8)
        )

        self.ax = self.fig.add_axes(
            [0.07, 0.28, 0.62, 0.65]
        )

        self.info = self.fig.add_axes(
            [0.73, 0.28, 0.24, 0.65]
        )

        self.info.axis("off")

        # ----------------------------------------------------
        # Sliders
        # ----------------------------------------------------

        self.ax_diameter = self.fig.add_axes(
            [0.10, 0.21, 0.55, 0.025]
        )

        self.ax_depth = self.fig.add_axes(
            [0.10, 0.17, 0.55, 0.025]
        )

        self.ax_feed = self.fig.add_axes(
            [0.10, 0.13, 0.55, 0.025]
        )

        self.ax_speed = self.fig.add_axes(
            [0.10, 0.09, 0.55, 0.025]
        )

        self.ax_kc = self.fig.add_axes(
            [0.10, 0.05, 0.55, 0.025]
        )

        self.slider_diameter = Slider(
            self.ax_diameter,
            "Stock Ø",
            5.0,
            50.0,
            valinit=20.0,
            valstep=0.1
        )

        self.slider_depth = Slider(
            self.ax_depth,
            "Depth",
            0.1,
            5.0,
            valinit=2.0,
            valstep=0.1
        )

        self.slider_feed = Slider(
            self.ax_feed,
            "Feed mm/rev",
            0.01,
            0.5,
            valinit=0.10,
            valstep=0.01
        )

        self.slider_speed = Slider(
            self.ax_speed,
            "Cut speed m/min",
            1.0,
            100.0,
            valinit=20.0,
            valstep=1.0
        )

        self.slider_kc = Slider(
            self.ax_kc,
            "Kc N/mm²",
            500.0,
            3000.0,
            valinit=1500.0,
            valstep=50.0
        )

        # ----------------------------------------------------
        # Reset button
        # ----------------------------------------------------

        self.reset_ax = self.fig.add_axes(
            [0.70, 0.09, 0.10, 0.04]
        )

        self.reset_button = Button(
            self.reset_ax,
            "Reset"
        )

        # Connect events
        self.slider_diameter.on_changed(
            self.update
        )

        self.slider_depth.on_changed(
            self.update
        )

        self.slider_feed.on_changed(
            self.update
        )

        self.slider_speed.on_changed(
            self.update
        )

        self.slider_kc.on_changed(
            self.update
        )

        self.reset_button.on_clicked(
            self.reset
        )

        self.update(None)

    # ========================================================
    # DRAW
    # ========================================================

    def update(self, _):

        self.sim.stock_diameter = (
            self.slider_diameter.val
        )

        self.sim.depth = (
            self.slider_depth.val
        )

        self.sim.feed = (
            self.slider_feed.val
        )

        self.sim.cutting_speed = (
            self.slider_speed.val
        )

        self.sim.kc = (
            self.slider_kc.val
        )

        result = self.sim.calculate()

        self.ax.clear()

        # ----------------------------------------------------
        # Stock graph
        # ----------------------------------------------------

        z_stock, r_stock = make_stock_profile(
            self.sim.stock_diameter,
            self.sim.stock_length
        )

        self.ax.plot(
            z_stock,
            r_stock,
            color="black",
            linewidth=2,
            label="Original stock"
        )

        self.ax.plot(
            z_stock,
            -r_stock,
            color="black",
            linewidth=2
        )

        # ----------------------------------------------------
        # Final turned region
        # ----------------------------------------------------

        z_cut, r_cut = make_turned_profile(
            self.sim.stock_diameter,
            self.sim.cut_start,
            self.sim.cut_length,
            self.sim.depth
        )

        self.ax.plot(
            z_cut,
            r_cut,
            color="blue",
            linewidth=3,
            label="Final surface"
        )

        self.ax.plot(
            z_cut,
            -r_cut,
            color="blue",
            linewidth=3
        )

        # ----------------------------------------------------
        # Removed region
        # ----------------------------------------------------

        r_original = self.sim.stock_diameter / 2.0

        self.ax.fill_between(
            z_cut,
            r_cut,
            r_original,
            color="red",
            alpha=0.25,
            label="Removed material"
        )

        self.ax.fill_between(
            z_cut,
            -r_cut,
            -r_original,
            color="red",
            alpha=0.25
        )

        # ----------------------------------------------------
        # Tool
        # ----------------------------------------------------

        tool_z = (
            self.sim.cut_start
            + self.sim.cut_length / 2.0
        )

        tool_radius = (
            r_original
            - self.sim.depth
        )

        tz, tr = make_tool_shape(
            tool_z,
            tool_radius,
            self.sim.tool_width
        )

        self.ax.fill(
            tz,
            tr,
            color="orange",
            alpha=0.8,
            label="Cutter"
        )

        # ----------------------------------------------------
        # Axes
        # ----------------------------------------------------

        self.ax.axhline(
            0,
            color="gray",
            linewidth=1
        )

        self.ax.set_title(
            "030 — 2D Turning / Graph-Based Material Removal"
        )

        self.ax.set_xlabel(
            "Z position [mm]"
        )

        self.ax.set_ylabel(
            "Radius [mm]"
        )

        self.ax.grid(
            True,
            alpha=0.25
        )

        self.ax.legend(
            loc="upper right"
        )

        self.ax.set_xlim(
            0,
            self.sim.stock_length
        )

        self.ax.set_ylim(
            -self.sim.stock_diameter / 2 - 5,
            self.sim.stock_diameter / 2 + 5
        )

        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        self.info.clear()
        self.info.axis("off")

        text = f"""
MACHINING STATE

Material
  AISI 1040

Stock
  Diameter: {self.sim.stock_diameter:.2f} mm
  Length:   {self.sim.stock_length:.1f} mm

CUT

  Depth:       {self.sim.depth:.2f} mm
  Feed:        {self.sim.feed:.3f} mm/rev
  Speed:       {self.sim.cutting_speed:.1f} m/min

GEOMETRY

  Chip area:
    {result["area"]:.4f} mm²

  Final diameter:
    {result["final_diameter"]:.2f} mm

  Removed volume:
    {result["removed_volume"]:.1f} mm³

PHYSICS

  Kc:
    {self.sim.kc:.0f} N/mm²

  Cutting force:
    {result["force"]:.1f} N

  Torque:
    {result["torque"]:.3f} N·m

  Power:
    {result["power"]:.1f} W

MOTION

  RPM:
    {result["rpm"]:.1f}

  Feed velocity:
    {result["feed_mm_min"]:.2f} mm/min

  Removal rate:
    {result["mrr"]:.1f} mm³/min
"""

        self.info.text(
            0.02,
            0.98,
            text,
            verticalalignment="top",
            family="monospace",
            fontsize=10
        )

        self.fig.canvas.draw_idle()

    # ========================================================
    # RESET
    # ========================================================

    def reset(self, _):

        self.slider_diameter.reset()
        self.slider_depth.reset()
        self.slider_feed.reset()
        self.slider_speed.reset()
        self.slider_kc.reset()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("030 — Graph-Based Machining Simulation")
    print("=" * 60)

    gui = TurningGUI()

    plt.show()
