# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/blender_save_selected

import os
import subprocess
import tempfile
import bpy


class SaveSelected:

    _tmp_name = 'save_selection'

    @classmethod
    def save_selected(cls, context, file_path, blender_path, to_world_origin, cleanup_startup_file,
                      add_annotation_layer='NONE'):
        # save selected objects
        temp_dir = tempfile.gettempdir()
        # files path
        temp_py_path = os.path.join(temp_dir, cls._tmp_name + '.py').replace('\\', '/')
        temp_blend_path = os.path.join(temp_dir, cls._tmp_name + '.blend').replace('\\', '/')
        file_path = file_path.replace('\\', '/')
        # write selected objects to temporary library
        data_blocks = set(context.selected_objects)
        # if user used option to add annotation layer
        annotations_copy = None     # temporary copy of annotations
        if add_annotation_layer != 'NONE':
            if hasattr(context.scene, "annotation"):
                # >= 5.0
                annotations_copy = context.scene.annotation.copy()
            else:
                # < 5.0
                if 'Annotations' in context.blend_data.grease_pencils:
                    annotations_copy = context.blend_data.grease_pencils['Annotations'].copy()
            if add_annotation_layer != 'ALL':
                no_save_layers = (_layer for _layer in annotations_copy.layers if _layer.info != add_annotation_layer)
                for no_save_layer in no_save_layers:
                    annotations_copy.layers.remove(no_save_layer)
            data_blocks = set(context.selected_objects) | {annotations_copy, }
        # save data to temporary lib file
        context.blend_data.libraries.write(temp_blend_path, data_blocks)
        # cleanup temporary data
        if annotations_copy:
            if hasattr(context.scene, "annotation"):
                # >= 5.0
                context.blend_data.annotations.remove(annotations_copy)
            else:
                # < 5.0
                context.blend_data.grease_pencils.remove(annotations_copy)
        # make py script for import from temporary library, placing objects in the center of the scene
        # and saving to dest file
        text_block_content = 'import bpy' + '\n'
        if cleanup_startup_file:
            text_block_content += 'for obj in bpy.data.objects:' + '\n'
            text_block_content += '    bpy.data.objects.remove(obj)' + '\n'
        text_block_content += 'src_path="' + temp_blend_path + '"' + '\n'
        text_block_content += 'dest_path="' + file_path + '"' + '\n'
        text_block_content += 'with bpy.data.libraries.load(src_path) as (data_from, data_to):' + '\n'
        text_block_content += '    data_to.objects = data_from.objects' + '\n'
        text_block_content += '    data_to.annotations = data_from.annotations if hasattr(data_from, "annotations") else None' + '\n'
        text_block_content += '    data_to.grease_pencils = data_from.grease_pencils if hasattr(data_from, "grease_pencils") else None' + '\n'
        text_block_content += 'for obj in data_to.objects:' + '\n'
        text_block_content += '    bpy.context.scene.collection.objects.link(obj)' + '\n'
        text_block_content += 'bpy.ops.object.select_all(action="SELECT")' + '\n'
        # place imported object to the center of the scene
        if to_world_origin:
            text_block_content += 'bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)' + '\n'
            text_block_content += 'win = bpy.context.window' + '\n'
            text_block_content += 'scr = win.screen' + '\n'
            text_block_content += 'areas3d = [area for area in scr.areas if area.type == "VIEW_3D"]' + '\n'
            text_block_content += 'if bpy.app.version < (4, 0, 0):' + '\n'
            text_block_content += '    region = [region for region in areas3d[0].regions if region.type == "WINDOW"]' \
                                  + '\n'
            text_block_content += '    override = {"window": win,' + '\n'
            text_block_content += '        "screen":scr,' + '\n'
            text_block_content += '        "area":areas3d[0],' + '\n'
            text_block_content += '        "region":region,' + '\n'
            text_block_content += '        "scene" :bpy.context.scene,' + '\n'
            text_block_content += '    }' + '\n'
            text_block_content += '    bpy.ops.view3d.snap_selected_to_cursor(override, use_offset=True)' + '\n'
            text_block_content += 'else:' + '\n'
            text_block_content += '    with bpy.context.temp_override(area=areas3d[0]):' + '\n'
            text_block_content += '        bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)' + '\n'
        # annotations
        text_block_content += 'if data_to.annotations:' + '\n'
        text_block_content += '    bpy.context.scene.annotation = data_to.annotations[0]' + '\n'
        text_block_content += 'if data_to.grease_pencils:' + '\n'
        text_block_content += '    bpy.context.scene.grease_pencil = data_to.grease_pencils[0]' + '\n'
        # save to dest file
        text_block_content += 'bpy.ops.wm.save_as_mainfile(filepath=dest_path)' + '\n'
        # save script to temporary directory
        with open(file=temp_py_path, mode='w', encoding='utf8') as py_file:
            py_file.write(text_block_content)
        # execute script in subprocess
        subprocess.call([blender_path, '-b', '--python', temp_py_path])

    @staticmethod
    def annotation_layers_names_items(self_obj, context):
        # get annotations layers names
        if bpy.app.version < (4, 5, 0):
            return [
                ('NONE', 'NONE', 'NONE', '', 0)
            ]
        elif (4, 5, 0) <= bpy.app.version < (5, 0, 0):
            layer_names = [
                ('NONE', 'NONE', 'NONE', '', 0),
                ('ALL', 'ALL', 'ALL', '', 1),
            ]
            for i, layer in enumerate(context.blend_data.grease_pencils['Annotations'].layers):
                layer_names.append((layer.info, layer.info, layer.info, '', i + 2))
            return layer_names
        else:
            layer_names = [
                ('NONE', 'NONE', 'NONE', '', 0),
            ]
            if context.scene.annotation:
                layer_names.append(('ALL', 'ALL', 'ALL', '', 1))
                for i, layer in enumerate(context.scene.annotation.layers):
                    layer_names.append((layer.info, layer.info, layer.info, '', i + 2))
            return layer_names
