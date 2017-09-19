bl_info = {
    "name": "Some Helpers",
    "category": "Object",
}

import bpy
from mathutils import Vector





class CreateCenterPotinOfSelecteds(bpy.types.Operator):
    bl_idname = "view3d.create_center_potin_of_selecteds"
    bl_label = "Create Center Potin of Selecteds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.duplicate_move()
        bpy.ops.mesh.merge(type="CENTER")
        return {"FINISHED"}


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



class DifferenceOfObjects(bpy.types.Operator):
    bl_idname = "view3d.difference_of_objects"
    bl_label = "Difference of Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ori_active = context.object
        ori_seleted = bpy.context.selected_objects.copy()

        bpy.context.scene.objects.active = None
        for obj in ori_seleted :
            obj.select = False

        print("active obj", ori_active)
        print("seleteds obj", ori_seleted)

        print("context.object =", context.object)
        print("bpy.context.selected_objects =", bpy.context.selected_objects)

        for obj in ori_seleted :
            if obj == ori_active :
                print("--", obj)
                continue

            print("..", obj)

            bpy.context.scene.objects.active = obj

            bpy.ops.object.modifier_add(type="BOOLEAN")

            modifier = context.object.modifiers.values().pop()
            modifier.operation = "DIFFERENCE"
            print(context.object, "-", ori_active)
            modifier.object = ori_active

            obj.select = False

        for obj in ori_seleted:
            obj.select = True
        ori_active.select = True

        return {"FINISHED"}



class SetOriginToSelected(bpy.types.Operator):
    bl_idname = "view3d.set_origin_to_selected"
    bl_label = "set origin to selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        print("SetOriginToSelected")

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
            print("there are no active objects")
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

class UIHelper(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Helper"
    bl_idname = "UIHelper"
    bl_region_type = 'TOOLS'
    bl_space_type = 'VIEW_3D'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.row()
        layout.operator(DifferenceOfObjects.bl_idname, text="布尔差集:选中-活动")
        layout.row()
        layout.operator(CreateCenterPotinOfSelecteds.bl_idname, text="创建中点")
        layout.row()
        layout.operator(MoveSelectedsToActive.bl_idname, text="移动:选中>活动")
        layout.operator(MoveObjectToCursor.bl_idname, text="移动:活动>游标")
        layout.operator(CursorToSelected.bl_idname, text="移动:游游标>选中中点")
        layout.operator(SetOriginToSelected.bl_idname, text="设置:原点>选中中点")
    
    
# store keymaps here to access after registration
addon_keymaps = []

def register():
    print("register(Helper 1)")
    bpy.utils.register_class(CursorToSelected)
    bpy.utils.register_class(SetOriginToSelected)
    bpy.utils.register_class(MoveSelectedsToActive)
    bpy.utils.register_class(MoveObjectToCursor)
    bpy.utils.register_class(CreateCenterPotinOfSelecteds)
    bpy.utils.register_class(DifferenceOfObjects)
    bpy.utils.register_class(UIHelper)

    # handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc.keymaps.get("3D View")==None :
        km = kc.keymaps.new('3D View')
    else :
        km = kc.keymaps['3D View']
    if kc:
        addon_keymaps.append((km, km.keymap_items.new(CursorToSelected.bl_idname, 'Q', 'PRESS', ctrl=True)))
        addon_keymaps.append((km, km.keymap_items.new(SetOriginToSelected.bl_idname, 'Q', 'PRESS', alt=True)))
        addon_keymaps.append((km, km.keymap_items.new(MoveSelectedsToActive.bl_idname, 'W', 'PRESS', ctrl=True)))
        addon_keymaps.append((km, km.keymap_items.new(MoveObjectToCursor.bl_idname, 'W', 'PRESS', alt=True)))

def unregister():
    print("unregister()")
    bpy.utils.unregister_class(CursorToSelected)
    bpy.utils.unregister_class(SetOriginToSelected)
    bpy.utils.unregister_class(MoveSelectedsToActive)
    bpy.utils.unregister_class(MoveObjectToCursor)
    bpy.utils.unregister_class(CreateCenterPotinOfSelecteds)
    bpy.utils.unregister_class(DifferenceOfObjects)
    bpy.utils.unregister_class(UIHelper)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()