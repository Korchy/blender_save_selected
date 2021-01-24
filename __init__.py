# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

from . import save_selected_ops
from . import save_selected_ui
from . import save_selected_keymap
from .addon import Addon


bl_info = {
    'name': 'Save Selected',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 91, 0),
    'location': 'Main menu: File – Export – Save Selected',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-save-selected/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-save-selected/',
    'description': 'Save only selected objects from the current file'
}


def register():
    if not Addon.dev_mode():
        save_selected_ops.register()
        save_selected_ui.register()
        save_selected_keymap.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        save_selected_keymap.unregister()
        save_selected_ui.unregister()
        save_selected_ops.unregister()


if __name__ == '__main__':
    register()
