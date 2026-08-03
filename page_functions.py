"""This module contains functions that handle streamlit page elements for the current session.

    Functions
    ---------
        **load_data(files) -> pandas.DataFrame**
            loads and concenates individual data files to a uniform term DataFrame (cached).
        **load_grid(rowlen) -> _Array[tuple[int, int], float64]**
            initialises array tracking stamped fields (cached).
        **load_stamp(file, zoom) -> OffsetImage**
            loads bingo stamp (cached).
        **load_start_date() -> str**
            loads current date and time as string for file naming.
        **load_start_time() -> float**
            loads current time.
        **refresh_check() -> None**
            displays dialog box checking in, if card should really be reloaded (with st.dialog).
        **check_bingo() -> None**
            checks and updates bingo count.
        **upload_terms() -> None**
            handles file upload to import terms as csv (with st.dialog).
        **export_image(fig) -> BufferedReader[_BufferedReaderStream]**
            exports current bingo card as png image.
        **clear_card_store() -> None**
            deletes all saved image files that are not currently relevant.

    Requirements
    ------------
    - streamlit
    - pandas
    - numpy
    - matplotlib
    - datetime
    - time
    - os
    - scipy
"""
##########################################################################################################################################################
## IMPORTS
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os

from matplotlib.offsetbox import OffsetImage
import scipy.ndimage as ndimage
from matplotlib.figure import Figure

##########################################################################################################################################################
@st.cache_data
def load_data(files:list[str]) -> pd.DataFrame:
    """Load and concenate individual data files to a uniform term DataFrame.

    Arguments
    ---------
        files (list[str]) : list of paths to data files 

    Returns
    -------
        data (pandas.DataFrame) : concatenated DataFrame
    """
    # Initialise DataFrame
    data = pd.DataFrame()
    for file in files:
        # Read file
        curr_data = pd.read_csv(file, header=None, delimiter=";", names=["terms", "comments"])
        # Add current data to overall DF
        data = pd.concat([data, curr_data])
    data["custom"] = 0
    return data


##########################################################################################################################################################
@st.cache_data
def load_grid(rowlen:int):
    """Initialise array tracking stamped fields.

    Arguments
    ---------
        rowlen      (int)   : number of fields making up one row of the card

    Returns
    -------
        start_grid (_Array[tuple[int, int], float64]) : description
    """   
    # Initialise start grid with 0
    start_grid = np.zeros((rowlen,rowlen))
    # Set FREE field as 1
    start_grid[rowlen//2,rowlen//2] = 1
    return start_grid


##########################################################################################################################################################
@st.cache_data
def load_stamp(file:str, zoom:float) -> OffsetImage:
    """Load bingo stamp.

    Arguments
    ---------
        file    (str)      : file path for stamp image
        zoom    (float)    : zoom factor for OffsetImage

    Returns
    -------
        (OffsetImage) : stamp in format that can be added to plot as artist
    """
    # Load image as array
    arr_img = plt.imread(file)
    # Rotate image (45°)
    arr_img = ndimage.rotate(arr_img, 45, reshape=True)
    # Define as OffsetImage (can be added to plot as artist)
    return OffsetImage(arr_img, zoom=zoom)


##########################################################################################################################################################
def load_start_date() -> str:
    """Load current date and time as string for file naming.

    Returns
    -------
        (str) : current date and time as string
    """
    return datetime.today().strftime("%d-%m-%Y_%H-%M-%s")


##########################################################################################################################################################
def load_start_time() -> float:
    """Load current time.

    Returns
    -------
        (float) : current time
    """
    return time.time()


##########################################################################################################################################################
@st.dialog("Bist du dir sicher, dass du eine neue Karte erstellen möchtest?")
def refresh_check() -> None:
    """Display dialog box checking in, if card should really be reloaded."""
    if st.button("neue Karte"):
        # Refresh page
        st.session_state.confirmed_refresh = True
        st.rerun()
    # Give user opportunity to cancel operation
    if st.button("Abbrechen", type="primary"):
        st.rerun()


##########################################################################################################################################################
def check_bingo() -> None:
    """Check and update bingo count to infer reaction."""
    # Initialise check list
    row_checks = []
    # Add sum of game rows
    row_checks.extend(sum(st.session_state.game))
    # Add sum of game columns
    row_checks.extend(sum(st.session_state.game.T))
    # Add sum of game diagonals
    row_checks.extend([sum([st.session_state.game[i,i] for i in range(0,len(st.session_state.game))])])
    row_checks.extend([sum([st.session_state.game[i,j] for i, j in enumerate(range(len(st.session_state.game)-1,-1,-1))])])
    # If at least one bingo is present
    if 5 in row_checks:
        # Initialise counter
        five_count = 0
        for s in row_checks:
            if s == 5:
                # Update counter for every bingo
                five_count = five_count +1
        if st.session_state.bingo_count < five_count:
            # New bingo
            st.session_state.new_bingo = True
            # Update session state
            st.session_state.bingo_count = five_count
            st.rerun()
        elif st.session_state.bingo_count > five_count:
            # Update bingo count (less than before)
            st.session_state.bingo_count = five_count
            st.rerun()
    else:
        # Less bingos than before
        if st.session_state.bingo_count > 0:
            # Update session state
            st.session_state.bingo_count = 0
            st.rerun()


##########################################################################################################################################################
@st.dialog("Bitte lade eine csv-Datei mit Begriffen hoch:")
def upload_terms() -> None:
    """Handle file upload to import terms as csv."""
    # Initialise file uploader instance
    file = st.file_uploader(
        label="Datei hochladen",
        type="csv",
    )
    # If a file has been uploaded
    if file:
        # Read terms into session state
        st.session_state.bingo_terms = pd.read_csv(file, index_col=0)
        # Refresh page
        st.session_state.confirmed_refresh = True
        st.session_state.uploaded_terms = True
        st.rerun()


##########################################################################################################################################################
def export_image(fig:Figure):
    """Export current bingo card as png image.

    Arguments
    ---------
        fig (matplotlib.Figure) : description (default=)

    Returns
    -------
        (BufferedReader[_BufferedReaderStream]) : description
    """
    # Set background colour black
    fig.patch.set_facecolor("black")
    # Initialise file name for export
    savepath = f"{st.session_state.bingo_card}_export.png"
    # Save figure as image
    fig.savefig(savepath)
    # Revert fig background
    fig.patch.set_facecolor("none")
    return open(savepath, "rb")


##########################################################################################################################################################
def clear_card_store() -> None:
    """Delete all saved image files that are not currently relevant."""
    cards = sorted(os.listdir("Bingo_Card"))
    images = [c for c in cards if (st.session_state.userID in c) & ("png" in c)]
    terms = [c for c in cards if (st.session_state.userID in c) & ("png" not in c)]
    if len(images) > 2:
        for filename in images + terms:
            # Get file in directory
            file_path = os.path.join("Bingo_Card", filename)
            # Check if it is a file (not a subdirectory & not the currently relevant one
            if (os.path.isfile(file_path)) & (datetime.today().strftime("%d-%m-%Y") not in file_path):
                os.remove(file_path)


##########################################################################################################################################################
def get_previous_cards():
    cards = sorted(os.listdir("Bingo_Card"))
    terms = [c for c in cards if (st.session_state.userID in c) & ("csv" in c)]
    return [term.split(".csv")[0] for term in terms]
    # if len(terms) > 1:
    #     return str(os.path.join("Bingo_Card",terms[-2].split(".csv")[0]))
    # elif len(terms) > 0:
    #     return str(os.path.join("Bingo_Card",terms[-1].split(".csv")[0]))
    # else:
    #     return None


##########################################################################################################################################################
def set_previous_card():
    st.session_state.set_prev = True
    st.session_state.confirmed_refresh = True


##########################################################################################################################################################
@st.dialog("Login :)", width="small", dismissible=False, icon=None)
def test_login():
    st.session_state.userID = st.multiselect(
        label="User",
        placeholder = "Wer bist du???", 
        options = ["Mama & Papa", "Maria & Ansgar"], 
        max_selections=1, 
        accept_new_options=False,
        label_visibility="collapsed",
    )
    if st.session_state.userID:
        st.session_state.userID = st.session_state.userID[0].replace(" ", "_")
        st.rerun()