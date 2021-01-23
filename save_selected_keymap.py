# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

import bpy


class SAVE_SELECTED_KeyMap:

    _keymaps = []

    @classmethod
    def register(cls, context):
        # add new key map
        if context.window_manager.keyconfigs.addon:
            keymap = context.window_manager.keyconfigs.addon.keymaps.new(name='Window')
            # add keys
            keymap_item = keymap.keymap_items.new('save_selected.save', 'S', 'PRESS', ctrl=True, alt=True)
            cls._keymaps.append((keymap, keymap_item))

    @classmethod
    def unregister(cls):
        for keymap, keymap_item in cls._keymaps:
            keymap.keymap_items.remove(keymap_item)
        cls._keymaps.clear()


def register():
    SAVE_SELECTED_KeyMap.register(context=bpy.context)


def unregister():
    SAVE_SELECTED_KeyMap.unregister()
