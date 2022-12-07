import csv
import itertools

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
    temp = [groundTextures, flipColors, groundPrimaryColors, groundSecondaryColors, lightX, lightY, lightZ, WaterHeight, LegoX, LegoY, LegoRot]
    everyCombination = list(itertools.product(*temp))
    with open('C:\\Users\\Matias\\_Thesis\\pictures\\Metadata\\ImageData.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        i = 0
        for row in everyCombination:
            id = f'image_{i}'
            imageData = (id, *row)
            writer.writerow(imageData)
            i += 1
        
        
setupMetadata()