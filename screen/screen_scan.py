import csv
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import optic1
from functions import image_show
import pandas as pd 
from data_func import make_new_data,update

@st.cache
def convert_df_to_csv(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

def screen_scan_main():
    st.title("Optik Okuma")
    dataFrame = pd.read_csv('data/untitled.csv')
    sinif_kodu = int(st.text_input("Sınıf Kodu",value=10))
    ders_kodu = int(st.text_input("Ders Kodu",value=10))
    image_file = st.file_uploader(
        "Upload image for testing", type=['jpeg', 'png', 'jpg', 'webp'])
    #st.dataframe(dataFrame)
    
    if image_file != None:
        image = Image.open(image_file)
        image = np.array(image.convert('RGB'))
        
        
        
        if st.button("Işle ve Görüntüle"):
                #(ans_txt,pathImage, save_images= True)
                grading, wrong_ans, student_idFix, resim_list =optic1.optic1(ans_txt1="cevapanahtari/cevapanahtari_ders1.txt",
                                                                             ans_txt2="cevapanahtari/cevapanahtari_ders2.txt",
                                                                             ans_txt3="cevapanahtari/cevapanahtari_ders3.txt",
                                                                             pathImage=image,save_images=False) 

                image_show(resim_list)

                st.write("Notu:",grading[0])
                st.write("Yanlis Yaptigi sorular:",wrong_ans[0])
                st.write("Ogrenci Numarasi:",student_idFix)
                new_data = make_new_data(sinif_kodu=sinif_kodu,ders_kodu=ders_kodu, ogrenci_no=int(student_idFix),
                                     notu=grading[0],yanlislar=wrong_ans[0])
                    
       
        if st.button("Işle ve Kaydet"):
                #(ans_txt,pathImage, save_images= True)
                grading, wrong_ans, student_idFix, resim_list =optic1.optic1(ans_txt1="cevapanahtari/cevapanahtari_ders1.txt",
                                                                             ans_txt2="cevapanahtari/cevapanahtari_ders2.txt",
                                                                             ans_txt3="cevapanahtari/cevapanahtari_ders3.txt",
                                                                             pathImage=image,save_images=False) 

                #image_show(resim_list)
                st.write("Notu:",grading[0])
                st.write("Yanlis Yaptigi sorular:",wrong_ans[0])
                st.write("Ogrenci Numarasi:",student_idFix)
                new_data = make_new_data(sinif_kodu=sinif_kodu,ders_kodu=ders_kodu, ogrenci_no=int(student_idFix),
                                     notu=grading[0],yanlislar=wrong_ans[0])
            
                st.dataframe(new_data)
                updated = update(new_data=new_data,ex_df=dataFrame)
                #st.dataframe(updated,use_container_width=True)
                updated.to_csv("data/untitled.csv",index=False)
            
                st.download_button(label="Download data as CSV",data=convert_df_to_csv(updated),
                               file_name='large_df.csv',mime='text/csv',)        
            
#python -m streamlit run app.py
if __name__ == '__main__':
    screen_scan_main()	   