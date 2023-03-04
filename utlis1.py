import cv2
import numpy as np


## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


def rectContour(contours):
    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i) #alan hesabi
        #piksel alani 50den byukse gecerlidir
        if area > 30:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True) #kac tane koseye sahip oldugu
            if len(approx) == 4: #4 ise dortgendir
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True) #alanlari hesaplicak ve siralicak ki ona gore alanlari belirleyelim
    #print(len(rectCon))
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    #print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    #print(add)
    #print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

def splitBoxes(img):
    rows = np.vsplit(img,20) #vertical
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,6) #horizantal
        for box in cols:
            boxes.append(box)
    return boxes

def splitColumn(img):
    column = np.hsplit(img,3)
    
    return column

def grading(answers,num_questions,myAnswers):
    grading=[]
    for x in range(0,num_questions):
        if answers[x] == myAnswers[x]:
            grading.append(1)
        else:
            grading.append(0)
    score = (sum(grading)/num_questions)*100 
    return score

def user_answers(num_questions,myPixelVal):
    myIndex=[]
    for x in range (0,num_questions):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndex.append(myIndexVal[0][0])
    return myIndex
    
def pixelVal(num_questions,choices,box):
    countR=0 #rows
    countC=0 #column
    myPixelVal = np.zeros((num_questions,choices))
    for image in box:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC]= totalPixels
        countC += 1
        if (countC==choices):countC=0;countR +=1
    return myPixelVal