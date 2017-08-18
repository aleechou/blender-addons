bl_info = {
    "name": "Some Tools",
    "category": "Object",
}

import bpy
from mathutils import Vector

class MakeCube(bpy.types.Operator):
    bl_idname = "mesh.make_cube"
    bl_label = "add cube"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        vertices = \
        [
            Vector((0, 0, 0)),
            Vector((10, 0, 0)),
            Vector((10, 10, 0)),
            Vector((0, 10, 0)),
            
            Vector((0, 0, 10)),
            Vector((10, 0, 10)),
            Vector((10, 10, 10)),
            Vector((0, 10, 10)),
        ]
        edges = []
        faces = [[3, 2, 1, 0], [0, 1, 5, 4], [1, 2, 6, 5], [4, 5, 6, 7], [3, 7, 6, 2], [0, 4, 7, 3]]
        
        cube = bpy.data.meshes.new("Clue2")
        cube.from_pydata(vertices, edges, faces)
        cube.update()
        object = bpy.data.objects.new("Cube2 ", cube)
        context.scene.objects.link(object)
        object.location = context.scene.cursor_location
        return {"FINISHED"}
    #end invoke
#end MakeCube

class MakeFace(bpy.types.Operator):
    bl_idname = "mesh.make_face"
    bl_label = "add face"
    bl_options = {'REGISTER', 'UNDO'}
    def invoke(self, context, event):
        vertices = \
        [
            Vector((0, 0, 0)),
            Vector((10, 0, 0)),
            Vector((10, 10, 0)),
            Vector((0, 10, 0)),
        ]
        edges = []
        faces = [[3, 2, 1, 0]]
        
        
        
        face = bpy.data.meshes.new("Face")
        face.from_pydata(vertices, edges, faces)
        face.update()
        object = bpy.data.objects.new("Face", face)
        context.scene.objects.link(object)
        object.location = context.scene.cursor_location
        return {"FINISHED"}
    #end invoke
#end MakeFace


def menu_func(self, context):
    self.layout.operator(MakeCube.bl_idname, icon='MESH_CUBE')
    self.layout.operator(MakeFace.bl_idname, icon='MESH_CUBE')

def register():
    bpy.utils.register_class(MakeCube)
    bpy.utils.register_class(MakeFace)
    bpy.types.INFO_MT_mesh_add.append(menu_func)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(MakeCube)
    bpy.utils.unregister_class(MakeFace)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
    
if __name__ == "__main__":
    register()