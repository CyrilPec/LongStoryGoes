"""
032+03.py
=========

KIENZLE CUTTING-FORCE MODEL + VALIDATION FRAMEWORK
===================================================

Purpose
-------

Upgrade the simplified model:

    Fc = Kc * A

to the established Kienzle/Victor form:

    Fc = b * kc1_1 * h**(1 - mc)

where:

    Fc      = main cutting force [N]
    b       = uncut chip width [mm]
    h       = uncut chip thickness [mm]
    kc1_1   = specific cutting force at h = 1 mm [N/mm²]
    mc      = material exponent [-]

For a simple 90-degree turning approximation:

    b = depth of cut
    h = feed per revolution

Therefore:

    Fc = ap * kc1_1 * f**(1-mc)

---------------------------------------------------------------

IMPORTANT SCIENTIFIC POINT
---------------------------

kc1_1 and mc depend on:

    workpiece material
    tool material
    rake angle
    cutting-edge geometry
    cutting speed
    chip thickness
    lubrication/cooling
    material condition

Therefore this file does NOT pretend that one universal pair
of coefficients exists for AISI 1040 + HSS.

Instead:

    1. coefficients are explicit inputs;
    2. experimental data can be entered;
    3. prediction error is calculated;
    4. coefficients can later be fitted from experiments.

This is the correct direction for research.

---------------------------------------------------------------

VALIDATION DATA
---------------

The file contains an example dataset from published AISI 1040
turning work.

Do NOT treat this dataset as validation of YOUR exact tool.

The published experiment used its own:

    tool geometry
    machine
    workpiece dimensions
    cutting conditions
    dynamometer

Therefore it is useful as an external benchmark, while actual
validation of our model requires matching our own experimental
conditions.

---------------------------------------------------------------

MODEL HIERARCHY
---------------

geometry
    ↓
uncut chip width b
    ↓
uncut chip thickness h
    ↓
Kienzle equation
    ↓
cutting force Fc
    ↓
torque
    ↓
power

Later:

geometry
    ↓
actual contact
    ↓
local b(x)
    ↓
local h(x)
    ↓
local force density
    ↓
integrated force

---------------------------------------------------------------
"""

import math
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# KIENZLE MODEL
# ============================================================

@dataclass
class KienzleParameters:

    # Specific cutting force at:
    #
    # b = 1 mm
    # h = 1 mm
    #
    # [N/mm²]

    kc1_1: float

    # Material exponent.

    mc: float

    name: str = "Calibration"


class KienzleModel:

    def __init__(
        self,
        parameters: KienzleParameters,
    ):

        self.parameters = parameters

    # --------------------------------------------------------
    # Specific cutting force
    # --------------------------------------------------------

    def specific_cutting_force(
        self,
        h_mm,
    ):

        kc1_1 = (
            self.parameters.kc1_1
        )

        mc = (
            self.parameters.mc
        )

        return (
            kc1_1
            * h_mm ** (-mc)
        )

    # --------------------------------------------------------
    # Main cutting force
    # --------------------------------------------------------

    def cutting_force(
        self,
        b_mm,
        h_mm,
    ):

        kc1_1 = (
            self.parameters.kc1_1
        )

        mc = (
            self.parameters.mc
        )

        return (
            b_mm
            * kc1_1
            * h_mm ** (1.0 - mc)
        )

    # --------------------------------------------------------
    # Simplified turning interface
    # --------------------------------------------------------

    def turning_force(
        self,
        depth_of_cut_mm,
        feed_mm_rev,
    ):

        b = depth_of_cut_mm

        h = feed_mm_rev

        return self.cutting_force(
            b,
            h,
        )


# ============================================================
# MACHINING EQUATIONS
# ============================================================

def spindle_rpm(
    cutting_speed_m_min,
    diameter_mm,
):

    return (
        1000.0
        * cutting_speed_m_min
        / (
            math.pi
            * diameter_mm
        )
    )


def cutting_power(
    force_N,
    cutting_speed_m_min,
):

    velocity_m_s = (
        cutting_speed_m_min
        / 60.0
    )

    return (
        force_N
        * velocity_m_s
    )


def spindle_torque(
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


# ============================================================
# SINGLE CUT CALCULATION
# ============================================================

def calculate_cut(
    model,
    diameter_mm,
    depth_of_cut_mm,
    feed_mm_rev,
    cutting_speed_m_min,
):

    force = model.turning_force(
        depth_of_cut_mm,
        feed_mm_rev,
    )

    rpm = spindle_rpm(
        cutting_speed_m_min,
        diameter_mm,
    )

    torque = spindle_torque(
        force,
        diameter_mm,
    )

    power = cutting_power(
        force,
        cutting_speed_m_min,
    )

    return {
        "force_N": force,
        "rpm": rpm,
        "torque_Nm": torque,
        "power_W": power,
    }


# ============================================================
# EXPERIMENTAL DATA STRUCTURE
# ============================================================

@dataclass
class Experiment:

    speed_m_min: float

    feed_mm_rev: float

    depth_mm: float

    measured_force_N: float


# ============================================================
# EXAMPLE PUBLISHED AISI 1040 DATA
# ============================================================

"""
Example values below come from a published AISI 1040 turning
study.

They are included as a benchmark dataset.

The exact experimental setup must be considered when comparing
against these values.

Do not use them as universal coefficients for your machine/tool.
"""

EXPERIMENTS = [

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.2,
        depth_mm=0.2,
        measured_force_N=359.1,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.2,
        depth_mm=0.4,
        measured_force_N=357.3,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.2,
        depth_mm=0.6,
        measured_force_N=351.5,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.4,
        depth_mm=0.2,
        measured_force_N=361.3,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.4,
        depth_mm=0.4,
        measured_force_N=348.7,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.4,
        depth_mm=0.6,
        measured_force_N=356.9,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.6,
        depth_mm=0.2,
        measured_force_N=363.8,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.6,
        depth_mm=0.4,
        measured_force_N=364.7,
    ),

    Experiment(
        speed_m_min=80,
        feed_mm_rev=0.6,
        depth_mm=0.6,
        measured_force_N=375.8,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.2,
        depth_mm=0.2,
        measured_force_N=417.9,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.2,
        depth_mm=0.4,
        measured_force_N=483.8,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.2,
        depth_mm=0.6,
        measured_force_N=474.5,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.4,
        depth_mm=0.2,
        measured_force_N=463.2,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.4,
        depth_mm=0.4,
        measured_force_N=428.3,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.4,
        depth_mm=0.6,
        measured_force_N=433.8,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.6,
        depth_mm=0.2,
        measured_force_N=441.2,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.6,
        depth_mm=0.4,
        measured_force_N=427.6,
    ),

    Experiment(
        speed_m_min=160,
        feed_mm_rev=0.6,
        depth_mm=0.6,
        measured_force_N=441.2,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.2,
        depth_mm=0.2,
        measured_force_N=623.7,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.2,
        depth_mm=0.4,
        measured_force_N=627.1,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.2,
        depth_mm=0.6,
        measured_force_N=627.8,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.4,
        depth_mm=0.2,
        measured_force_N=624.1,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.4,
        depth_mm=0.4,
        measured_force_N=623.0,
    ),

    Experiment(
        speed_m_min=240,
        feed_mm_rev=0.4,
        depth_mm=0.6,
        measured_force_N=595.6,
    ),
]


# ============================================================
# PREDICTION
# ============================================================

def predict_experiments(
    model,
    experiments,
):

    predicted = []

    measured = []

    errors_percent = []

    for experiment in experiments:

        prediction = (
            model.turning_force(
                experiment.depth_mm,
                experiment.feed_mm_rev,
            )
        )

        measured_force = (
            experiment.measured_force_N
        )

        error = (
            prediction
            - measured_force
        )

        error_percent = (
            100.0
            * error
            / measured_force
        )

        predicted.append(
            prediction
        )

        measured.append(
            measured_force
        )

        errors_percent.append(
            error_percent
        )

    return (
        np.array(predicted),
        np.array(measured),
        np.array(errors_percent),
    )


# ============================================================
# METRICS
# ============================================================

def validation_metrics(
    measured,
    predicted,
):

    error = (
        predicted
        - measured
    )

    absolute_error = np.abs(
        error
    )

    percentage_error = (
        100.0
        * absolute_error
        / np.maximum(
            np.abs(measured),
            1e-12,
        )
    )

    mae = np.mean(
        absolute_error
    )

    mape = np.mean(
        percentage_error
    )

    rmse = np.sqrt(
        np.mean(
            error**2
        )
    )

    ss_res = np.sum(
        error**2
    )

    ss_tot = np.sum(
        (
            measured
            - np.mean(measured)
        )**2
    )

    r2 = (
        1.0
        - ss_res / ss_tot
    )

    return {
        "MAE_N": mae,
        "MAPE_percent": mape,
        "RMSE_N": rmse,
        "R2": r2,
        "max_error_percent":
            np.max(
                percentage_error
            ),
    }


# ============================================================
# SIMPLE PARAMETER FIT
# ============================================================

def fit_kienzle(
    experiments,
):

    """
    Fit:

        Fc = b * kc1_1 * h^(1-mc)

    Taking logarithms:

        ln(Fc/b)
            =
        ln(kc1_1)
            +
        (1-mc) ln(h)

    Let:

        y = ln(Fc/b)
        x = ln(h)

    Then:

        y = A + Bx

    where:

        kc1_1 = exp(A)
        mc = 1-B

    IMPORTANT:

    This simple fit ignores cutting-speed dependence.

    It is therefore a calibration demonstration, not a final
    production model.
    """

    h = np.array(
        [
            e.feed_mm_rev
            for e in experiments
        ]
    )

    b = np.array(
        [
            e.depth_mm
            for e in experiments
        ]
    )

    force = np.array(
        [
            e.measured_force_N
            for e in experiments
        ]
    )

    x = np.log(
        h
    )

    y = np.log(
        force / b
    )

    B, A = np.polyfit(
        x,
        y,
        1,
    )

    kc1_1 = math.exp(
        A
    )

    mc = 1.0 - B

    return KienzleParameters(
        kc1_1=kc1_1,
        mc=mc,
        name="Fitted from benchmark",
    )


# ============================================================
# REPORT
# ============================================================

def print_report(
    parameters,
    metrics,
):

    print()
    print("=" * 70)
    print("032+03 — KIENZLE VALIDATION")
    print("=" * 70)

    print()
    print("KIENZLE PARAMETERS")
    print("-" * 70)

    print(
        f"kc1_1:          "
        f"{parameters.kc1_1:.3f} N/mm²"
    )

    print(
        f"mc:             "
        f"{parameters.mc:.5f}"
    )

    print(
        f"source:         "
        f"{parameters.name}"
    )

    print()
    print("VALIDATION METRICS")
    print("-" * 70)

    print(
        f"MAE:            "
        f"{metrics['MAE_N']:.3f} N"
    )

    print(
        f"MAPE:           "
        f"{metrics['MAPE_percent']:.3f} %"
    )

    print(
        f"RMSE:           "
        f"{metrics['RMSE_N']:.3f} N"
    )

    print(
        f"R²:             "
        f"{metrics['R2']:.5f}"
    )

    print(
        f"Maximum error:  "
        f"{metrics['max_error_percent']:.3f} %"
    )


# ============================================================
# PLOTS
# ============================================================

def plot_validation(
    measured,
    predicted,
):

    minimum = min(
        measured.min(),
        predicted.min(),
    )

    maximum = max(
        measured.max(),
        predicted.max(),
    )

    plt.figure(
        figsize=(7, 7)
    )

    plt.scatter(
        measured,
        predicted,
        color="royalblue",
        s=45,
        label="Model",
    )

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
        "k--",
        label="Perfect prediction",
    )

    plt.xlabel(
        "Measured force [N]"
    )

    plt.ylabel(
        "Predicted force [N]"
    )

    plt.title(
        "Kienzle model validation"
    )

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


# ============================================================
# ERROR PLOT
# ============================================================

def plot_error(
    measured,
    predicted,
):

    error_percent = (
        100.0
        * (
            predicted
            - measured
        )
        / measured
    )

    plt.figure(
        figsize=(9, 5)
    )

    plt.axhline(
        0,
        color="black",
        linewidth=1,
    )

    plt.scatter(
        np.arange(
            len(error_percent)
        ),
        error_percent,
        color="darkred",
    )

    plt.xlabel(
        "Experiment"
    )

    plt.ylabel(
        "Prediction error [%]"
    )

    plt.title(
        "Kienzle prediction error"
    )

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# PARAMETER STUDY
# ============================================================

def parameter_study(
    model,
):

    feeds = np.linspace(
        0.05,
        0.8,
        100,
    )

    depth = 0.5

    forces = np.array(
        [
            model.turning_force(
                depth,
                f,
            )
            for f in feeds
        ]
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        feeds,
        forces,
        linewidth=2,
    )

    plt.xlabel(
        "Feed [mm/rev]"
    )

    plt.ylabel(
        "Cutting force [N]"
    )

    plt.title(
        "Kienzle force vs feed"
    )

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("032+03 — KIENZLE CUTTING FORCE")
    print("=" * 70)

    # --------------------------------------------------------
    # Fit coefficients from benchmark data
    # --------------------------------------------------------

    fitted = fit_kienzle(
        EXPERIMENTS
    )

    print()
    print(
        "Fitted coefficients from benchmark dataset:"
    )

    print(
        f"kc1_1 = "
        f"{fitted.kc1_1:.3f} N/mm²"
    )

    print(
        f"mc = "
        f"{fitted.mc:.5f}"
    )

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = KienzleModel(
        fitted
    )

    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    predicted, measured, errors = (
        predict_experiments(
            model,
            EXPERIMENTS,
        )
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    metrics = validation_metrics(
        measured,
        predicted,
    )

    print_report(
        fitted,
        metrics,
    )

    # --------------------------------------------------------
    # Show individual results
    # --------------------------------------------------------

    print()
    print("EXPERIMENT-BY-EXPERIMENT")
    print("-" * 70)

    print(
        "No. | Vc | f | ap | "
        "Measured | Predicted | Error"
    )

    print(
        "    | m/min | mm/rev | mm | "
        "N | N | %"
    )

    print("-" * 70)

    for i, experiment in enumerate(
        EXPERIMENTS
    ):

        print(
            f"{i+1:3d} | "
            f"{experiment.speed_m_min:3.0f} | "
            f"{experiment.feed_mm_rev:.2f} | "
            f"{experiment.depth_mm:.2f} | "
            f"{measured[i]:8.2f} | "
            f"{predicted[i]:9.2f} | "
            f"{errors[i]:7.2f}"
        )

    # --------------------------------------------------------
    # Example actual machining calculation
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("EXAMPLE")
    print("=" * 70)

    example = calculate_cut(
        model=model,
        diameter_mm=20.0,
        depth_of_cut_mm=2.0,
        feed_mm_rev=0.10,
        cutting_speed_m_min=20.0,
    )

    print(
        f"Diameter:       20.0 mm"
    )

    print(
        f"Depth:           2.0 mm"
    )

    print(
        f"Feed:            0.10 mm/rev"
    )

    print(
        f"Speed:           20.0 m/min"
    )

    print(
        f"RPM:             "
        f"{example['rpm']:.2f}"
    )

    print(
        f"Cutting force:   "
        f"{example['force_N']:.2f} N"
    )

    print(
        f"Torque:          "
        f"{example['torque_Nm']:.3f} N*m"
    )

    print(
        f"Power:           "
        f"{example['power_W']:.2f} W"
    )

    # --------------------------------------------------------
    # Plots
    # --------------------------------------------------------

    plot_validation(
        measured,
        predicted,
    )

    plot_error(
        measured,
        predicted,
    )

    parameter_study(
        model
    )

    print()
    print("=" * 70)
    print("032+03 COMPLETE")
    print("=" * 70)

    print(
        """
IMPORTANT:

This benchmark fit is NOT yet a validated model for your
specific HSS tool and AISI 1040 stock.

For real validation:

    1. measure cutting force;
    2. record Vc, f, ap;
    3. measure tool geometry;
    4. collect several experiments;
    5. fit kc1_1 and mc;
    6. hold some experiments out;
    7. predict the held-out experiments;
    8. calculate MAPE/RMSE/R².

Then the model becomes experimentally validated.

NEXT:

    geometry
        ↓
    actual engagement
        ↓
    local chip thickness
        ↓
    local Kienzle force
        ↓
    force vector
        ↓
    PyBullet / dynamics
    """
    )


if __name__ == "__main__":
    main()
