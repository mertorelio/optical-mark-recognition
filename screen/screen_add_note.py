import streamlit as st
import pandas as pd
import data_func
from data_func import DATASET_REPO_URL,DATA_FILENAME,DATA_FILE,HF_TOKEN




def screen_add_main():
    st.title("Not Giris")
    repo, repo_df = data_func.pull_read()
    # Kullanıcıdan verileri alma
    sinif_kodu = st.text_input("Sınıf Kodu")
    ogrenci_no = st.text_input("Öğrenci No")
    ders_kodu = st.text_input("Ders Kodu")
    notu = st.slider("Notu", 0, 100)
    yanlislar = st.text_input("Yanlış Sorulari (virgul ile ayirin)")
    yanlislar = str(yanlislar)
     
    if st.button("Veriyi Yukle"):
        new_data = data_func.make_new_data(sinif_kodu=sinif_kodu,
                                           ogrenci_no= ogrenci_no,
                                           ders_kodu= ders_kodu,
                                           notu=notu,
                                           yanlislar= yanlislar)
        updated_df = data_func.update(new_data,repo_df)
        data_func.save_and_push(updated_df,repo)
        st.subheader("Girilen Veriler")
        st.write(new_data)


if __name__ == "__main__":
    screen_add_main()

