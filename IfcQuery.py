bl_info = {
    "name" : "My Addons",
    "author" : "Carlos Dias",
    "version" : (0, 1),
    "blender" : (2,80,0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Execute queries in ifc files",
    "warning": "",
    "doc_url": "",
    "category": "My Addons",
}

import bpy
import ifcopenshell
from ifcopenshell.util.selector import Selector
import blenderbim.bim.ifc


class OBJECT_PT_IfcQuery(bpy.types.Panel):

    bl_idname = "OBJECT_PT_IfcQuery"
    bl_label = "My AddOns"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Addons'
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.ifcquery", text="IFC Query", icon="VIEWZOOM")
        



# IFC Query selector        
class WM_OT_ExecuteQuery(bpy.types.Operator):
    bl_label = "Execute Query"
    bl_idname = "wm.ifcquery" 
    
    text = bpy.props.StringProperty(name = "Query :", default="")
    hide = bpy.props.BoolProperty(name = "Hide Unselect", default= False)
    
    def execute(self, context):
        #bpy.ops.object.hide_view_clear()
        bpy.ops.object.select_all(action='DESELECT')
        
        h = self.hide
        try:
            ifc = blenderbim.bim.ifc.IfcStore().get_file()
            
            selector = Selector()
            elements = selector.parse(ifc, self.text)

            l = [e.GlobalId for e in elements]
        
            for obj in bpy.data.objects:
                if obj.BIMObjectProperties.attributes[0].string_value in l:
                    obj.select_set(True)
                    obj.hide_set(False)
            
            if h:
                bpy.ops.object.hide_view_set(unselected=True)
        except:
            self.report({"ERROR"}, "No results for query")
        
        return {"FINISHED"}
     
    def invoke(self, context, event):
         return context.window_manager.invoke_props_dialog(self)      




def register():
    bpy.utils.register_class(OBJECT_PT_IfcQuery)
    bpy.utils.register_class(WM_OT_ExecuteQuery)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_IfcQuery)
    bpy.utils.unregister_class(WM_OT_ExecuteQuery)


if __name__ == "__main__":
    register()
