"""
LongStoryGoes Blender Add-on
============================

V1 add-on entry point.

IMPORTANT:
For normal Blender add-on installation this file should be named:

    __init__.py

The user-facing importer implementation is in:

    v1_importer.py
"""

from __future__ import annotations

import bpy

from . import v1_importer


bl_info = {
    "name": "LongStoryGoes V1 Importer",
    "author": "Cyril Pech",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > LongStoryGoes",
    "description": (
        "Import LongStoryGoes Python world nodes "
        "into Blender."
    ),
    "category": "Import-Export",
}


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class LONGSTORY_PT_main_panel(
    bpy.types.Panel,
):
    """Main LongStoryGoes panel."""

    bl_label = "LongStoryGoes"
    bl_idname = "LONGSTORY_PT_main_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "LongStoryGoes"

    def draw(
        self,
        context,
    ):

        layout = self.layout

        layout.label(
            text="World → Blender"
        )

        layout.separator()

        operator = layout.operator(
            v1_importer.LONGSTORY_OT_import_story.bl_idname,
            text="Import Story Node",
            icon="IMPORT",
        )

        operator.clear_previous = True


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

CLASSES = (
    LONGSTORY_PT_main_panel,
)


def register() -> None:

    v1_importer.register()

    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister() -> None:

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    v1_importer.unregister()


if __name__ == "__main__":
    register()
