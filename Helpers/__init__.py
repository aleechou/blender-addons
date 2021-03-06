bl_info = {
    "name": "Some Helpers",
    "category": "Object",
}

import bpy
import bmesh
from mathutils import Vector
from bpy.props import FloatProperty, FloatVectorProperty, BoolProperty

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
    """布尔差集"""
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
    # bl_rna = "view3d.set_origin_to_selected[bl_rna]"

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


# 返回活动定点（选中历史中最后一个被选中的）
def activedVert(bm):
    for vert in reversed(bm.select_history):
        if isinstance(vert, bmesh.types.BMVert) and vert.select:
            return vert
    return None

class MovePointsSelectedsToActive(bpy.types.Operator):
    bl_idname = "view3d.move_selecteds_to_active"
    bl_label = "move selecteds to active"
    bl_options = {'REGISTER', 'UNDO'}
    
    xAxe = BoolProperty(default=False)
    yAxe = BoolProperty(default=False)
    zAxe = BoolProperty(default=False)

    def execute(self, context):
        
        bm = bmesh.from_edit_mesh(context.object.data)

        # 选中的活动顶点
        actived = activedVert(bm)
        if actived==None:
            print("there is no actived vert")
            return {"FINISHED"}

        for vert in bm.verts:
            if vert.select and vert!=actived :
                if self.xAxe :
                    vert.co[0] = actived.co[0]
                if self.yAxe :
                    vert.co[1] = actived.co[1]
                if self.zAxe :
                    vert.co[2] = actived.co[2]

        return {"FINISHED"}

    
class MoveObjectToCursor(bpy.types.Operator):
    bl_idname = "view3d.move_object_to_cursor"
    bl_label = "move object to cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        context.scene.objects.active.location = context.scene.cursor_location
        return {"FINISHED"}


class SlideVertAlongLine(bpy.types.Operator):
    bl_idname = "view3d.slide_vert_along_line"
    bl_label = "所有[选中点],沿到[活动点]方向滑动"
    bl_options = {'REGISTER', 'UNDO'}

    distance = FloatProperty(0)
    
    def execute(self, context):

        bm = bmesh.from_edit_mesh(context.object.data)

        # 选中的活动顶点
        actived = activedVert(bm)
        if actived==None:
            print("there is no actived vert")
            return {"FINISHED"}

        # 所有 选中点 向 活动点 滑动指定距离
        for vert in bm.verts:
            if vert.select and vert!=actived :
                betw = actived.co - vert.co
                betw = betw * (self.distance/betw.length)
                vert.co+= betw

        return {"FINISHED"}
    


class MoveBackFaces(bpy.types.Operator):
    bl_idname = "view3d.move_back_faces"
    bl_label = "move back selected faces"
    bl_options = {'REGISTER', 'UNDO'}

    distance = FloatProperty(0.2)
    
    def execute(self, context):

        mesh = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        scale = bpy.context.edit_object.scale

        for face in mesh.faces:
            if not face.select :
                continue
            
            move = face.normal * (-self.distance)
            move[0] = move[0] / scale[0]
            move[1] = move[1] / scale[1]
            move[2] = move[2] / scale[2]
            
            for v in face.verts:
                v.co+= move

        # mesh.faces[0].select = True
        bmesh.update_edit_mesh(bpy.context.edit_object.data, True)

        return {"FINISHED"}
    

def includes(array, item) :
    for i in array:
        if i==item :
            return True
    return False

# http://blog.sina.com.cn/s/blog_8f050d6b0101crwb.html
class CreateCrossLineAndFace(bpy.types.Operator):
    bl_idname = "view3d.create_cross_line_and_face"
    bl_label = "create cross point of selected line & face"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        mesh = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        if mesh.faces.active == None :
            return

        print(mesh.edges)
        activeEdge = None
        for edge in mesh.edges:
            if edge.select and not includes(mesh.faces.active.edges, edge) :
                activeEdge = edge
                break

        print("..",activeEdge)

        if activeEdge == None :
            return {"FINISHED"}

        # 平面法向量
        vp1 = mesh.faces.active.normal[0]
        vp2 = mesh.faces.active.normal[1]
        vp3 = mesh.faces.active.normal[2]

        # 平面任意一点
        n1 = mesh.faces.active.edges[0].verts[0].co[0]
        n2 = mesh.faces.active.edges[0].verts[0].co[1]
        n3 = mesh.faces.active.edges[0].verts[0].co[2]

        # 边上的任意两点
        m1 = activeEdge.verts[0].co[0]
        m2 = activeEdge.verts[0].co[1]
        m3 = activeEdge.verts[0].co[2]

        v = activeEdge.verts[1].co - activeEdge.verts[0].co
        v1 = v[0]
        v2 = v[1]
        v3 = v[2]

        t = ((n1-m1)*vp1+(n2-m2)*vp2+(n3-m3)*vp3) / (vp1* v1+ vp2* v2+ vp3* v3)

        x = m1+ v1 * t
        y = m2+ v2 * t
        z = m3+ v3 * t

        vertex = mesh.verts.new([x,y,z])
        bmesh.update_edit_mesh(context.object.data, False, True)

        print(vertex.co)
        

        return {"FINISHED"}



class SelectedVectorsCube(bpy.types.Operator):
    """
    计算并输出所有选中点的立方外边界
    """
    bl_idname = "view3d.selected_vectors_cube"
    bl_label = "SelectedVectorsCube"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        bm = bmesh.from_edit_mesh(context.object.data)

        if len(bm.verts)<1 :
            return {"FINISHED"}

        maxx = minx = maxy = None
        miny = maxz = minz = None

        for vert in bm.verts:
            if not vert.select :
                continue
            
            if minx==None or vert.co[0]<minx : minx = vert.co[0]
            if miny==None or vert.co[1]<miny : miny = vert.co[1]
            if minz==None or vert.co[2]<minz : minz = vert.co[2]

            if maxx==None or vert.co[0]>maxx : maxx = vert.co[0]
            if maxy==None or vert.co[1]>maxy : maxy = vert.co[1]
            if maxz==None or vert.co[2]>maxz : maxz = vert.co[2]

        context.scene.SelectedVectorsCube[0] = maxx- minx
        context.scene.SelectedVectorsCube[1] = maxy- miny
        context.scene.SelectedVectorsCube[2] = maxz- minz

        return {"FINISHED"}



class SelectedVectorsDistance(bpy.types.Operator):
    """
    计算并输出两点距离
    """
    bl_idname = "view3d.selected_vectors_distance"
    bl_label = "SelectedVectorsDistance"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        bm = bmesh.from_edit_mesh(context.object.data)
        p1 = p2 = None

        for vert in bm.verts:
            if not vert.select :
                continue
            if p1 == None :
                p1 = vert.co
                continue
            elif p2 == None :
                p2 = vert.co
                break
    
        if not p1 or not p2 :
            return {"FINISHED"}

        context.scene.SelectedVectorsDistance = (p1-p2).length

        return {"FINISHED"}


class OutputSelectedLocation(bpy.types.Operator):
    """
    输出所有选中点的本地坐标
    """
    bl_idname = "view3d.output_selected_location"
    bl_label = "OutputSelectedLocation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        bm = bmesh.from_edit_mesh(context.object.data)
        for vert in bm.verts:
            if vert.select :
                output(vert.co[0],",",vert.co[1],",",vert.co[2])

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
        layout.row()
        layout.operator(CreateCenterPotinOfSelecteds.bl_idname, text="创建:中点")
        layout.operator(SetOriginToSelected.bl_idname, text="设置:原点>选中中点")
        layout.row()
        layout.row()
        layout.operator(MoveSelectedsToActive.bl_idname, text="移动:选中>活动")
        layout.operator(MoveObjectToCursor.bl_idname, text="移动:活动>游标")
        layout.operator(CursorToSelected.bl_idname, text="移动:游标>选中中点")
        layout.row()
        layout.operator(MovePointsSelectedsToActive.bl_idname, text="移动:选中点>活动点")
        layout.operator(SlideVertAlongLine.bl_idname, text="滑动:选中点>活动点")

        layout.row()
        layout.row()
        layout.operator(OutputSelectedLocation.bl_idname, text="输出选中点坐标")

        layout.row()
        layout.row()
        layout.operator(MoveBackFaces.bl_idname, text="后移:选中[面]沿法向")
        layout.operator(CreateCrossLineAndFace.bl_idname, text="创建:选中[边&面]交点")
        # layout.operator(MoveBackFaces.bl_idname, text="创建:选中[边&边]交点")
        # layout.operator(MoveBackFaces.bl_idname, text="创建:选中[边&边]中垂线")

        layout.row()
        row = layout.row()
        row.operator(SelectedVectorsCube.bl_idname, text="计算:[选中点]立方")
        row.operator(SelectedVectorsDistance.bl_idname, text="计算:两点距离")
        row = layout.row()
        row.prop(context.scene, "SelectedVectorsCube", text="")
        row.prop(context.scene, "SelectedVectorsDistance", text="")


def console_get():
    for area in bpy.context.screen.areas:
        if area.type == 'CONSOLE':
            for space in area.spaces:
                if space.type == 'CONSOLE':
                    return area, space
    return None, None


def output(*args):
    text = ""
    for v in args:
        if type(v) is str:
            text += v + "  "
        else:
            text += str(v) + "  "

    area, space = console_get()
    if space is None:
        for line in text.split("\n"):
            print(line)
        return

    context = bpy.context.copy()
    context.update(dict(
        space=space,
        area=area,
    ))

    for line in text.split("\n"):
        bpy.ops.console.scrollback_append(context, text=line, type='OUTPUT')

    
    
# store keymaps here to access after registration
addon_keymaps = []

def register():
    print("register(Helper)")

    bpy.utils.register_class(CursorToSelected)
    bpy.utils.register_class(SetOriginToSelected)
    bpy.utils.register_class(MoveSelectedsToActive)
    bpy.utils.register_class(MovePointsSelectedsToActive)
    bpy.utils.register_class(MoveObjectToCursor)
    bpy.utils.register_class(CreateCenterPotinOfSelecteds)
    bpy.utils.register_class(DifferenceOfObjects)
    bpy.utils.register_class(SlideVertAlongLine)
    bpy.utils.register_class(CreateCrossLineAndFace)
    bpy.utils.register_class(MoveBackFaces)
    bpy.utils.register_class(SelectedVectorsCube)
    bpy.utils.register_class(SelectedVectorsDistance)
    bpy.utils.register_class(OutputSelectedLocation)
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

    bpy.types.Scene.SelectedVectorsCube = FloatVectorProperty(size=3)
    bpy.types.Scene.SelectedVectorsDistance = FloatProperty()

def unregister_class(clazz):
    try:
        bpy.utils.unregister_class(clazz)
    except RuntimeError:
        pass

def unregister():
    print("unregister()")

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    unregister_class(CursorToSelected)
    unregister_class(SetOriginToSelected)
    unregister_class(MoveSelectedsToActive)
    unregister_class(MovePointsSelectedsToActive)
    unregister_class(MoveObjectToCursor)
    unregister_class(CreateCenterPotinOfSelecteds)
    unregister_class(DifferenceOfObjects)
    unregister_class(SlideVertAlongLine)
    unregister_class(CreateCrossLineAndFace)
    unregister_class(MoveBackFaces)
    unregister_class(SelectedVectorsCube)
    unregister_class(SelectedVectorsDistance)
    unregister_class(OutputSelectedLocation)
    unregister_class(UIHelper)

if __name__ == "__main__":
    register()