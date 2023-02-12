import bpy
import mathutils
from mathutils import Matrix
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
def setupGround(flipColors = False, texture = "Checkered", primaryColor = 14922970, secondaryColor = 10369869):
    
    color1 = secondaryColor if flipColors else primaryColor
    color2 = primaryColor if flipColors else secondaryColor
    
    bpy.ops.mesh.primitive_plane_add(size=50)
    bpy.context.active_object.name = 'Ground'
    bpy.context.object.location[0] = 0
    bpy.context.object.location[1] = 0
    bpy.context.object.location[2] = -0.01

    ground_material = bpy.data.materials.new('Ground_Material')
    ground_material.use_nodes = True
    P_BSDF = ground_material.node_tree.nodes.get('Principled BSDF')
    P_BSDF.inputs[0].default_value = hex_to_rgb(int(color1))
    
    #Material
    #print(texture)
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
    
    bpy.ops.mesh.primitive_cube_add(size=3)
    bpy.context.active_object.name = 'Container'

    container_material = bpy.data.materials.new("Container_Material")
    container_material.diffuse_color = (0.2227, 0.8, 0.2656, 1)
    #bpy.ops.object.material_slot_add()
    bpy.context.object.active_material = container_material

    bpy.context.object.scale[2] = 0.75

    container = bpy.context.active_object
    
    data = container.data
    min_z = min([v.co.z for v in data.vertices])
    container.location.z -= min_z
    data.transform(Matrix.Translation((0, 0, -min_z)))
    data.update()
    
    container.location = (0,0,0)


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
        offset          = 0.34, 
        offset_pct      = 0, 
        segments        = 25, 
        affect          = 'VERTICES', 
        release_confirm = True
    )



# -------------------- Set up lego (randomize) -------------------- 

def setupLego(legoX, legoY, legoRot):
    
     # Load from file
    lego = bpy.data.objects["Empty"]
    lego.select_set(state=True)
    bpy.context.view_layer.objects.active = lego
    
    
    bpy.context.object.location[0] = legoX
    bpy.context.object.location[1] = legoY
    bpy.context.object.location[2] = 0.15

    bpy.context.object.rotation_euler[0] = 3.1416
    bpy.context.object.rotation_euler[1] = -3.1416 
    bpy.context.object.rotation_euler[2] = legoRot

    


    bpy.context.object.scale[0] *= 0.01
    bpy.context.object.scale[1] *= 0.01
    bpy.context.object.scale[2] *= 0.01

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
    
    
    
    #bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
    setupLegoMaterial(lego)


def setupLegoShape(legoMatrix):
    
    
    legoParent = None
    # Loops over all indexes from bottom up
    #print(legoMatrix)
    isParent = True
    
    for z in range(2, -1, -1):
        for x in range(7):
            for y in range(5):
                if legoMatrix[x][y][z] == 1:
                    if isParent:
                        bpy.ops.import_mesh.stl(filepath=f"{dir}\\files\\LEGO-2X2-L_simple.stl")
                        legoParent = bpy.context.scene.objects["LEGO-2X2-L_simple"]
                        bpy.ops.object.transform_apply()
                        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
                        buildLego(legoParent, x, y, z, isParent) 
                        #print("---->", x, y, z)
                        
                        
                        
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

def setupBoundingBox(boundX, boundY, boundZ):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.empty_add(type="CUBE")
    boundingBox = bpy.data.objects["Empty"]
    boundingBox.select_set(state=True)
    bpy.context.view_layer.objects.active = boundingBox
    bpy.context.object.location = (8*(boundX-1), 8*(boundY-1), 4.8*(boundZ-1))
    bpy.context.object.scale = (8*boundX, 8*boundY, 4.8*boundZ)
    
    bpy.ops.object.select_all(action='DESELECT')
    legoParent = bpy.context.scene.objects["LEGO-2X2-L_simple"]
    legoParent.parent = boundingBox
    legoParent.matrix_parent_inverse = boundingBox.matrix_world.inverted()

    

# -------------------- Set up light (randomize?) -------------------- 
def setupLight(lightX, lightY, lightZ):
    bpy.ops.object.light_add(location=(lightX, lightY, lightZ), type='POINT')
    bpy.context.active_object.name = 'PointLight'
    bpy.data.lights["Point"].energy = 20000
    #bpy.data.objects['PointLight'].rotation_euler = (0.027, 0.465, 0.377)

# -------------------- Set up camera (randomize?) -------------------- 
def setupCamera(camera_x = -1, camera_y = -1, camera_z = -1, randomize = True):
    
    t_x = 0
    t_y = 0
    t_z = 0
    
    if randomize:
        
        t_x = random.uniform(-0.2, 0.2)
        t_y = random.uniform(-1.2, 0)
        t_z = random.uniform(-0.2, 0.2)
    else:
        camera_x =  0.0
        camera_y = 2.0
        camera_z = 7.0
        
        t_x = 0.0
        t_y = -0.6
        t_z = 0
    
    target_location = (t_x, t_y, t_z)
    
    #print(t_x, t_y, t_z)
    
    bpy.ops.object.camera_add()
    camera = bpy.context.scene.objects["Camera"]
    camera.location = (camera_x, camera_y, camera_z)
    
    direction = mathutils.Vector(camera.location) - mathutils.Vector(target_location)
    camera.rotation_mode = 'XYZ'
    camera.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    
    bpy.context.active_object.name = 'Camera'
    bpy.context.scene.camera = bpy.context.object

# Set up render (In its own file!)
def render(name="name", pred = False):
    
    if pred:
        bpy.context.scene.render.filepath = f'{dir}\\pictures\\Predictions\\{name}'
    else:
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
    start = 0
    stop = 2000
    for i, row in enumerate(metadata):
        if i < start:
            continue
        if i == stop:
            break
        
        CleanScene.clean_scene()     
        setupGround(int(row[1]), row[2], row[3], row[4])
        setupContainer()
        setupWater(float(row[8]))
        
        #print(row[12])
        setupLegoShape(ast.literal_eval(row[12]))
        setupBoundingBox(int(row[13]), int(row[14]), int(row[15]))
        setupLego(float(row[9]), float(row[10]), float(row[11]))

        #print(ast.literal_eval(row[12]))
        
        setupLight(float(row[5]), float(row[6]), float(row[7]))
        setupCamera(float(row[16]), float(row[17]), float(row[18]))
        #break
        render(f"{row[0]}")
        
        #if i == 5:
        #    break
        
        amountOfRows = stop-start
        if i != 0 and i % 20 == 0:
            elapsed_time = time.time() - start_time
            remaining_time = (elapsed_time / i) * (amountOfRows - i)
            completion_time = time.ctime(time.time() + remaining_time)
            print("The current run will finish at approximatly", completion_time)
        

#    for obj in bpy.data:
#        print(obj)
def renderTrue(i, row):
    setupWater(float(row[3]))
    setupLegoShape(ast.literal_eval(row[7]))
    setupBoundingBox(float(row[8]), float(row[9]), float(row[10]))
    setupLego(float(row[0]), float(row[1]), float(row[2]))
    setupLight(float(row[4]), float(row[5]), float(row[6]))
    setupCamera(randomize = False)
    render(f"image_{i}_True", pred=True)

def renderPred(i, row, lightX, lightY, lightZ):
    setupWater(float(row[3]))
    setupLegoShape(ast.literal_eval(row[4]))
    setupBoundingBox(float(row[5]), float(row[6]), float(row[7]))
    setupLego(float(row[0]), float(row[1]), float(row[2]))
    setupLight(float(lightX), float(lightY), float(lightZ))
    setupCamera(randomize = False)
    render(f"image_{i}_Pred", pred=True)

def testPrediction():
    predFile = open(f'{dir}\\pictures\\Metadata\\RecreatedImageData.csv')
    predMetadata = csv.reader(predFile)
    header = next(predMetadata)
    
    trueFile = open(f'{dir}\\pictures\\Metadata\\TrueImageData.csv')
    trueMetadata = csv.reader(trueFile)
    header = next(trueMetadata)
    for i, row in enumerate(trueMetadata):
        CleanScene.clean_scene()
        setupGround()  
        setupContainer()
        #setupWater(float(row[3]))
        #
        renderTrue(i, row)
        
        CleanScene.clean_scene()
        setupGround()  
        setupContainer()
        #setupWater(float(row[3]))
        renderPred(i, next(predMetadata), row[4], row[5], row[6])
        
    predFile.close()
    trueFile.close()

if __name__ == "__main__":
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

    #testPrediction()
    
    #file = open(f'{dir}\\pictures\\Metadata\\ImageData.csv')
    #renderLoop(file)
    #file.close()
    #

    #bpy.data.objects["WaterTop"].hide_render = True

    #render("NoWater")

    # TODO REMOVE This is only while testing
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
