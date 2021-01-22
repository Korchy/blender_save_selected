# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class SAVE_SELECTED_PT_panel(Panel):
    bl_idname = 'SAVE_SELECTED_PT_panel'
    bl_label = 'Save Selected'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Save Selected'

    def draw(self, context):
        self.layout.operator('save_selected.save', icon='BLENDER')


def register():
    register_class(SAVE_SELECTED_PT_panel)


def unregister():
    unregister_class(SAVE_SELECTED_PT_panel)
