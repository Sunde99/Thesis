import csv
import sys
import os
import itertools
import bpy

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
print("dir: " + str(dir))


def setupMetadata():
    header = ['ID', 'flipColors', 'GroundTexture', 'GroundPrimaryColor', 'GroundSecondaryColor', 'LightX', 'LightY', 'LightZ', 'WaterHeight', 'LegoX', 'LegoY', 'legoRot']
    groundTextures = ['Blank', 'Checkered']
    flipColors = [1, 0]
    groundPrimaryColors = [0xE3B4DA, 0x7E9E73]
    groundSecondaryColors = [0x9E3B4D, 0xBA70F5]
    lightX = [5]
    lightY = [2]
    lightZ = [12]
    WaterHeight = [1.5]
    LegoX = [-0.700]
    LegoY = [-0.710]
    LegoRot = [2.69, 1.67]
    temp = [flipColors, groundTextures, groundPrimaryColors, groundSecondaryColors, lightX, lightY, lightZ, WaterHeight, LegoX, LegoY, LegoRot]
    everyCombination = list(itertools.product(*temp))
    with open(f'{dir}\\pictures\\Metadata\\ImageData.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        i = 0
        for row in everyCombination:
            id = f'image_{i}'
            imageData = (id, *row)
            writer.writerow(imageData)
            i += 1
        
        
setupMetadata()