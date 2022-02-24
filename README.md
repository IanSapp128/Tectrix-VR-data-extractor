# Tectrix VR bike and climber data extractor

A python script to extract data from Tectrix VR Bike and Climber applications (**one** file).

Currently extracts textures and models from Tectrix VR Bike and Climber applications. This initial release focuses on the Sweeny Town application and it's **one** file (any language) and exports textures and models to .bmp and .obj. There are plans to support the other applications, but each of the Tectrix applications have their data stored differently so the script will have to have checks for which application is being read and adjust accordingly. If you would like to download the Tectrix VR bike applications they can be found in [this worldpack .iso file](http://tulrich.com/tectrixvr/download.html) or from these [CD rips on archive.org](https://archive.org/details/TectrixVR).

### To-Do

- ~~Model extraction to .obj~~ *This has been implemented.*
- Textured models *(Models are currenly not textured)*
- Terrain extraction to .obj
- Universal texture format for all applications
- Fix color pallet on some applications

Each one of the Tectrix VR bike applications have their data stored differently so the script will have to have checks for which application is being read and adjust accordingly.

### Known issues

Currently, some of the images are corrupt upon export due to the way the bytes are stored. An [issue request](https://github.com/IanSapp128/Tectrix-VR-data-extractor/issues/1#issue-1149829973) has been opened for this and I will look at it when I have more time.
