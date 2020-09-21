bl_info = {
    "name": "Portrait Lighting Studio.",
    "author": "Rithvik Kadiresan",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D",
    "description": "Adds Studio Style Lighting for Portrait Renders. ",
    "warning": "Make Sure your Bust/Head is facing the Y axis with the X axis being horizontal to it, and it is selected; to work.",
    "doc_url": "",
    "category": "Add Lighting",
}

##need to fix panel menu
#class PlightingPanel(bpy.types.Panel):
#    """Adds Studio Like Portait Lighitng"""
#    bl_label = "Portrait lighitng Panel"
#    bl_idname = "SCENE_PT_layout"
#    bl_space_type = 'PROPERTIES'
#    bl_region_type = 'WINDOW'
#    bl_context = "scene"

#    def draw(self, context):
#        layout = self.layout

#        scene = context.scene

#        layout.label(text="Add Studio Portrait Lighitng:")
#        row = layout.row()
#        row.scale_y = 2.0
#        row.operator("object.portrait_lighting") 


import bpy

class PortraitLighting(bpy.types.Operator):
    """Setup Portrait Lighting"""
    bl_idname = "object.portrait_lighting"
    bl_label = "Add Studio Potrait Lighting"

    def execute(self, context):            
        #assigning variables for object data
        so = bpy.context.active_object
        sox = so.location.x
        soy = so.location.y
        soz = so.location.z
        light_power = 1000
        #adding rim light and moving it to be above context object
        bpy.ops.object.light_add(type=('AREA'))
        rimlight = bpy.context.active_object
        rimlight.location[2] = soz + 2
        bpy.context.object.data.energy = light_power
        rimlight.name = 'Rimlight'
        #bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name="Portrait Lighting Setup")

        #adding keylight and oreinting it
        bpy.ops.object.light_add(type=('AREA'))
        keylight = bpy.context.active_object
        keylight.location[1] = soy + -1
        keylight.location[0] = sox + 10
        bpy.context.object.data.energy = light_power
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = so
        keylight.name = 'keylight'

        #adding fill light
        bpy.ops.object.light_add(type=('AREA'))
        flight = bpy.context.active_object
        flight.location[1] = soy + -5
        flight.location[0] = sox + -10
        bpy.context.object.data.energy = light_power - 500
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = so
    
        return {'FINISHED'}



#drawing menu 
   
class LightingMenu(bpy.types.Menu):
    bl_label = "Portrait Lighting"
    bl_idname = "pmenu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.portrait_lighting")
        




addon_keymaps = []




def register():
    bpy.utils.register_class(PortraitLighting)
    bpy.utils.register_class(LightingMenu)
    #bpy.utils.register_class(PlightingPanel)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
        kmi = km.keymap_items.new("object.portrait_lighting", type= 'F', value= 'PRESS', shift= True)
        
        addon_keymaps.append((km,kmi))


def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear
        
    
    
    bpy.utils.unregister_class(PortraitLighting)
    bpy.utils.unregister_class(LightingMenu)
    #bpy.utils.unregister_class(PlightingPanel)
    
    

if __name__ == "__main__":
    register()



    # Portrait Lighting test call
    #bpy.ops.object.portrait_lighting()
    # The menu can also be called from scripts
    #bpy.ops.wm.call_menu(name=LightingMenu.bl_idname)

    
    




