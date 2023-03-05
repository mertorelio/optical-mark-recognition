import cv2
import numpy as np
import utlis1

#fotograf ozellikleri
heightImg = 300*4
widthImg  = 210*4
pathImage = "denemeler/100luk_numarali.jpg"
questions=20
choices=6

#cevap anahtarini dosyadan okuma ve sayiya cevirme
ans_abc = utlis1.read_answers("cevapanahtari.txt")
ans = utlis1.answers2numbers(ans_abc)

#perspektif islemleri icin cozunurluk
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
    #cevap siklari icin -************************************************************
    pts1 = np.float32(biggestContour) 
    pts2 = np.float32([[0, 0],[wrap_v, 0], [0, wrap_h],[wrap_v, wrap_h]]) 
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    imgWarpColored_1 = cv2.warpPerspective(img, matrix, (wrap_v, wrap_h))
    imgWarpGray_1 = cv2.cvtColor(imgWarpColored_1,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh_1 = cv2.threshold(imgWarpGray_1, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

    #second buyuk icin perspektif 
    secondContour=utlis1.reorder(secondContour)
    pts1_2 = np.float32(secondContour) # PREPARE POINTS FOR WARP
    pts2_2 = np.float32([[0, 0],[wrap_v, 0], [0, wrap_h],[wrap_v, wrap_h]]) # PREPARE POINTS FOR WARP
    matrix_2 = cv2.getPerspectiveTransform(pts1_2, pts2_2)
    imgWarpColored_2 = cv2.warpPerspective(img, matrix_2, (wrap_v, wrap_h))
    imgWarpGray_2 = cv2.cvtColor(imgWarpColored_2,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh_2 = cv2.threshold(imgWarpGray_2, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE
    
    
    #student id
    bubbles = utlis1.split_num(imgThresh_2, 10, 10)
    myPixelVal_2 = utlis1.pixelVal(10,10,bubbles)
    myPixelVal_2 = utlis1.id_reorder(myPixelVal_2)
    student_id = utlis1.id_answers(10,myPixelVal_2)
    #print(student_id)
    
    #soru kisimi
    column_3 = utlis1.splitColumn(imgThresh_1)
    boxes_1 = utlis1.splitBoxes(column_3[0])
    boxes_2 = utlis1.splitBoxes(column_3[1])
    boxes_3 = utlis1.splitBoxes(column_3[2])
    myPixelVal = utlis1.pixelVal(questions,choices,boxes_1)
    myIndex = utlis1.user_answers(questions,myPixelVal)
    grading, wrong_ans = utlis1.grading(ans,questions,myIndex)


imgBlank = np.zeros_like(img)
#out_thresh1 = imgThresh_1.r

resim_listesi = [imgThresh_1,imgThresh_2,imgBiggestContour,imgContours]

for i in range(0,len(resim_listesi)):
    cv2.imwrite(f"images/{i}.jpg",resim_listesi[i])


cv2.imshow("Stacked",imgBiggestContour)
cv2.waitKey(0)
