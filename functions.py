import cv2
import numpy as np
import streamlit as st 

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
    peri = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) #kose degerleri
    return approx


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) #fazla  koseliyi kaldiralim
    #print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) 
    add = myPoints.sum(1)
    #print(add)
    #print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

#siklari bolmek icin 20 tane soru vertical/ 5 tane isaret alani +1 tane soru sayisi yazan yer
#6 horizatanl bolmek
def splitBoxes(img):
    rows = np.vsplit(img,20) #vertical
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,6) #horizantal
        for box in cols:
            boxes.append(box)
    return boxes

#ogrenci numarasi alani icin ayni fonksiyonu kullandik 
#yuakrdakisini silip sadece bu da kullanilabilir dogru degerler ile
#ogrenci numarasi alani 0-9 arasi sayilardan 10 tane isaretleme yeri iceriyor
#10x10seklinde boleriz
def split_num(img,vertical, horizantal):
    rows = np.vsplit(img,vertical) #vertical
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,horizantal) #horizantal
        for box in cols:
            boxes.append(box)
    return boxes

#yan yana 3 tane birlesik ders alani oldugu icin onlari 3 ayri 
#sekle getiriyor
def splitColumn(img):
    column = np.hsplit(img,3)
    
    return column


#puan hesaplama alani
#soru sayisi dogru cevaplari ve ogrenci cevaplarini aliyor
#bunlari karsilastirip yeni bir listeye 1/0 seklinde kodluyor
#1ler toplanip puan hesaplanmis oluyor
def grading(answers,num_questions,myAnswers):
    grading=[]
    wrong_ans = []
    for x in range(0,num_questions):
        if answers[x] == myAnswers[x]:
            grading.append(1)
        else:
            grading.append(0)
            wrong_ans.append(x+1)
            if myAnswers[x]== 1:
                wrong_ans.append("A")
            if myAnswers[x]== 2:
                wrong_ans.append("B")
            if myAnswers[x]== 3:
                wrong_ans.append("C")
            if myAnswers[x]== 4:
                wrong_ans.append("D")
            if myAnswers[x]== 5:
                wrong_ans.append("E")
        
    score = (sum(grading)/num_questions)*100 
    return score ,wrong_ans

#piksel degerlerinde kullanici cevaplarini 
#okuyupu index seklinde listeye kaydediyor
def user_answers(num_questions,myPixelVal):
    myIndex=[]
    for x in range (0,num_questions):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndex.append(myIndexVal[0][0])
    return myIndex
    
#student id kismi yukardan asagiya dogru karsilastirma yaparak
#isretli alan tespit edilecegi icin satir ve sutunlari tekrar duzenlemiz gerekti
#[[1,2,3],[4,5,6],[7,8,9]] ----> [[1,4,7],[2,5,8],[3,6,9]]
def id_reorder(myPixelVal):
    duz_liste = []
    for sutun in range(len(myPixelVal[0])):
        for satir in range(len(myPixelVal)):
            duz_liste.append(myPixelVal[satir][sutun])
    yeni_liste = []
    satir = []
    for eleman in duz_liste:
        satir.append(eleman)
        if len(satir) == len(myPixelVal):
            yeni_liste.append(satir)
            satir = []
    return yeni_liste
                
#ogrenci numarasi kisminin piksel degerine gore hangisinin iseretli
#oldugunun tespiti    
def id_answers(vertical_num,myPixelVal):
    myIndex=[]
    for x in range (0,vertical_num):
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

#dosyadan cevap anahtarinin okunmasi
def read_answers(dosya_adi):
    with open(dosya_adi, 'r') as f:
        satirlar = f.readlines()

    okunan_veriler = []
    for satir in satirlar:
        sutunlar = satir.split()
        okunan_veriler.append(sutunlar[1])
        
    return okunan_veriler


#dosyadan okunan cevaplarin numerik hale getirilmesi
def answers2numbers(answers):
    num_answers = []
    for i in answers:
        if i == "a":
            num_answers.append(1)
        elif i == "b":
            num_answers.append(2)
        elif i == "c":
            num_answers.append(3)
        elif i == "d":
            num_answers.append(4)
        elif i == "e":
            num_answers.append(5)
        else:
            print("Oppss Check Txt file")
    return num_answers

   
def image_show(images):
    col1, col2, col3 = st.columns(3)
    with col1:
            st.header("0")
            st.image(images[0],width=200)
    with col2:
            st.header("1")
            st.image(images[1],width=200)
    with col3:
            st.header("2")
            st.image(images[2],width=200)
            
    col4, col5= st.columns(2)
    
    with col4:
            st.header("3")
            st.image(images[4],width=200)
    with col5:
            st.header("4")
            st.image(images[5],width=200)
    col6, col7= st.columns(2)
    with col6:
            st.header("5")
            st.image(images[6],width=200)
    
    with col7:
            st.header("6")
            st.image(images[7],width=200)
    