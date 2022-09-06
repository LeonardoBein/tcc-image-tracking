from pathlib import Path
import time
from utils import ImageTransformer, humanizeBytes, humanizeTime
import cv2 as cv
import glob
import numpy as np
import os
# import argparse

# ap = argparse.ArgumentParser()
# ap.add_argument("--rm", type=str, help="image base")
# ap.add_argument("-d", "--data", type=str, help="imagens para inserir")
# ap.add_argument("-s", "--save", type=str, help="diretorio para salvar o resultado")
# args = vars(ap.parse_args())



# config
here = Path(__file__).parent
pathResults = here / "out/"
imageTrackings = [
    here / "assets/image-tracking1.png",
    here / "assets/image-tracking2.png"
]
# end config


if not pathResults.exists():
    pathResults.mkdir()
else:
    files = glob.glob(str(pathResults / "*/*"))
    toRemoveString = input(f"to remove {len(files)} files: [N/s]")

    toRemove = True if toRemoveString.upper() == "S" else False
    if toRemove is True:
        for f in files:
            print(f"Remove: {f}")
            os.remove(f)

rangeZ = range(-90, 90)
rangeX = range(-90, 90)
rangeY = range(-90, 90)

totalFiles = 2 * (len(rangeX) * len(rangeZ) * len(rangeY))
totalSize = totalFiles * 25000
print(f"totalFiles={totalFiles}")
print(f"totalSize={humanizeBytes(totalSize)}")

pause = input(f"press enter to start process...")

indexFiles = 0
averageCreateFile = 0

for index, imagePath in enumerate(imageTrackings):
    it = ImageTransformer(str(imagePath))

    for degZ in rangeZ:
        imagePathSave = pathResults / f"image{index}_z{degZ}"

        if not imagePathSave.exists():
            imagePathSave.mkdir()

        for degX in rangeX:
            for degY in rangeY:
                start_time = time.time()
                rotatedImg = it.rotateAlongAxis(phi=degY, theta=degX, gamma=degZ)
                imageNameSave = str(imagePathSave / f"image{index}_z{degZ}_x{degX}_y{degY}.png")
                cv.imwrite(imageNameSave, rotatedImg)
                end_time = time.time()
                
                indexFiles += 1
                averageCreateFile = (averageCreateFile + float(end_time - start_time))/2

        percentComplete = np.round((indexFiles / totalFiles) * 100, 2)
        speedString = humanizeTime(averageCreateFile, 's')
        timeComplete = humanizeTime(averageCreateFile * (totalFiles - indexFiles), "s")
        print(f"Complete {percentComplete}%\tspeed={speedString}\ttimeComplete={timeComplete}")
        


        
