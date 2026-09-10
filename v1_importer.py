"""
LongStoryGoes - Blender V1 Importer
===================================

Reads a LongStoryGoes story-node Python file and creates a Blender scene.

Architecture:

    Story .py
        |
        v
    World objects
        |
        +--> Asset exists -> load asset
        |
        +--> No asset -> create primitive
        |
        +--> No geometry -> create placeholder
        |
        v
    Blender scene

Important:
- Story files do NOT contain bpy.
- Python world data remains authoritative.
- Blender is only the visual representation.
"""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any

import bpy
from mathutils import Vector


# ---------------------------------------------------------------------------
# Add-on information
# ---------------------------------------------------------------------------

VERSION = (1, 0, 0)
NAME = "LongStoryGoes V1 Importer"


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def log(message: str) -> None:
    """Print importer messages to the Blender console."""
    print(f"[LongStoryGoes] {message}")


def get_object_id(world_object: Any) -> str:
    """Return the stable world ID."""
    return str(getattr(world_object, "id", "unknown_object"))


def get_object_type(world_object: Any) -> str:
    """Return the world object type."""
    return str(getattr(world_object, "type", "object"))


def get_object_name(world_object: Any) -> str:
    """Return a readable object name."""
    object_id = get_object_id(world_object)
    name = getattr(world_object, "name", None)

    if name:
        return str(name)

    return object_id


# ---------------------------------------------------------------------------
# Asset handling
# ---------------------------------------------------------------------------

def find_asset(
    world_object: Any,
    story_file: Path,
) -> Path | None:
    """
    Find an asset specified by the world object.

    Supported fields:

        asset="assets/swing.blend"

    or, if later added:

        model="swing.blend"

    Asset paths are first interpreted relative to the story file.
    """

    asset = getattr(world_object, "asset", None)

    if not asset:
        asset = getattr(world_object, "model", None)

    if not asset:
        return None

    asset_path = Path(str(asset))

    if not asset_path.is_absolute():
        asset_path = story_file.parent / asset_path

    asset_path = asset_path.resolve()

    if asset_path.exists():
        return asset_path

    log(f"Asset not found: {asset_path}")

    return None


def import_blend_asset(
    asset_path: Path,
    object_id: str,
) -> list[bpy.types.Object]:
    """
    Import objects from a .blend asset.

    V1 uses Blender's library append mechanism.

    The asset is expected to contain one or more objects.
    """

    imported_objects: list[bpy.types.Object] = []

    with bpy.data.libraries.load(
        str(asset_path),
        link=False,
    ) as (data_from, data_to):

        data_to.objects = list(data_from.objects)

    for obj in data_to.objects:
        if obj is None:
            continue

        bpy.context.collection.objects.link(obj)
        imported_objects.append(obj)

    log(
        f"Imported asset '{asset_path.name}' "
        f"for world object '{object_id}'"
    )

    return imported_objects


# ---------------------------------------------------------------------------
# Primitive generation
# ---------------------------------------------------------------------------

def create_sphere(
    name: str,
    radius: float,
) -> bpy.types.Object:

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=float(radius),
        location=(0.0, 0.0, 0.0),
    )

    obj = bpy.context.object
    obj.name = name

    return obj


def create_box(
    name: str,
    size: tuple[float, float, float],
) -> bpy.types.Object:

    bpy.ops.mesh.primitive_cube_add(
        location=(0.0, 0.0, 0.0),
    )

    obj = bpy.context.object
    obj.name = name

    obj.scale = (
        float(size[0]) / 2.0,
        float(size[1]) / 2.0,
        float(size[2]) / 2.0,
    )

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True,
    )

    return obj


def create_cylinder(
    name: str,
    radius: float,
    depth: float,
) -> bpy.types.Object:

    bpy.ops.mesh.primitive_cylinder_add(
        radius=float(radius),
        depth=float(depth),
        location=(0.0, 0.0, 0.0),
    )

    obj = bpy.context.object
    obj.name = name

    return obj


def create_plane(
    name: str,
    size: tuple[float, float],
) -> bpy.types.Object:

    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        location=(0.0, 0.0, 0.0),
    )

    obj = bpy.context.object
    obj.name = name

    obj.scale = (
        float(size[0]),
        float(size[1]),
        1.0,
    )

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True,
    )

    return obj


def create_placeholder(
    name: str,
    object_type: str,
) -> bpy.types.Object:
    """
    Generic fallback for an object for which V1 has no geometry.
    """

    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0.0, 0.0, 0.5),
    )

    obj = bpy.context.object
    obj.name = name

    log(
        f"No geometry for '{name}' "
        f"(type={object_type}); using cube placeholder."
    )

    return obj


# ---------------------------------------------------------------------------
# Geometry resolver
# ---------------------------------------------------------------------------

def create_from_geometry(
    world_object: Any,
) -> list[bpy.types.Object]:
    """
    Create Blender geometry from the object's geometry dictionary.

    V1 understands:

        sphere
        box
        cube
        cylinder
        plane

    The current 010.py uses:

        {"shape": "sphere", "radius": 0.12}

    so V1 also accepts the older 'shape' field.
    """

    geometry = getattr(
        world_object,
        "geometry",
        {},
    ) or {}

    object_id = get_object_id(world_object)
    object_name = get_object_name(world_object)
    object_type = get_object_type(world_object)

    primitive = geometry.get("primitive")

    if primitive is None:
        primitive = geometry.get("shape")

    primitive = str(primitive).lower() if primitive else ""

    # --------------------------------------------------------------
    # Sphere
    # --------------------------------------------------------------

    if primitive in {"sphere", "ball"}:

        radius = geometry.get("radius", 0.5)

        obj = create_sphere(
            object_name,
            radius,
        )

        return [obj]

    # --------------------------------------------------------------
    # Box / cube
    # --------------------------------------------------------------

    if primitive in {"box", "cube"}:

        size = geometry.get(
            "size",
            (1.0, 1.0, 1.0),
        )

        obj = create_box(
            object_name,
            (
                float(size[0]),
                float(size[1]),
                float(size[2]),
            ),
        )

        return [obj]

    # --------------------------------------------------------------
    # Cylinder
    # --------------------------------------------------------------

    if primitive == "cylinder":

        radius = geometry.get("radius", 0.5)
        depth = geometry.get("depth", 1.0)

        obj = create_cylinder(
            object_name,
            radius,
            depth,
        )

        return [obj]

    # --------------------------------------------------------------
    # Plane
    # --------------------------------------------------------------

    if primitive in {"plane", "ground"}:

        size = geometry.get(
            "size",
            (10.0, 10.0),
        )

        obj = create_plane(
            object_name,
            (
                float(size[0]),
                float(size[1]),
            ),
        )

        return [obj]

    # --------------------------------------------------------------
    # Simple V1 type-specific fallbacks
    # --------------------------------------------------------------

    if object_type == "location":

        ground = geometry.get("ground")

        if ground == "sand":

            obj = create_plane(
                object_name,
                (10.0, 10.0),
            )

            return [obj]

    if object_type == "swing":

        # V1 fallback swing:
        # two vertical posts + top bar + seat.
        return create_swing(object_name)

    if object_type == "character":

        return create_character_placeholder(object_name)

    return [
        create_placeholder(
            object_name,
            object_type,
        )
    ]


# ---------------------------------------------------------------------------
# Swing fallback
# ---------------------------------------------------------------------------

def create_swing(
    name: str,
) -> list[bpy.types.Object]:
    """
    Very simple procedural swing.

    This is intentionally primitive.

    Later:
        asset = "assets/swing.blend"

    can replace this automatically.
    """

    objects: list[bpy.types.Object] = []

    # Left post
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=2.2,
        location=(-0.7, 0.0, 1.1),
    )
    left = bpy.context.object
    left.name = f"{name}_left_post"
    objects.append(left)

    # Right post
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=2.2,
        location=(0.7, 0.0, 1.1),
    )
    right = bpy.context.object
    right.name = f"{name}_right_post"
    objects.append(right)

    # Top bar
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=1.4,
        location=(0.0, 0.0, 2.2),
        rotation=(0.0, 1.5708, 0.0),
    )
    top = bpy.context.object
    top.name = f"{name}_top_bar"
    objects.append(top)

    # Seat
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0.0, 0.0, 1.0),
    )
    seat = bpy.context.object
    seat.name = f"{name}_seat"
    seat.scale = (0.45, 0.18, 0.05)

    bpy.ops.object.transform_apply(
        location=False,
        rotation=False,
        scale=True,
    )

    objects.append(seat)

    # Suspension ropes
    for x in (-0.35, 0.35):

        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.015,
            depth=1.2,
            location=(x, 0.0, 1.6),
        )

        rope = bpy.context.object
        rope.name = f"{name}_rope"

        objects.append(rope)

    log(f"Created procedural swing '{name}'")

    return objects


# ---------------------------------------------------------------------------
# Character fallback
# ---------------------------------------------------------------------------

def create_character_placeholder(
    name: str,
) -> list[bpy.types.Object]:
    """
    Very simple character placeholder.

    A real character asset can later replace this.
    """

    objects: list[bpy.types.Object] = []

    # Body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.25,
        depth=1.0,
        location=(0.0, 0.0, 1.0),
    )

    body = bpy.context.object
    body.name = f"{name}_body"
    objects.append(body)

    # Head
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.28,
        location=(0.0, 0.0, 1.7),
    )

    head = bpy.context.object
    head.name = f"{name}_head"
    objects.append(head)

    log(f"Created character placeholder '{name}'")

    return objects


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

def apply_transform(
    objects: list[bpy.types.Object],
    world_object: Any,
) -> None:
    """
    Apply world transform.

    Expected:

        transform={
            "position": (x, y, z),
            "rotation": (rx, ry, rz),
            "scale": (sx, sy, sz),
        }
    """

    transform = getattr(
        world_object,
        "transform",
        {},
    ) or {}

    position = transform.get(
        "position",
        (0.0, 0.0, 0.0),
    )

    rotation = transform.get(
        "rotation",
        (0.0, 0.0, 0.0),
    )

    scale = transform.get(
        "scale",
        (1.0, 1.0, 1.0),
    )

    for obj in objects:

        obj.location = Vector(
            (
                float(position[0]),
                float(position[1]),
                float(position[2]),
            )
        )

        obj.rotation_euler = (
            float(rotation[0]),
            float(rotation[1]),
            float(rotation[2]),
        )

        obj.scale = (
            float(scale[0]),
            float(scale[1]),
            float(scale[2]),
        )


# ---------------------------------------------------------------------------
# World metadata
# ---------------------------------------------------------------------------

def store_world_data(
    obj: bpy.types.Object,
    world_object: Any,
) -> None:
    """
    Store the original world identity and data on the Blender object.

    This is important for future synchronization.
    """

    obj["longstory_id"] = get_object_id(world_object)
    obj["longstory_type"] = get_object_type(world_object)

    location = getattr(
        world_object,
        "location",
        None,
    )

    if location is not None:
        obj["longstory_location"] = str(location)

    state = getattr(
        world_object,
        "state",
        {},
    ) or {}

    for key, value in state.items():

        # Blender custom properties accept simple values.
        try:
            obj[f"state_{key}"] = value
        except Exception:
            obj[f"state_{key}"] = str(value)


# ---------------------------------------------------------------------------
# Scene cleanup
# ---------------------------------------------------------------------------

def clear_longstory_scene() -> None:
    """
    Remove only objects previously generated by LongStoryGoes.

    Existing user-created Blender objects are preserved.
    """

    objects_to_remove = [
        obj
        for obj in bpy.data.objects
        if "longstory_id" in obj
    ]

    for obj in objects_to_remove:
        bpy.data.objects.remove(
            obj,
            do_unlink=True,
        )

    log(
        f"Removed {len(objects_to_remove)} "
        f"previous LongStoryGoes objects."
    )


# ---------------------------------------------------------------------------
# Import one world object
# ---------------------------------------------------------------------------

def import_world_object(
    world_object: Any,
    story_file: Path,
) -> list[bpy.types.Object]:
    """
    Convert one WorldObject into Blender objects.

    Priority:

        1. Asset
        2. Primitive geometry
        3. Type-specific fallback
        4. Generic placeholder
    """

    object_id = get_object_id(world_object)
    object_name = get_object_name(world_object)

    log(
        f"Importing '{object_id}' "
        f"type={get_object_type(world_object)}"
    )

    # --------------------------------------------------------------
    # 1. Asset
    # --------------------------------------------------------------

    asset_path = find_asset(
        world_object,
        story_file,
    )

    if asset_path is not None:

        objects = import_blend_asset(
            asset_path,
            object_id,
        )

    else:

        # ----------------------------------------------------------
        # 2/3/4. Geometry / fallback
        # ----------------------------------------------------------

        objects = create_from_geometry(
            world_object,
        )

    # --------------------------------------------------------------
    # Apply transform
    # --------------------------------------------------------------

    apply_transform(
        objects,
        world_object,
    )

    # --------------------------------------------------------------
    # Store world identity/state
    # --------------------------------------------------------------

    for obj in objects:

        store_world_data(
            obj,
            world_object,
        )

    return objects


# ---------------------------------------------------------------------------
# Import story file
# ---------------------------------------------------------------------------

def import_story_file(
    filepath: str,
    clear_previous: bool = True,
) -> int:
    """
    Execute a LongStoryGoes Python story node and import its World.

    Example:

        import_story_file(
            "C:/LongStoryGoes/010.py"
        )
    """

    story_path = Path(filepath).resolve()

    if not story_path.exists():
        raise FileNotFoundError(
            f"Story file does not exist: {story_path}"
        )

    log(f"Reading story: {story_path}")

    if clear_previous:
        clear_longstory_scene()

    # --------------------------------------------------------------
    # Execute story node.
    #
    # 010.py creates:
    #
    #     world = World(...)
    #
    # and then populates:
    #
    #     world.objects
    # --------------------------------------------------------------

    namespace = runpy.run_path(
        str(story_path),
        run_name="__longstory_node__",
    )

    world = namespace.get("world")

    if world is None:
        raise RuntimeError(
            "Story file does not define a 'world' object."
        )

    objects = getattr(
        world,
        "objects",
        None,
    )

    if not isinstance(objects, dict):
        raise RuntimeError(
            "Story world does not contain "
            "a valid 'objects' dictionary."
        )

    imported_count = 0

    # --------------------------------------------------------------
    # Create Blender representation
    # --------------------------------------------------------------

    for world_object in objects.values():

        import_world_object(
            world_object,
            story_path,
        )

        imported_count += 1

    log(
        f"Import complete: "
        f"{imported_count} world objects."
    )

    return imported_count


# ---------------------------------------------------------------------------
# Blender operator
# ---------------------------------------------------------------------------

class LONGSTORY_OT_import_story(
    bpy.types.Operator,
):
    """Import a LongStoryGoes story node."""

    bl_idname = "longstory.import_story"
    bl_label = "Import LongStoryGoes Story"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="Story File",
        subtype="FILE_PATH",
    )

    clear_previous: bpy.props.BoolProperty(
        name="Clear Previous Import",
        description="Remove previous LongStoryGoes objects",
        default=True,
    )

    def execute(self, context):

        try:

            count = import_story_file(
                self.filepath,
                clear_previous=self.clear_previous,
            )

        except Exception as exc:

            self.report(
                {"ERROR"},
                str(exc),
            )

            log(f"ERROR: {exc}")

            return {"CANCELLED"}

        self.report(
            {"INFO"},
            f"Imported {count} world objects.",
        )

        return {"FINISHED"}

    def invoke(
        self,
        context,
        event,
    ):

        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

CLASSES = (
    LONGSTORY_OT_import_story,
)


def register() -> None:

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    log(f"{NAME} {VERSION} registered.")


def unregister() -> None:

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    log(f"{NAME} unregistered.")
