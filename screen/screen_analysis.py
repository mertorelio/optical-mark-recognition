import streamlit as st 
import pandas as pd
import data_func
from data_func import DATASET_REPO_URL,DATA_FILENAME,DATA_FILE,HF_TOKEN



def screen_analysis_main():
    #repo, repo_df = data_func.pull_read()
    #ogrenci_no = st.text_input("Öğrenci No")
    #filtered_df = repo_df[(repo_df['sinif_no'] == 3) & (repo_df['not'] > 70)]
    dataFrame = pd.read_csv('temp.csv')
    


if __name__ == "__main__":
    screen_analysis_main()