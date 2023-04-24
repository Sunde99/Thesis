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
    lightZ = 1.2
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
        for i in range(10000):
            #print("-------------------------------------------------------------------")
            
            
            lightX = random.uniform(-0.6, 0.6)
            lightY = random.uniform(-0.6, 0.6)
            
            water_height = random.uniform(0.04, 0.28) 
            
            legoX = random.uniform(-0.09711, 0.09711)
            legoY = random.uniform(-0.09711, 0.09711)
            legoRot = random.uniform(0, 2) * math.pi
            
            lego_shape, lego_length, lego_width, lego_height = buildLego.create_connected_matrix()
            
            camera_x = random.uniform(-0.09, 0.09)
            camera_y = random.uniform(0.20, 0.35)
            camera_z = random.uniform(0.82, 0.95)
            
            row = [*combinations[i%54], 
                    lightX, lightY, lightZ, 
                    water_height, 
                    legoX, legoY, legoRot, 
                    lego_shape, 
                    lego_length, lego_width, lego_height, 
                    camera_x, camera_y, camera_z]
            
            id = f'image_{i}'
            imageData = (id, *row)
            writer.writerow(imageData)
        
        
def setupMetadataTesting():
    header = ['ID', 'flipColors', 'GroundTexture', 'GroundPrimaryColor', 'GroundSecondaryColor', 'LightX', 'LightY', 'LightZ', 'WaterHeight', 'LegoX', 'LegoY', 'legoRot', 'lego_shape', 'lego_length', 'lego_width', 'lego_height', 'cameraX', 'cameraY', 'cameraZ']
    groundTextures = ['Checkered']
    flipColors = [0]
    groundPrimaryColors = [0xE3B4DA]
    groundSecondaryColors = [0x9E3B4D]
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
    with open(f'{dir}\\pictures\\Metadata\\ImageDataTest.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        lego_shape, lego_length, lego_width, lego_height = buildLego.create_connected_matrix()
        for i in range(600):
            #print("-------------------------------------------------------------------")
            
            
            lightX = -4
            lightY = 3
            
            water_height = random.uniform(0.4, 1.8)
            
            legoX = 0
            legoY = 0
            legoRot = 0
            
            camera_x = 0
            camera_y = 2
            camera_z = 7
            
            row = [*combinations[0], 
                    lightX, lightY, lightZ, 
                    water_height, 
                    legoX, legoY, legoRot, 
                    lego_shape, 
                    lego_length, lego_width, lego_height, 
                    camera_x, camera_y, camera_z]
            
            id = f'image_{i}'
            imageData = (id, *row)
            writer.writerow(imageData)
            
setupMetadata()
#setupMetadataTesting()