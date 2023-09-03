import os
import re
import sys

'''
Tectrix VR data extractor
2022-2023 Ian Sapp
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
        bmpList = []
        offsetList = []
        fileList = []

        for m in re.finditer(Bitmap, line):
            bmpList.append(m)

        for key, value in list(textureDict.items()):
            bmpBytes = str.encode(f' {key}.bmp')
            wdfBytes = str.encode(f' {key}.wdf')
            
            if bmpBytes in line or wdfBytes in line:
                fileList.append(key)

        if len(fileList) > 0:
            offset = line.index(Bitmap)        
            comboBytes = data[count]
            iterations = 50
            for i in range(1, 900):
                comboBytes += data[count + i]

            lastItem = fileList[-1]

            for item in fileList:
                byteSized = int(textureDict[item])

                # This code is not elegant at all, but it (kind of) works
                
                # Get the last item in the list
                if item != lastItem:
                    # Start with the offset
                    byteClean = comboBytes[offset:]
                    # Get all of the bytes between offset and the next instance of the Bitmap bytes
                    # Apparently the byte sizes in the header aren't accurate. The bytes will go all the way
                    # to the next instance of the bitmap header. This has resolved quite a few BMPs not rendering
                    # but there are still some that need work.
                    endOffset = comboBytes.find(Bitmap, offset + 1)
                    byteClean = byteClean[:endOffset]
                    doesExist = os.path.exists('textures')
                    if not doesExist:
                        os.makedirs('textures')
                    
                    outFile = open(f'./textures/{item}.bmp', 'wb')
                    outFile.write(bytes(byteClean))
                    outFile.close()
                    del textureDict[item]
                    offset = comboBytes.find(Bitmap, offset + 1)
                # If this is in fact the last item in the file list, just set the right slice
                # to the byte size given in the dictionary. Again, this is super sloppy but it
                # works for the most part.
                else:
                    byteClean = comboBytes[offset:]
                    byteClean = byteClean[:byteSized]
                    doesExist = os.path.exists('textures')
                    if not doesExist:
                        os.makedirs('textures')
                    
                    outFile = open(f'./textures/{item}.bmp', 'wb')
                    outFile.write(bytes(byteClean))
                    outFile.close()
                    del textureDict[item]
                    offset = comboBytes.find(Bitmap, offset + 1)
    
    if b'(dres' in line and b'(polygon' in line or  b'(geo' in line and b'(polygon' in line:
        if b'(dres' in line:
            result = re.search(b'\(dres(.*?)\(', line)
            bfileName = result.group(1).replace(b' ', b'')
            fileName = bfileName.decode('utf-8')
        elif b'(geo' in line:
            result = re.search(b'\(geo(.*?)\(', line)
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
                        pass
            typeCount = 0

            doesExist = os.path.exists('models')
            if not doesExist:
                os.makedirs('models')
               
            with open(f'./models/{fileName}.obj', 'w') as f:
                for line in lines:
                    f.write(f'{line}\n')
    count += 1