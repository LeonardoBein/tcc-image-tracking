from pathlib import Path
import random
from typing import Tuple
from uuid import uuid4
import cv2 as cv
import numpy as np
import argparse
from utils import mergeImages, ImageTransformer

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, help="image base", required=True)
ap.add_argument("-d", "--destination", type=str, help="image destination", required=True)
ap.add_argument("-n", type=str, help="repeat operation", default=1)
args = vars(ap.parse_args())

# config
here = Path(__file__).parent
config = {
    "pathResults" : Path(args['destination']),
    "pathImageTrackingResults" : here / "out/image_tracking/",
    "imageTrackings" : [
        here / "assets/image-tracking1.png",
        here / "assets/image-tracking2.png"
    ],
    "rangeZ" : (-45, 45),
    "rangeX" : (-45, 45),
    "rangeY" : (-45, 45),
}
# end config

imageBase = cv.imread(args['image'], cv.IMREAD_UNCHANGED)

def normalization(x, xMin, xMax):
    return (x - xMin) / (xMax - xMin)

def getImageTracking(
    imagePath: Path, imagePathSave: Path, deg: Tuple[int, int, int],
) -> cv.Mat:

    imageName =  str(imagePathSave)

    if not imagePathSave.parent.exists():
        imagePathSave.parent.mkdir(parents=True)

    if not imagePathSave.exists():
        it = ImageTransformer(str(imagePath))
        rotatedImg = it.rotateAlongAxis(phi=deg[0], theta=deg[1], gamma=deg[2])
        cv.imwrite(str(imagePathSave), rotatedImg)
        return rotatedImg
    
    return cv.imread(imageName, cv.IMREAD_UNCHANGED)

def run(imageBase: cv.Mat):
    global config

    y_shape, x_shape, _ = imageBase.shape

    areaUsed = np.zeros((imageBase.shape[0], imageBase.shape[1]))

    labels = []
    numberOfImages = random.randint(5, 15)

    for n in range(numberOfImages):
        index = random.randint(0, len(config["imageTrackings"]) - 1)
        
        labelName = str(index)
        imageTracking = config["imageTrackings"][index]

        degX = random.randint(config["rangeX"][0], config["rangeX"][1])
        degY = random.randint(config["rangeY"][0], config["rangeY"][1])
        degZ = random.randint(config["rangeZ"][0], config["rangeZ"][1])

        imageFile = config["pathImageTrackingResults"] / f"image{index}_z{degZ}/image{index}_z{degZ}_x{degX}_y{degY}.png"

        # phi=degY, theta=degX, gamma=degZ
        deg = (
            degY,
            degX,
            degZ,
        )

        imageTrackingMat = getImageTracking(imageTracking, imageFile, deg)

        size = random.randint(50, 100)

        brighter = random.randint(1, 100)

        intensity = np.ones(imageTrackingMat.shape, dtype='uint8') * brighter
        imageTrackingMat = cv.subtract(imageTrackingMat, intensity)

        position = [ random.randint(0, y_shape - size), random.randint(0, x_shape - size) ]

        areaPosition = np.zeros(areaUsed.shape)
        areaPosition[position[0]: position[0]+size, position[1]: position[1]+size] = 1

        while ( (areaPosition == 1) & (areaUsed == 1) ).any():
            position[0] = random.randint(0, y_shape - size)
            position[1] = random.randint(0, x_shape - size)
            areaPosition[:,:] = 0
            areaPosition[position[0]: position[0]+size, position[1]: position[1]+size] = 1
        
        imageBase = mergeImages(imageBase, imageTrackingMat, (size, size), position)
        areaUsed[position[0]: position[0]+size, position[1]: position[1]+size] = 1

        x_center = normalization( position[1] + size/2, 0, x_shape)
        y_center = normalization( position[0] + size/2, 0, y_shape)
        width = normalization(size, 0, x_shape)
        height = normalization(size, 0, y_shape)

        labels.append(f'{labelName} {x_center} {y_center} {width} {height}')


    hashString = str(uuid4())

    fileResultImage = config["pathResults"] / f"images/image-{hashString}.jpeg"
    fileResultLabel = config["pathResults"] / f"labels/image-{hashString}.txt"

    if not fileResultImage.parent.exists():
        fileResultImage.parent.mkdir()
    if not fileResultLabel.parent.exists():
        fileResultLabel.parent.mkdir()
    
    print(f"Created '{str(fileResultImage)}'")

    cv.imwrite(str(fileResultImage), imageBase)
    with open(str(fileResultLabel), 'w') as f:
        f.write("\n".join(labels))

if __name__ == "__main__":

    for i in range(int(args["n"])):
        run(imageBase)