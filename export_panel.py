from bpy.types import (Panel)


class Export_Panel(Panel):
    bl_idname = "PANEL_PT_Export_Coords_Addon"
    bl_label = "Exportar Objetos"
    bl_category = "Exportar CSV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        export_panel = scene.export_panel

        row_directory = layout
        row_directory.label(text="Pasta de Destino")
        row_directory.prop(export_panel, "path")

        row = layout.split()
        row.operator('view3d.export_coord', text="Exportar para CSV")
