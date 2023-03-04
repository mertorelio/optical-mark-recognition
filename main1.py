import cv2
import numpy as np
import utlis1

#fotograf ozellikleri
heightImg = 300*4
widthImg  = 210*4
pathImage = "denemeler/bossikli.jpg"
questions=20
choices=6
ans= [2,3,2,1,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
wrap_h = 18*20
wrap_v = 18*20

#fotonun okunmasi ------------------------------------------------------------------------------------------------
img = cv2.imread(pathImage)
img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
imgBiggestContour = img.copy()
imgFinal = img.copy()
imgContours = img.copy()
imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) 

#donusumler---------------------------------------------------------------------------------
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 

#CONTOURS-------------------------------------------------------
contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS

#dortgen bulma--------------------------------------------------
rectCon = utlis1.rectContour(contours) 
biggestContour = utlis1.getCornerPoints(rectCon[0])
secondContour = utlis1.getCornerPoints(rectCon[1])
thirdContour = utlis1.getCornerPoints(rectCon[2])
fourthContour = utlis1.getCornerPoints(rectCon[3])

#main
if biggestContour.size != 0 and secondContour.size != 0:
    
    cv2.drawContours(imgBiggestContour, biggestContour,-1,(0,255,0),20) 
    cv2.drawContours(imgBiggestContour, secondContour,-1,(255,0,0),20) #sondk' kalinlik ortada renk 
    cv2.drawContours(imgBiggestContour, thirdContour,-1,(0,0,255),20) #sondk' kalinlik ortada renk 
    cv2.drawContours(imgBiggestContour, fourthContour,-1,(0,0,20),20) #sondk' kalinlik ortada renk 
    
    biggestContour=utlis1.reorder(biggestContour)
    secondContour=utlis1.reorder(secondContour)
    
    pts1 = np.float32(biggestContour) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[wrap_v, 0], [0, wrap_h],[wrap_v, wrap_h]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (wrap_v, wrap_h))
    
    #second buyuk icin perspektif 
    #pts1_s = np.float32(secondContour) # PREPARE POINTS FOR WARP
    #pts2_s = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    #matrix_s = cv2.getPerspectiveTransform(pts1_s, pts2_s)
    #imgWarpColored_s = cv2.warpPerspective(img, matrix_s, (widthImg, heightImg))

    # APPLY THRESHOLD
    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

    #kutularabolme
    
    column_3 = utlis1.splitColumn(imgThresh)
    boxes_1 = utlis1.splitBoxes(column_3[1])
    #print(len(boxes_1))
    #cv2.imshow("" , boxes_1[2])
        
    myPixelVal = utlis1.pixelVal(questions,choices,boxes_1)
    myIndex = utlis1.user_answers(questions,myPixelVal)
    grading = utlis1.grading(ans,questions,myIndex)
    print(grading)


imgBlank = np.zeros_like(img)

imageArray = ([imgGray,imgCanny],
          [imgContours, imgBiggestContour])

imgStacked = utlis1.stackImages(imageArray,0.5)
cv2.imshow("Stacked",imgStacked
cv2.waitKey(0)
