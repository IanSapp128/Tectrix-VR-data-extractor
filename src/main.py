import os

textureDict = {}
file1 = open('one', 'rb')
data = file1.readlines()
#Bitmap = bytes.fromhex('424DB4A7') - Old value
Bitmap = bytes.fromhex('424D')

count = 0

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
    count += 1