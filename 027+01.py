"""
027+01.py — Numerical Physical Layer

Small CPU-friendly numerical layer for experiment 027.

This file deliberately does not own World state.
It only performs numerical calculations.

NumPy arrays are used as the tensor representation.
A future version may optionally provide a PyTorch backend.
"""

from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np


def tensor(
    values: Iterable[float],
) -> np.ndarray:
    """
    Create a numerical tensor using NumPy.
    """

    return np.asarray(
        list(values),
        dtype=np.float64,
    )


def vector(
    x: float,
    y: float,
    z: float,
) -> np.ndarray:
    return tensor((x, y, z))


def magnitude(
    values: Iterable[float],
) -> float:
    value = tensor(values)
    return float(np.linalg.norm(value))


def distance(
    first: Iterable[float],
    second: Iterable[float],
) -> float:
    a = tensor(first)
    b = tensor(second)

    return float(np.linalg.norm(a - b))


def box_volume(
    length: float,
    width: float,
    height: float,
) -> float:
    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError(
            "All dimensions must be positive."
        )

    dimensions = tensor(
        (length, width, height)
    )

    return float(np.prod(dimensions))


def box_mass(
    length: float,
    width: float,
    height: float,
    density: float,
) -> float:
    if density <= 0:
        raise ValueError(
            "Density must be positive."
        )

    return (
        box_volume(
            length,
            width,
            height,
        )
        * density
    )


def kinetic_energy(
    mass: float,
    velocity: float,
) -> float:
    if mass <= 0:
        raise ValueError(
            "Mass must be positive."
        )

    return 0.5 * mass * velocity ** 2


def pressure(
    force: float,
    area: float,
) -> float:
    if area <= 0:
        raise ValueError(
            "Area must be positive."
        )

    return force / area


def estimate_joint_capacity(
    connection_strength: float,
    nail_count: int,
    plank_length: float,
) -> float:
    """
    Convert the World-approved connection strength into an
    experimental load capacity.

    This is intentionally conservative and simple.

    It is NOT presented as a real engineering formula.
    Its purpose is to give experiment 027 a measurable quantity
    that future experiments can challenge and improve.
    """

    if connection_strength < 0:
        raise ValueError(
            "Connection strength cannot be negative."
        )

    if nail_count < 0:
        raise ValueError(
            "Nail count cannot be negative."
        )

    if plank_length <= 0:
        raise ValueError(
            "Plank length must be positive."
        )

    if nail_count == 0:
        return 0.0

    geometry_factor = 1.0 / (
        1.0 + plank_length
    )

    strength = (
        connection_strength
        * geometry_factor
        * 0.001
    )

    return float(max(0.0, strength))


def normalize(
    values: Iterable[float],
) -> np.ndarray:
    value = tensor(values)
    norm = np.linalg.norm(value)

    if norm == 0:
        return np.zeros_like(value)

    return value / norm


def weighted_average(
    values: Iterable[float],
    weights: Iterable[float],
) -> float:
    values_array = tensor(values)
    weights_array = tensor(weights)

    if len(values_array) != len(weights_array):
        raise ValueError(
            "Values and weights must have equal length."
        )

    total_weight = float(
        np.sum(weights_array)
    )

    if total_weight <= 0:
        raise ValueError(
            "Total weight must be positive."
        )

    return float(
        np.sum(
            values_array * weights_array
        )
        / total_weight
    )


def self_test() -> None:
    assert abs(
        box_volume(2.0, 0.5, 0.5)
        - 0.5
    ) < 1e-9

    assert abs(
        box_mass(
            2.0,
            0.5,
            0.5,
            600.0,
        )
        - 300.0
    ) < 1e-9

    assert abs(
        kinetic_energy(
            2.0,
            3.0,
        )
        - 9.0
    ) < 1e-9

    assert abs(
        distance(
            (0.0, 0.0, 0.0),
            (3.0, 4.0, 0.0),
        )
        - 5.0
    ) < 1e-9

    print("027+01 self_test: OK")


if __name__ == "__main__":
    self_test()
