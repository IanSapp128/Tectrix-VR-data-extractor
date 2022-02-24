import os
import re
import sys

'''
Tectrix VR data extractor
2022 Ian Sapp
'''

textureDict = {}
file1 = open('one', 'rb')
data = file1.readlines()
Bitmap = bytes.fromhex('424D')

count = 0
polyCount = 0

for line in data:
    # Get the texture names and byte size
    if line.startswith(b'; ') and b'.bmp' in line:
        if not b'Input' in line:
            string = line.decode('utf-8').replace('\n','').replace('; ', '')
            string = string.split()
            string[0] = string[0].replace('.bmp', '')
            textureDict[string[0]] = string[3]

    if Bitmap in line:
        for key, value in list(textureDict.items()):
            bmpBytes = str.encode(f' {key}.bmp')
            wdfBytes = str.encode(f' {key}.wdf')
            if bmpBytes in line or wdfBytes in line:
                offset = line.index(Bitmap)
                byteSized = int(value)
                comboBytes = data[count]
                iterations = 50

                for i in range(1, 900):
                    comboBytes += data[count + i]

                byteClean = comboBytes[offset:]
                byteClean = byteClean[:byteSized]
                doesExist = os.path.exists('textures')

                if not doesExist:
                    os.makedirs('textures')
                
                outFile = open(f'./textures/{key}.bmp', 'wb')
                outFile.write(bytes(byteClean))
                outFile.close()
                del textureDict[key]
    
    if b'(dres' in line and b'(polygon' in line :
        result = re.search(b'\(dres(.*?)\(', line)
        bfileName = result.group(1).replace(b' ', b'')
        fileName = bfileName.decode('utf-8')
        result = re.search(b'\(polygon(.*)\)\)\)', line)

        if result.group(1):
            lines = []
            poly = re.findall(b'\(.*?\)', result.group(1))
            typeCount = 0
            for gon in poly:                
                gonString = str(gon.decode('utf-8'))
                cleanedString = gonString.replace('(', '').replace(')', '')
                if '((' in gonString:
                    typeCount = typeCount + 1
                if typeCount == 1:
                    lines.append(f'v {cleanedString}')
                elif typeCount == 2:
                    try:
                        faces = cleanedString.split()
                        x = int(faces[0]) + 1
                        y = int(faces[1]) + 1
                        z = int(faces[2]) + 1
                        lines.append(f'f {x} {y} {z}')
                    except:
                        print("error")
            typeCount = 0

            doesExist = os.path.exists('models')
            if not doesExist:
                os.makedirs('models')
               
            with open(f'./models/{fileName}.obj', 'w') as f:
                for line in lines:
                    f.write(f'{line}\n')
    count += 1