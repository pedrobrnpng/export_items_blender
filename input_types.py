from os import name
from bpy.props import (StringProperty, EnumProperty)
from bpy.types import (PropertyGroup)
import bpy


class InputSettings(PropertyGroup):

    path: StringProperty(
        name="Pasta de Destino",
        subtype="FILE_PATH",
        default="C:/Export/new.csv"
    )
