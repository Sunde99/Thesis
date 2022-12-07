import bpy
import sys
import os
import json
import csv

# Set up imports
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )


import CleanScene 

# Delete EVERYTHING!

CleanScene.clean_scene()
bpy.context.scene.render.engine = 'CYCLES'
bpy.data.scenes["Scene"].cycles.use_denoising

# Convert hex to rgb
def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])

# -------------------- Set up ground -------------------- 
def setupGround(texture, flipColors, primaryColor, secondaryColor):
    
    color1 = secondaryColor if flipColors else primaryColor
    color2 = primaryColor if flipColors else secondaryColor
    
    bpy.ops.mesh.primitive_plane_add(size=50)
    bpy.context.active_object.name = 'Ground'
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = 0

    ground_material = bpy.data.materials.new('Ground_Material')
    ground_material.use_nodes = True
    P_BSDF = ground_material.node_tree.nodes.get('Principled BSDF')
    P_BSDF.inputs[0].default_value = hex_to_rgb(int(color1))
    
    #Material
    print(texture)
    if (texture == 'Checkered'):
        checker_node = ground_material.node_tree.nodes.new('ShaderNodeTexChecker')

        ground_material.node_tree.links.new(checker_node.outputs[0], P_BSDF.inputs[0])
        checker_node.inputs[3].default_value = 15
        
        checker_node.inputs[1].default_value = hex_to_rgb(int(color1))
        checker_node.inputs[2].default_value = hex_to_rgb(int(color2))


    bpy.context.object.active_material = ground_material




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
def setupWater(height):
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0,0,height))
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

def setupLego(legoX, legoY, legoRot):
    
     # Load from file
    bpy.ops.import_mesh.stl(filepath="C:\\Users\Matias\\_Thesis\Project-Blender\\files\\LEGO-2X4-L_simple.stl")

    lego_material = bpy.data.materials.new("Lego_Material")
    lego_material.use_nodes = True
    bpy.data.materials["Lego_Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
    bpy.context.object.active_material = lego_material
    
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')

    bpy.context.object.rotation_euler[0] = 3.1416
    bpy.context.object.rotation_euler[1] = -3.1416 
    bpy.context.object.rotation_euler[2] = legoRot

    bpy.context.object.location[0] = legoX
    bpy.context.object.location[1] = legoY
    bpy.context.object.location[2] = 0.541523

    bpy.context.object.scale[0] = 0.018132
    bpy.context.object.scale[1] = 0.018132
    bpy.context.object.scale[2] = 0.018132

    


     # Build bricks (Maybe start with one big?)
     # Place on random pos
     # Random rotation
     # Random material
     

# -------------------- Set up light (randomize?) -------------------- 
def setupLight(lightX, lightY, lightZ):
    bpy.ops.object.light_add(location=(lightX, lightY, lightZ), type='POINT')
    bpy.context.active_object.name = 'PointLight'
    bpy.data.lights["Point"].energy = 20000
    #bpy.data.objects['PointLight'].rotation_euler = (0.027, 0.465, 0.377)

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
    path = 'C:\\Users\Matias\\_Thesis\\Project-Blender\\metadata.json'
    if not (os.path.isfile(path)):
        jsonString = {}
        jsonFile = open("metadata.json", "w")
        jsonFile.write(json.dumps(jsonString))
        jsonFile.close()
    metadata = open("metadata.json")
    
    
def renderLoop(file):
    
    metadata = csv.reader(file)
    header = next(metadata)

    for row in metadata:
        CleanScene.clean_scene()
        setupGround(row[1], int(row[2]), row[3], row[4])
        setupContainer()
        setupWater(float(row[8]))
        setupLego(float(row[9]), float(row[10]), float(row[11]))
        setupLight(float(row[5]), float(row[6]), float(row[7]))
        setupCamera()
        render(f"{row[0]}")
#    for obj in bpy.data:
#        print(obj)
        


file = open('C:\\Users\\Matias\\_Thesis\\pictures\\Metadata\\ImageData.csv')
renderLoop(file)
file.close()
#

#bpy.data.objects["WaterTop"].hide_render = True

#render("NoWater")

# TODO REMOVE This is only while testing
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
