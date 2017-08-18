bl_info = {
    "name": "Some Helpers",
    "category": "Object",
}

import bpy
from mathutils import Vector

class CursorToSelected(bpy.types.Operator):
    bl_idname = "view3d.cursor_to_selecteds"
    bl_label = "cursor to selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
                bpy.ops.view3d.snap_cursor_to_selected(ctx)
                break
        return {"FINISHED"}

    
    
    
class SetOriginToSelected(bpy.types.Operator):
    bl_idname = "view3d.set_origin_to_selected"
    bl_label = "set origin to selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
    
        ori_cursor_location = bpy.context.scene.cursor_location
        print(ori_cursor_location)

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
                bpy.ops.view3d.snap_cursor_to_selected(ctx)
                break
                    
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.mode_set(mode='EDIT')

        print(bpy.context.scene.cursor_location)
        bpy.context.scene.cursor_location = ori_cursor_location
        
        return {"FINISHED"}



    
    
class MoveSelectedsToActive(bpy.types.Operator):
    bl_idname = "view3d.move_selecteds_to_active"
    bl_label = "move selecteds to active"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        if not bpy.context.scene.objects.active :
            return {"FINISHED"}

        for obj in bpy.context.selected_objects:
            if obj == bpy.context.scene.objects.active :
                continue
            
            obj.location = bpy.context.scene.objects.active.location
        
        return {"FINISHED"}


    
class MoveObjectToCursor(bpy.types.Operator):
    bl_idname = "view3d.move_object_to_cursor"
    bl_label = "move object to cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        context.scene.objects.active.location = context.scene.cursor_location
        return {"FINISHED"}


    
    
# store keymaps here to access after registration
addon_keymaps = []

def register():
    bpy.utils.register_class(CursorToSelected)
    bpy.utils.register_class(SetOriginToSelected)
    bpy.utils.register_class(MoveSelectedsToActive)
    bpy.utils.register_class(MoveObjectToCursor)
    
    # handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['3D View']
    if kc:
        addon_keymaps.append((km, km.keymap_items.new(CursorToSelected.bl_idname, 'Q', 'PRESS', ctrl=True)))
        addon_keymaps.append((km, km.keymap_items.new(SetOriginToSelected.bl_idname, 'Q', 'PRESS', alt=True)))
        addon_keymaps.append((km, km.keymap_items.new(MoveSelectedsToActive.bl_idname, 'W', 'PRESS', ctrl=True)))
        addon_keymaps.append((km, km.keymap_items.new(MoveObjectToCursor.bl_idname, 'W', 'PRESS', alt=True)))

def unregister():
    bpy.utils.unregister_class(CursorToSelected)
    bpy.utils.unregister_class(SetOriginToSelected)
    bpy.utils.unregister_class(MoveSelectedsToActive)
    bpy.utils.unregister_class(MoveObjectToCursor)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()