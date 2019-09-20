import bpy
from pathlib import Path

bl_info = {
    "name": "HeroForge model import",
    "author": "RED_EYE",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "File > Import-Export > HeroForge model (.ckb)",
    "description": "Addon allows to import HeroForge models",
    "category": "Import-Export"
}

from bpy.props import StringProperty, BoolProperty, CollectionProperty


class HeroForge_OT_operator(bpy.types.Operator):
    """Load HeroForge ckb models"""
    bl_idname = "import_mesh.ckb"
    bl_label = "Import HeroForge model"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    filter_glob = StringProperty(default="*.ckb", options={'HIDDEN'})

    def execute(self, context):
        from . import bl_loader
        directory = Path(self.filepath).parent.absolute()
        for file in self.files:
            importer = bl_loader.HeroIO(str(directory / file.name))

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(HeroForge_OT_operator.bl_idname, text="HeroForge model (.ckb)")

def make_annotations(cls):
    """Converts class fields to annotations if running with Blender 2.8"""
    if bpy.app.version < (2, 80):
        return cls
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls

classes = (
    HeroForge_OT_operator,
)

def register():
    for cls in classes:
        make_annotations(cls)
        bpy.utils.register_class(cls)

    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_file_import.append(menu_import)
    else:
        bpy.types.TOPBAR_MT_file_import.append(menu_import)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if bpy.app.version < (2, 80, 0):
        bpy.types.INFO_MT_file_import.remove(menu_import)
    else:
        bpy.types.TOPBAR_MT_file_import.remove(menu_import)

if __name__ == "__main__":
    register()
