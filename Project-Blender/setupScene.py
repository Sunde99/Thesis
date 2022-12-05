import bpy
import sys
import os

# Set up imports
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )


import CleanScene 

# Delete EVERYTHING!

CleanScene.clean_scene()
bpy.context.scene.render.engine = 'CYCLES'
bpy.data.scenes["Scene"].cycles.use_denoising

# -------------------- Set up ground -------------------- 
def setupGround():
    bpy.ops.mesh.primitive_plane_add(size=50)
    bpy.context.active_object.name = 'Ground'
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0


# TODO add material (randomize?)

# -------------------- Set up box (Fix dimentions) -------------------- 
def setupContainer():
    
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0,0,1.5))
    bpy.context.active_object.name = 'Container'

    container_material = bpy.data.materials.new("Container_Material")
    container_material.diffuse_color = (0.2227, 0.8, 0.2656, 1)
    #bpy.ops.object.material_slot_add()
    bpy.context.object.active_material = container_material

    bpy.context.object.scale[2] = 0.75

    container = bpy.context.active_object

    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    container.data.polygons[5].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.delete(type='FACE')

    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    container.data.edges[1].select = True
    container.data.edges[3].select = True
    container.data.edges[6].select = True
    container.data.edges[9].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.bevel(
        offset_type   = 'OFFSET',
        offset        = 0.5,
        segments      = 25,
    )

    # Exit edit mode before moving on
    bpy.ops.object.mode_set(mode = 'OBJECT')

# -------------------- Set up water -------------------- 
def setupWater():
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,1.5))
    bpy.context.active_object.name = 'WaterTop'

    water_material = bpy.data.materials.new("Water_Material")
    water_material.use_nodes = True
    bpy.data.materials["Water_Material"].node_tree.nodes["Principled BSDF"].inputs[5].default_value = 0.25
    bpy.data.materials["Water_Material"].node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0
    bpy.data.materials["Water_Material"].node_tree.nodes["Principled BSDF"].inputs[14].default_value = 1.33
    bpy.data.materials["Water_Material"].node_tree.nodes["Principled BSDF"].inputs[15].default_value = 1
    bpy.context.object.active_material = water_material

    bpy.context.object.scale[0] = 1.5
    bpy.context.object.scale[1] = 1.5

    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.bevel(
        offset          = 0.5, 
        offset_pct      = 0, 
        segments        = 25, 
        affect          = 'VERTICES', 
        release_confirm = True
    )



# -------------------- Set up lego (randomize) -------------------- 
def setupLego():
    
     # Load from file
    bpy.ops.import_mesh.stl(filepath="C:\\Users\Matias\\_Thesis\Project-Blender\\files\\LEGO-2X4-L_simple.stl")

    lego_material = bpy.data.materials.new("Lego_Material")
    lego_material.use_nodes = True
    bpy.data.materials["Lego_Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
    bpy.context.object.active_material = lego_material


    bpy.context.object.scale[0] = 0.02
    bpy.context.object.scale[1] = 0.02
    bpy.context.object.scale[2] = 0.02

    bpy.context.object.location[0] = 0.5
    bpy.context.object.location[1] = 0.76
    bpy.context.object.location[2] = 0.375

    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')

    bpy.context.object.rotation_euler[0] = 3.141593
    bpy.context.object.rotation_euler[1] = -3.141593
    bpy.context.object.rotation_euler[2] = 2.69
     # Build bricks (Maybe start with one big?)
     # Place on random pos
     # Random rotation
     # Random material
     
    bpy.ops.transform.resize(value=(1.36265, 1.36265, 1.36265), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
     
    bpy.ops.transform.translate(value=(0.233577, -0.0974, 0.044318), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

    bpy.ops.transform.resize(value=(0.665307, 0.665307, 0.665307), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


# -------------------- Set up light (randomize?) -------------------- 
def setupLight():
    bpy.ops.object.light_add(location=(5, 2, 12), type='SPOT')
    bpy.context.active_object.name = 'SpotLight'
    bpy.data.lights["Spot"].energy = 10000
    bpy.data.objects['SpotLight'].rotation_euler = (0.027, 0.465, 0.377)

# -------------------- Set up camera (randomize?) -------------------- 
def setupCamera():
    bpy.ops.object.camera_add(location=(0.33,3,6.69), rotation=(-2.47, 3.2, -0.04))
    bpy.context.active_object.name = 'Camera'
    bpy.context.scene.camera = bpy.context.object

# Set up render (In its own file!)
def render(name="name"):
    
    bpy.context.scene.render.filepath = f'C:\\Users\\Matias\\_Thesis\\pictures\\Autogenerated\\{name}'
    bpy.context.scene.render.resolution_x = 512 #perhaps set resolution in code
    bpy.context.scene.render.resolution_y = 512
    bpy.ops.render.render(write_still = True)
    bpy.ops.render.render()
    
def createJson():
    
    

setupGround()
setupContainer()
setupWater()
setupLego()
setupLight()
setupCamera()

render("Water")

bpy.data.objects["WaterTop"].hide_render = True

render("NoWater")

# TODO REMOVE This is only while testing
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
