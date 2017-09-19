bl_info = {
    "name": "Export What You Want to STL",
    "category": "Object",
}

import bpy
import os

from bpy.props import BoolProperty, StringProperty

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Export What You Want to STL"
    bl_idname = "export_what_you_want_to_stl"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        
        row = layout.row()
        row.prop(obj, "is_export_to_stl", text="导出为独立的STL文件")
        
        row = layout.row()
        row.prop(obj, "stl_filename", text="STL文件名")
        layout.label(text="(不需要扩展名；如果为空，则使用物体名)")



class ExportSelectionToStl(bpy.types.Operator):
    bl_idname = "view3d.export_selection_to_stl"
    bl_label = "export selection to stl"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        if not bpy.data.is_saved:
            print("current blend file not save yet.")
            return {"FINISHED"}
        
        dirpath = bpy.path.abspath("//"+bpy.path.display_name_from_filepath(bpy.data.filepath)+"-stl/")
        
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
            
        original_selected = []
        for obj in bpy.context.scene.objects:
            if obj.select :
                original_selected.append(obj)
            
        
        # deselect all objects
        bpy.ops.object.select_all(action='DESELECT')    

        for obj in bpy.context.scene.objects:
            if obj.type!="MESH" :
                continue
        
            if not hasattr(obj, "is_export_to_stl"):
                break
            
            obj.select = True
        
        bpy.ops.export_mesh.stl(filepath=dirpath, use_selection=True, batch_mode="OBJECT")
            
            
        bpy.ops.object.select_all(action='DESELECT') 
        for obj in original_selected:  
            obj.select = True
        
        return {"FINISHED"}


class UIExporter(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Export What You Want to STL"
    bl_idname = "UIExporter"
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.prop(obj, "is_export_to_stl", text="导出为独立的STL文件")


def register():
    print("register(Export What You Want to STL)")
    bpy.types.Object.is_export_to_stl = BoolProperty()
    bpy.types.Object.stl_filename = StringProperty()

    bpy.utils.register_class(ExportSelectionToStl)
    bpy.utils.register_class(UIExporter)



def unregister():
    bpy.utils.unregister_class(ExportSelectionToStl)
    bpy.utils.unregister_class(UIExporter)


if __name__ == "__main__":
    register()
