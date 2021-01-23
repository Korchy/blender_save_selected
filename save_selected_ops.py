# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
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

    def execute(self, context):
        SaveSelected.save_selected(
            context=context,
            scene_data=bpy.data,
            file_path=self.filepath,
            blender_path=bpy.app.binary_path
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)


def register():
    register_class(SAVE_SELECTED_OT_save)


def unregister():
    unregister_class(SAVE_SELECTED_OT_save)
