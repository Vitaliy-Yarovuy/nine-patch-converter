from __future__ import print_function
from PIL import Image
import sys
import getopt

Y = 1
X = 0


def get_pieces(data):
    # 'static' => true 'dynamic' => false
    tempDS = data[0][3] == 0
    tempPosition = 1
    returnPieces = []

    for position, point in enumerate(data):
        if position == 0:
            continue
        if tempDS != (point[3] == 0):
            tempWidth = position - tempPosition
            returnPieces.append([tempDS, tempPosition, tempWidth])
            tempDS = point[3] == 0
            tempPosition = position

    tempWidth = len(data) - tempPosition -1
    returnPieces.append([tempDS, tempPosition, tempWidth])

    return returnPieces


def get_fill_length(pieces, length):
    tempStaticLength = 0
    tempDynamicCount = 0

    for piece in pieces:
        # true => 'static'
        if piece[0] == True:
            tempStaticLength += piece[2]
        else:
            tempDynamicCount += 1

    fillWidth = (length - tempStaticLength)/tempDynamicCount

    return fillWidth


def draw_nine_patch(originImg, size):

    verticalPieces = get_pieces(originImg.crop((0, 0, 1, originImg.size[Y])).getdata())
    horizontalPieces = get_pieces(originImg.crop((0, 0, originImg.size[X], 1)).getdata())

    width = size[X]
    height = size[Y]


    fillHeight = get_fill_length(verticalPieces, height)
    fillWidth = get_fill_length(horizontalPieces, width)


    print(originImg.mode)


    destImg = Image.new("RGBA",size)



    tempX = 0
    tempY = 0
    for vPiece in verticalPieces:
        originY = vPiece[1]
        originHeight = vPiece[2]

        # true => 'static'
        if vPiece[0]:
            tempFillHeight = originHeight
        else:
            tempFillHeight = fillHeight

        tempX = 0
        if tempFillHeight != 0:
            for hPiece in horizontalPieces:
                originX = hPiece[1]
                originWidth = hPiece[2]

                # true => 'static'
                if hPiece[0]:
                    tempFillWidth = originWidth
                else:
                    tempFillWidth = fillWidth



                if tempFillWidth != 0:

                    # print("######################")
                    # print("position",(tempX,tempX))
                    # print("size origin",(originWidth,originHeight))
                    # print("size dest",(originWidth,originHeight))
                    # print("crop",(originX,originY,originWidth,originHeight))

                    cropImg = originImg.crop((originX,originY,originX + originWidth, originY + originHeight))
                    cropImg = cropImg.resize((tempFillWidth,tempFillHeight))
                    destImg.paste(cropImg, (tempX, tempY))

                    tempX += tempFillWidth

            tempY += tempFillHeight


    return destImg




optlist, args = getopt.getopt(sys.argv[1:], 'i:o:s:')
inputFile = './imgs/bkg.9.png'
outputFile = './imgs/bkg.png'
size = (640,1136)

for key,value in optlist:
        if key == "-i":
            inputFile = value
        elif key == "-o":
            outputFile = value
        elif key == "-s":
            size = [int(x) for x in value.split("x")]


print("input:",inputFile)
print("output:",outputFile)
print("size:",size)

destIgm = draw_nine_patch(Image.open(inputFile),size)

destIgm.save(outputFile,"PNG")



