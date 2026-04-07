import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time


from matplotlib.offsetbox import OffsetImage
import scipy.ndimage as ndimage

######################################################################################
@st.cache_data
def load_data(files):
    data = []
    for file in files:
        curr_data = pd.read_csv(file, header=None)
        data = data + [curr_data.iloc[i, 0] for i in curr_data.index]
    return data

@st.cache_data
def load_grid(rowlen):
    start_grid = np.zeros((rowlen,rowlen))
    start_grid[rowlen//2,rowlen//2] = 1
    return start_grid

@st.cache_data
def load_stamp(file, zoom):
    arr_img = plt.imread(file)
    arr_img = ndimage.rotate(arr_img, 45, reshape=True)
    return OffsetImage(arr_img, zoom=zoom)

def load_start_date():
    return datetime.today().strftime("%d-%m-%Y_%H-%M-%s")

def load_start_time():
    return time.time()
######################################################################################
@st.dialog("Bist du dir sicher, dass du eine neue Karte erstellen möchtest?")
def refresh_check():
    if st.button("neue Karte"):
        st.session_state.confirmed_refresh = True
        st.rerun()
    # Give user opportunity to cancel operation
    if st.button("Abbrechen", type="primary"):
        st.rerun()

######################################################################################
def check_bingo():
    row_checks = []
    row_checks.extend(sum(st.session_state.game))
    row_checks.extend(sum(st.session_state.game.T))
    row_checks.extend([sum([st.session_state.game[i,i] for i in range(0,len(st.session_state.game))])])
    row_checks.extend([sum([st.session_state.game[i,j] for i, j in enumerate(range(len(st.session_state.game)-1,-1,-1))])])
    if 5 in row_checks:
        five_count = 0
        for s in row_checks:
            if s == 5:
                five_count = five_count +1
        
        if st.session_state.bingo_count < five_count:
            st.session_state.new_bingo = True
            st.session_state.bingo_count = five_count
            st.rerun()
        elif st.session_state.bingo_count > five_count:
            st.session_state.bingo_count = five_count
            st.rerun()
    else:
        if st.session_state.bingo_count > 0:
            st.session_state.bingo_count = 0
            st.rerun()


######################################################################################
@st.dialog("Bitte lade eine csv-Datei mit Begriffen hoch:")
def upload_terms():
    file = st.file_uploader(
        label="Datei hochladen",
        type="csv",
    )
    if file:
        curr_data = pd.read_csv(file, index_col=0)
        st.session_state.bingo_terms = [curr_data.iloc[i, 0] for i in curr_data.index]
        st.session_state.confirmed_refresh = True
        st.session_state.uploaded_terms = True
        st.rerun()

######################################################################################
def export_image(fig):
    fig.patch.set_facecolor("white")
    savepath = f"{st.session_state.bingo_card.split(".")[0]}_export.png"
    fig.savefig(savepath)
    fig.patch.set_facecolor("none")
    return open(savepath, "rb")
######################################################################################