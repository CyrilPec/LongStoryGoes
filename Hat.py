import pybullet as p
import pybullet_data
import math

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)


def make_hat_mesh(
    brim_radius=1.2,
    brim_z=0.08,
    crown_radius=0.75,
    crown_height=1.0,
    segments=48,
    rings=8
):
    vertices = []
    faces = []

    # -------------------------
    # Brim
    # -------------------------
    # Bottom center
    vertices.append([0, 0, 0])

    # Bottom outer ring
    for i in range(segments):
        a = 2 * math.pi * i / segments
        vertices.append([
            brim_radius * math.cos(a),
            brim_radius * math.sin(a),
            0
        ])

    # Top outer ring
    top_outer = len(vertices)
    for i in range(segments):
        a = 2 * math.pi * i / segments
        vertices.append([
            brim_radius * math.cos(a),
            brim_radius * math.sin(a),
            brim_z
        ])

    # Brim bottom triangles
    for i in range(segments):
        j = (i + 1) % segments
        faces.append([0, 1 + j, 1 + i])

    # -------------------------
    # Crown
    # -------------------------
    # Crown starts at the inner radius
    base_start = len(vertices)

    for r in range(rings + 1):
        t = r / rings

        # Slightly rounded crown profile
        radius = crown_radius * (1.0 - 0.12 * t)
        z = brim_z + crown_height * t

        for i in range(segments):
            a = 2 * math.pi * i / segments
            vertices.append([
                radius * math.cos(a),
                radius * math.sin(a),
                z
            ])

    # Connect crown rings
    for r in range(rings):
        ring_a = base_start + r * segments
        ring_b = base_start + (r + 1) * segments

        for i in range(segments):
            j = (i + 1) % segments

            faces.append([
                ring_a + i,
                ring_a + j,
                ring_b + j
            ])

            faces.append([
                ring_a + i,
                ring_b + j,
                ring_b + i
            ])

    # Top cap
    top_center = len(vertices)
    vertices.append([0, 0, brim_z + crown_height])

    top_ring = base_start + rings * segments

    for i in range(segments):
        j = (i + 1) % segments
        faces.append([
            top_ring + i,
            top_ring + j,
            top_center
        ])

    return vertices, faces


vertices, faces = make_hat_mesh()

mesh_id = p.createCollisionShape(
    p.GEOM_MESH,
    vertices=vertices,
    indices=[v for face in faces for v in face]
)

visual_id = p.createVisualShape(
    p.GEOM_MESH,
    vertices=vertices,
    indices=[v for face in faces for v in face],
    rgbaColor=[0.08, 0.08, 0.1, 1]
)

hat = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=mesh_id,
    baseVisualShapeIndex=visual_id
)

# Ground
p.loadURDF("plane.urdf")

while True:
    p.stepSimulation()
