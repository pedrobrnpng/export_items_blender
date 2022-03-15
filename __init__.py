import bpy
from bpy.props import (PointerProperty)

from .export_operator import Export_Operator
from .export_panel import Export_Panel
from .input_types import InputSettings


bl_info = {
    "name": "Exportar para CSV",
    "author": "Pedro Brandao",
    "description": "Exporta os objetos criados, junto com as suas respetivas dimensões e frequência, para um ficheiro do tipo .csv",
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "View3D",
    "warning": "",
    "category": "Object"
}

classes = (Export_Operator, Export_Panel, InputSettings)

register, unregister = bpy.utils.register_classes_factory(classes)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.export_panel = PointerProperty(type=InputSettings)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.export_panel


if __name__ == "__main__":
    register()
