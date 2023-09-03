# Tectrix VR bike data extractor

A small python script to extract data from Textrix VR Bike applications (one file).

Currently extracts textures from the Sweeny Town application's one file (any language) to .bmp. Manual extraction of model data has been achieved and will hopefully be automated in this script in the near future.

### To-Do

- Model extraction to .obj

- Terrain extraction to .obj

- Universal texture format for all applications

- Fix color pallet on some applications

Each one of the Textrix VR bike applications have their data stored differently so the script will have to have checks for which application is being read and adjust accordingly.

### Known issues

Currently, some of the images are corrupt upon export due to the way the bytes are stored. 
The latest push resolves almost all of the textures in Sweeny Town not working. Some are still broken, but
most are now exporting correctly. There seems to be a discrepancy with the byte sizes in the header.