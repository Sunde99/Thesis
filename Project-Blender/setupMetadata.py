import csv
import sys
import os
import itertools
import bpy
import random
import math

random.seed(42)

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
print("dir: " + str(dir))
import buildLego

def setupMetadata():
    header = ['ID', 'flipColors', 'GroundTexture', 'GroundPrimaryColor', 'GroundSecondaryColor', 'LightX', 'LightY', 'LightZ', 'WaterHeight', 'LegoX', 'LegoY', 'legoRot', 'lego_shape', 'lego_length', 'lego_width', 'lego_height', 'cameraX', 'cameraY', 'cameraZ']
    groundTextures = ['Blank', 'Checkered', 'Bricks']
    flipColors = [1, 0]
    groundPrimaryColors = [0xE3B4DA, 0x7E9E73, 0x5818BE]
    groundSecondaryColors = [0x9E3B4D, 0xBA70F5, 0x5A8D13]
#    lightX = [random.randint(-6, 6) for _ in range(3)]
#    lightY = [random.randint(-6, 6) for _ in range(3)]
    lightZ = 12
#    WaterHeight = 1.5
#    LegoX = [random.uniform(-0.8, 1) for _ in range(3)]
#    LegoY = [random.uniform(-0.8, 1) for _ in range(3)]
#    LegoRot = [random.uniform(0, 2) * math.pi for _ in range(3)
    temp = [flipColors, groundTextures, groundPrimaryColors, groundSecondaryColors]
    combinations = list(itertools.product(*temp))
    #print("-----------------------------NEW-------------------------------------")
    with open(f'{dir}\\pictures\\Metadata\\ImageData.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(6000):
            #print("-------------------------------------------------------------------")
            lego_shape, lego_length, lego_width, lego_height = buildLego.create_connected_matrix()
            
            water_height = random.uniform(0.1, 1.8) # change to 2.5 max
            camera_x = random.uniform(-0.6, 0.6)
            camera_y = random.uniform(1.6, 2.6)
            camera_z = random.uniform(6, 7.5)
            row = [*combinations[i%54], random.randint(-6, 6), random.randint(-6, 6), lightZ, water_height, random.uniform(-0.83, 0.83), random.uniform(-0.83, 0.83), random.uniform(0, 2) * math.pi, lego_shape, lego_length, lego_width, lego_height, camera_x, camera_y, camera_z]
            
            id = f'image_{i}'
            imageData = (id, *row)
            writer.writerow(imageData)
        
setupMetadata()