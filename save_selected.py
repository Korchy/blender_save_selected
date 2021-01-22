# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

import tempfile
import os


class SaveSelected:

    @classmethod
    def save_selected(cls, context, scene_data, file_path):
        # save selected objects

        text_block = scene_data.texts.new(name='save_selected')
        text_block_txt = \
            '''import bpy
            for obj in bpy.data.objects:
                bpy.context.scene.collection.objects.link(obj)
            bpy.ops.wm.save_as_mainfile(filepath="''' + file_path + '''")
        '''
        text_block.from_string(text_block_txt)
        text_block.name = 'save_selected'

        temp_file_path = os.path.join(tempfile.gettempdir(), 'save_selection_tmp.blend')
        data_blocks = set(bpy.context.selected_objects).union({text_block})
        bpy.data.libraries.write(temp_file_path, data_blocks)

        blender_path = bpy.app.binary_path

        import subprocess
        subprocess.call([blender_path, "-b", temp_file_path, "--python-text", "save_selected"])
