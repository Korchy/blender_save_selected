# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .save_selected import SaveSelected


class SAVE_SELECTED_OT_save(Operator, ExportHelper):
    bl_idname = 'save_selected.save'
    bl_label = 'Save Selected'
    bl_description = 'Save only selected objects from the current scene'
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.blend'

    filter_glob: StringProperty(
        default='*.blend',
        options={'HIDDEN'}
    )

    cleanup_startup_file: BoolProperty(
        name='Cleanup startup file',
        default=True
    )

    to_world_origin: BoolProperty(
        name='Move to world origin',
        default=False
    )

    def execute(self, context):
        SaveSelected.save_selected(
            context=context,
            file_path=self.filepath,
            blender_path=bpy.app.binary_path,
            to_world_origin=self.to_world_origin,
            cleanup_startup_file=self.cleanup_startup_file
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)


def register():
    register_class(SAVE_SELECTED_OT_save)


def unregister():
    unregister_class(SAVE_SELECTED_OT_save)
