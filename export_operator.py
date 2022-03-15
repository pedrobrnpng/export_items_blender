import bpy
from bpy.types import (Operator)

# Classe objeto:
# @name: nome do componente
# @x: valor do comprimento
# @y: valor da altura
# @z: valor da espessura
# @freq: quantidade de vezes


class Object:

    def __init__(self, name, x, y, z, freq):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.freq = freq


class Export_Operator(Operator):
    bl_idname = "view3d.export_coord"
    bl_label = "x"
    bl_description = "export selected objects "

    def execute(self, context):

        path = context.scene.export_panel.path

        if not path:
            self.report(
                {'INFO'}, "Selecione um ficheiro de destino."
            )
            return {'FINISHED'}

        objects = bpy.context.selected_objects

        # check selection
        if not objects:
            self.report(
                {'INFO'}, "Nenhum objeto selecionado. Selecione pelo menos um objeto"
            )
            return {'FINISHED'}

        # filter the meshes
        filteredObjects = list(
            filter(lambda obj: obj.type == "MESH", objects))

        # separates the linked objects and applies the scale.
        # if there is any multi user object, it throws an error, and while
        # catching it, the object is transformed to single user
        for obj in filteredObjects:
            try:
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.transform_apply(
                    location=False, rotation=False, scale=True)
            except:
                print("Objeto Multi-User detetado. A converter para Single-User.")
            finally:
                bpy.ops.object.make_single_user(
                    object=True, obdata=True, material=False, animation=False, obdata_animation=False)
                bpy.ops.mesh.separate(type='LOOSE')
                bpy.ops.object.transform_apply(
                    location=False, rotation=False, scale=True)

        objects = bpy.context.selected_objects
        filteredObjects = list(
            filter(lambda obj: obj.type == "MESH", objects))

        copyArray = list(filteredObjects)

        groupedObjects = []

        for obj in filteredObjects:
            dim = obj.dimensions
            freq = 1
            name = obj.name.split('.')
            for copyObj in copyArray:
                if copyObj != obj:
                    cDim = copyObj.dimensions
                    nameCopy = copyObj.name.split('.')

                    if name[0] == nameCopy[0] and round(dim.x, 4) == round(cDim.x, 4) and round(dim.y, 4) == round(cDim.y, 4) and round(dim.z, 4) == round(cDim.z, 4):
                        freq = freq + 1
                        filteredObjects.remove(copyObj)

            dimensions = [dim.x, dim.y, dim.z]
            dimensions.sort()

            newObj = Object(name[0], dimensions[2],
                            dimensions[1], dimensions[0], freq)
            groupedObjects.append(newObj)

        f = open(path, 'w+')

        f.write('NOME_COMPONENTE; QUANTIDADE; COMPRIMENTO; ALTURA; ESPESSURA\n')

        for obj in groupedObjects:
            f.write(
                obj.name+' ; '+'{:n} ; {:.3f} ; {:.3f} ; {:.3f}\n'.format(obj.freq, obj.x*1000, obj.y*1000, obj.z*1000))

        f.close()

        self.report({'INFO'}, "A informação foi exportada com successo")

        return {'FINISHED'}
