import bpy
import sys
import os
import json
import csv
import ast
import random
import time

random.seed(42)




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
def setupGround(flipColors, texture, primaryColor, secondaryColor):
    
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

    if (texture == 'Bricks'):
        brick_node = ground_material.node_tree.nodes.new('ShaderNodeTexBrick')

        ground_material.node_tree.links.new(brick_node.outputs[0], P_BSDF.inputs[0])
        brick_node.inputs[4].default_value = 15
        
        brick_node.inputs[1].default_value = hex_to_rgb(int(color1))
        brick_node.inputs[2].default_value = hex_to_rgb(int(color2))


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
    lego = bpy.data.objects["LEGO-2X2-L_simple"]
    lego.select_set(state=True)
    bpy.context.view_layer.objects.active = lego

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

def setupLegoMaterial(lego):
    lego_material = bpy.data.materials.new("Lego_Material")
    lego_material.use_nodes = True
    objects = bpy.data.objects
    lego.active_material = lego_material
    
    random_red = random.randint(0, 10) / 10
    random_gre = random.randint(0, 10) / 10
    random_blu = random.randint(0, 10) / 10
    
    lego.active_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (random_red, random_gre, random_blu, 1)

def buildLego(lego, x, y, z, isParent):

    objects = bpy.data.objects
    dx = 16
    dy = 16
    dz = 9.6
    
    lego.location[0] = x*dx
    lego.location[1] = y*dy
    lego.location[2] = (2-z)*dz
    
    if not isParent:
        parent = bpy.context.scene.objects["LEGO-2X2-L_simple"]
        lego.parent = parent
        lego.matrix_parent_inverse = parent.matrix_world.inverted()
        
    setupLegoMaterial(lego)


def setupLegoShape(legoMatrix):
    
    
    legoParent = None
    # Loops over all indexes from bottom up
    print(legoMatrix)
    isParent = True
    
    for z in range(2, -1, -1):
        for x in range(3):
            for y in range(3):
                if legoMatrix[x][z][y] == 1:
                    if isParent:
                        bpy.ops.import_mesh.stl(filepath=f"{dir}\\files\\LEGO-2X2-L_simple.stl")
                        legoParent = bpy.context.scene.objects["LEGO-2X2-L_simple"]
                        isParent = False
                    else:
                        bpy.ops.object.select_all(action='DESELECT')
                        legoParent.select_set(state=True)
                        bpy.context.view_layer.objects.active = legoParent
                        bpy.ops.object.duplicate(linked=False)
                        lego = bpy.context.active_object
                        buildLego(lego, x, y, z, isParent) 
                         
    setupLegoMaterial(legoParent)
                    

#    return parent
    

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
    
    bpy.context.scene.render.filepath = f'{dir}\\pictures\\Autogenerated\\{name}'

    bpy.ops.render.render(write_still = True)
    bpy.ops.render.render()
    
def createJson():
    path = f'{dir}\\metadata.json'
    if not (os.path.isfile(path)):
        jsonString = {}
        jsonFile = open("metadata.json", "w")
        jsonFile.write(json.dumps(jsonString))
        jsonFile.close()
    metadata = open("metadata.json")
    
    
def renderLoop(file):
    start_time = time.time()
    metadata = csv.reader(file)
    header = next(metadata)
    for i, row in enumerate(metadata):
        CleanScene.clean_scene()     
        setupGround(int(row[1]), row[2], row[3], row[4])
        setupContainer()
        setupWater(float(row[8]))

        setupLegoShape(ast.literal_eval(row[12]))
        setupLego(float(row[9]), float(row[10]), float(row[11]))
        setupLight(float(row[5]), float(row[6]), float(row[7]))
        setupCamera()
        render(f"{row[0]}")
        
        amountOfRows = 6000
        if i != 0 and i % 20 == 0:
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / i) * (amountOfRows - i)
            completion_time = time.ctime(time.time() + remaining_time)
            print("The code will finish at approximatly", completion_time)


#    for obj in bpy.data:
#        print(obj)
        

if __name__ == "__main__":
    bpy.app.debug_value = 3
    # Set up imports
    dir = os.path.dirname(bpy.data.filepath)
    if not dir in sys.path:
        sys.path.append(dir )
    print("dir: " + str(dir))
    import CleanScene 
    

    # Delete EVERYTHING!

    CleanScene.clean_scene()
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.data.scenes["Scene"].cycles.use_denoising
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.render.resolution_x = 64
    bpy.context.scene.render.resolution_y = 64
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.cycles.max_bounces = 4


    file = open(f'{dir}\\pictures\\Metadata\\ImageData.csv')
    renderLoop(file)
    file.close()
    #

    #bpy.data.objects["WaterTop"].hide_render = True

    #render("NoWater")

    # TODO REMOVE This is only while testing
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
