import streamlit as st
import pandas as pd
import data_func
from data_func import DATASET_REPO_URL,DATA_FILENAME,DATA_FILE,HF_TOKEN


def screen_note_main():
    repo, repo_df = data_func.pull_read()

    st.subheader("Girilen Veriler")
    st.dataframe(repo_df,use_container_width=True)
    #filtered_df = repo_df[(repo_df['sinif_no'] == 3) & (repo_df['not'] > 70)]
        
if __name__ == "__main__":
    screen_note_main()