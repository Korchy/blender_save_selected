# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

from bpy.types import TOPBAR_MT_file_export


# -- MENU ---

def menu_save_selected(self, context):
    # draw operator for menu
    self.layout.operator('save_selected.save', text='Save selected (.blend)', icon='FILE_TICK')


def register():
    # add to "File - Export" menu
    TOPBAR_MT_file_export.prepend(menu_save_selected)


def unregister():
    # remove from menu
    TOPBAR_MT_file_export.remove(menu_save_selected)
