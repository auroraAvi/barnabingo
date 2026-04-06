import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime

import card_functions as cf
import page_functions as pf
from streamlit_image_coordinates import streamlit_image_coordinates

#########################################################################################
# if not st.user.is_logged_in:
#     st.login()    # Show login dialogue
#     st.stop()  # Stop loading the application

# ### Load Application
# else:
st.set_page_config(
    page_title = "BARNABINGO",
    layout="wide"
)

grid_size = 5
data = pf.load_data(
    [
        "./data/dinge.csv",
        "./data/handlung_ermittlung.csv",
        "./data/handlung_fall.csv",
        "./data/handlung_sonstiges.csv",
        "./data/meta.csv",
        "./data/orte.csv",
        "./data/personen.csv",
        "./data/tatsachen.csv"
    ]
)
os.makedirs("Bingo_Card", exist_ok=True)

if 'game' not in st.session_state:
    st.session_state.file_name = pf.load_start_date()
    st.session_state.start_time = pf.load_start_time()
    st.session_state.custom_terms = []
    st.session_state.bingo_terms = cf.get_card_terms(grid_size, data, st.session_state.custom_terms)
    st.session_state.changed_ct = False
    st.session_state.stamp = pf.load_stamp("./data/mm_blue.png", 0.15)
    st.session_state.bingo_card = str(os.path.join("Bingo_Card", f"{pf.load_start_date()}-Bingo.png"))
    st.session_state.fig, st.session_state.ax = cf.create_bingo_card(grid_size, st.session_state.bingo_terms)
    st.session_state.confirmed_refresh = False
    st.session_state.last_click = 0
    st.session_state.bingo_count = 0
    st.session_state.new_bingo = False
    st.session_state.uploaded_terms = False
    st.session_state.game = pf.load_grid(grid_size)

if st.session_state.confirmed_refresh:
    st.session_state.stamp = pf.load_stamp("./data/mm_blue.png", 0.15)
    if st.session_state.uploaded_terms:
        st.session_state.uploaded_terms = False
    else:
        st.session_state.bingo_terms = cf.get_card_terms(grid_size, data, st.session_state.custom_terms)
    st.session_state.fig, st.session_state.ax = cf.create_bingo_card(grid_size, st.session_state.bingo_terms)
    st.session_state.confirmed_refresh = False
    st.session_state.game = pf.load_grid(grid_size)
    st.session_state.bingo_count = 0
    st.session_state.new_bingo = False
    st.rerun()

if st.session_state.new_bingo:
    st.balloons()
    st.session_state.new_bingo = False
#########################################################################################
st.markdown("<h1 style='color:black;font-size:350%;'>BARNABINGO</h1>", unsafe_allow_html=True)
#########################################################################################
with st.sidebar:
    st.header("Spezielle Begriffe")
    st.multiselect(
        label="",
        placeholder = "Wähle bis zu 4 Begriffe aus", 
        options = sorted(data), 
        max_selections=4,
        key="custom_change", 
        accept_new_options=False, 
        on_change=cf.add_custom_terms,
        label_visibility="collapsed"
    )
    if st.session_state.confirmed_refresh:
        st.rerun()
    st.divider()
    st.subheader("Neue Karte")
    st.button("Neue Karte erstellen", icon=":material/refresh:", on_click=pf.refresh_check)
    st.divider()
    st.subheader("Karte sichern")
    st.download_button(
        label="Begriffe sichern", 
        icon=":material/download:", 
        data= pd.DataFrame(st.session_state.bingo_terms).to_csv().encode("utf-8"),
        file_name="barnabingo_card.csv",
        on_click='ignore',
    )
    st.button(
        label= "Begriffe hochladen",
        icon = ":material/upload:",
        on_click= pf.upload_terms,
    )
    st.divider()
    st.subheader("Karte exportieren")
    st.download_button(
        label="Karte als Bild speichern",
        icon=":material/file_export:",
        data= pf.export_image(st.session_state.fig),
        file_name="card.png",
    )
click = streamlit_image_coordinates(st.session_state.bingo_card,  use_column_width=True)
if click:
    # New click
    if click["unix_time"] > st.session_state.last_click:
        # Update click time
        st.session_state.last_click = click["unix_time"]
        # Convert coordinates to grid slots
        click_x = [
            4 if click["x"] >= click["width"]/(125/99) else 
            3 if click["x"] >= click["width"]/(500/299) else 
            2 if click["x"] >= click["width"]/(250/101) else 
            1 if click["x"] >= click["width"]/(1000/209) else 
            0
        ]
        click_y = [
            0 if click["y"] >= click["height"]/(125/99) else 
            1 if click["y"] >= click["height"]/(500/299) else 
            2 if click["y"] >= click["height"]/(250/101) else 
            3 if click["y"] >= click["height"]/(1000/209) else 
            4
        ]
        # De-Select grid slot
        if st.session_state.game[click_x, click_y] == 1:
            st.session_state.fig, st.session_state.ax = cf.update_bingo_card(st.session_state.fig, st.session_state.ax, (click_x[0]+0.5, click_y[0]+0.5), "remove")
            st.session_state.game[click_x, click_y] = 0
        else:
            # Select grid slot
            st.session_state.fig, st.session_state.ax = cf.update_bingo_card(st.session_state.fig,st.session_state.ax, (click_x[0]+0.5, click_y[0]+0.5), "add")
            st.session_state.game[click_x, click_y] = 1
        st.rerun()

pf.check_bingo()
        
    