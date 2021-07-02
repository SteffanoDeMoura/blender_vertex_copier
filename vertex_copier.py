# ##### BEGIN GPL LICENSE BLOCK #####
#   
#    Vertex Copier Copyright (C) 2021  Steffano de Moura <fanolinux@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>
#
# ##### END GPL LICENSE BLOCK #####

import bpy, bmesh

#copy all vertices coordinates
def DoCopyAll (source, target):  
    for vertex in source.data.vertices:
        target.data.vertices[vertex.index].co = source.data.vertices[vertex.index].co

#copy selected vertices coordinates
def DoCopySelected (source, target):  
    for vertex in source.data.vertices:
        if vertex.select == True:
            target.data.vertices[vertex.index].co = source.data.vertices[vertex.index].co

class View3DPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
class CopyVertexLocation(bpy.types.Operator):
    bl_idname = "exe.copyvertexlocation"
    bl_label = "Copy vertext coordinate"
    bl_options = {'REGISTER', 'UNDO'}
    
    sname : bpy.props.StringProperty(name="sname")
    tname : bpy.props.StringProperty(name="tname")
    selonly : bpy.props.BoolProperty(name="selonly")

    def execute(self, context):
        if not self.sname or not self.tname:
                self.report({'WARNING'}, f"Please set Source & Target objects'")
        else:
            if self.selonly is True:
                DoCopySelected(bpy.data.objects[self.sname], bpy.data.objects[self.tname])
                self.report({'INFO'}, f"DoCopySelected: Source is '{self.sname}' & Target is '{self.tname}' & SelectedOnly is '{self.selonly}'")
            else:
                DoCopyAll(bpy.data.objects[self.sname], bpy.data.objects[self.tname])
                self.report({'INFO'}, f"DoCopyAll: Source is '{self.sname}' & Target is '{self.tname}' & SelectedOnly is '{self.selonly}'")

        return {'FINISHED'}

class PanelOne(View3DPanel, bpy.types.Panel):
    bl_idname = "vertices_retargeter"
    bl_label = "Vertex Copier"
    
    def draw(self, context):
        #define layout
        layout = self.layout
        #define scene
        scene = context.scene
        #start layout
        layout.label(text="Make sure to select Source & Target objects")
        #input fields
#        Source = context.object
        layout.prop_search(scene, "Source", scene, "objects")
        layout.prop_search(scene, "Target", scene, "objects")
        layout.prop(scene, "SelectedOnly", text="Selected vertices only (From Source)")
        # Big button
        row = layout.row()
        row.scale_y = 2.0
        op = row.operator(CopyVertexLocation.bl_idname, text = "GO", icon = "TRIA_RIGHT")
        #set source and target names
        op.sname = bpy.context.scene.Source
        op.tname = bpy.context.scene.Target
        op.selonly = bpy.context.scene.SelectedOnly
        layout.label(text=" ")

def register():
    bpy.utils.register_class(PanelOne)
    bpy.utils.register_class(CopyVertexLocation)
    bpy.types.Scene.Source = bpy.props.StringProperty(name="Source")
    bpy.types.Scene.Target = bpy.props.StringProperty(name="Target")
    bpy.types.Scene.SelectedOnly = bpy.props.BoolProperty(name="SelectedOnly")

def unregister():
    bpy.utils.unregister_class(PanelOne)
    bpy.utils.unregister_class(CopyVertexLocation)
    del bpy.types.Object.Source
    del bpy.types.Object.Target
    del bpy.types.Object.SelectedOnly

if __name__ == "__main__":
    register()