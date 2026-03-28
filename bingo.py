import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import card_functions as cf
import page_functions as pf
from streamlit_image_coordinates import streamlit_image_coordinates

#########################################################################################
st.set_page_config(
    page_title = "BARNABINGO",
    layout="wide"
)

grid_size = 5
img_size = 750
start_grid = pf.load_grid(grid_size)

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

if 'game' not in st.session_state:
    st.session_state.bingo_terms = cf.get_card_terms(grid_size, data)
    st.session_state.stamp = pf.load_stamp("./data/mm_blue.png", 0.15)
    st.session_state.bingo_card, st.session_state.fig, st.session_state.ax = cf.create_bingo_card(grid_size, st.session_state.bingo_terms)
    st.session_state.confirmed_refresh = False
    st.session_state.last_click = 0
    st.session_state.bingo_count = 0
    st.session_state.new_bingo = False
    st.session_state.game = pf.load_grid(grid_size)

if st.session_state.confirmed_refresh:
    st.session_state.stamp = pf.load_stamp("./data/mm_blue.png", 0.15)
    st.session_state.bingo_terms = cf.get_card_terms(grid_size, data)
    st.session_state.bingo_card, st.session_state.fig, st.session_state.ax = cf.create_bingo_card(grid_size, st.session_state.bingo_terms)
    st.session_state.confirmed_refresh = False
    st.session_state.game = start_grid
    st.session_state.bingo_count = 0
    st.session_state.new_bingo = False
    st.rerun()

if st.session_state.new_bingo:
    st.balloons()
    st.session_state.new_bingo = False
#########################################################################################
st.markdown("<h1 style='color:black;font-size:350%;'>BARNABINGO</h1>", unsafe_allow_html=True)
#########################################################################################
click = streamlit_image_coordinates(st.session_state.bingo_card, height=img_size, width=img_size)

if click:
    # New click
    if click["unix_time"] > st.session_state.last_click:
        # Update click time
        st.session_state.last_click = click["unix_time"]
        # Convert coordinates to grid slots
        click_x = [
            4 if click["x"] >= img_size/(125/99) else 
            3 if click["x"] >= img_size/(5/3) else 
            2 if click["x"] >= img_size/(250/101) else 
            1 if click["x"] >= img_size/(250/53) else 
            0
        ]
        click_y = [
            0 if click["y"] >= img_size/(125/99) else 
            1 if click["y"] >= img_size/(5/3) else 
            2 if click["y"] >= img_size/(250/101) else 
            3 if click["y"] >= img_size/(250/53) else 
            4
        ]
        # De-Select grid slot
        if st.session_state.game[click_x, click_y] == 1:
            st.session_state.fig, st.session_state.ax = cf.update_bingo_card(st.session_state.fig, st.session_state.ax, (click_x[0]+0.5, click_y[0]+0.5), "remove", st.session_state.bingo_card)
            st.session_state.game[click_x, click_y] = 0
        else:
            # Select grid slot
            st.session_state.fig, st.session_state.ax = cf.update_bingo_card(st.session_state.fig,st.session_state.ax, (click_x[0]+0.5, click_y[0]+0.5), "add", st.session_state.bingo_card)
            st.session_state.game[click_x, click_y] = 1
        st.rerun()

pf.check_bingo()
        

# # NEW CARD
# st.divider()
# b1, _, _ = st.columns(3)

# with b1:
#     st.button("Erstelle neue Karte", icon=":material/refresh:", on_click=pf.refresh_check)

##############################################################
# # BINGO GRID
# row1 = st.columns(5, width=1000)
# row2 = st.columns(5, width=1000)
# row3 = st.columns(5, width=1000)
# row4 = st.columns(5, width=1000)
# row5 = st.columns(5, width=1000)

# t = range(1,27) 
# j = 1
# for i, col in enumerate(row1 + row2 + row3 + row4 + row5):
#     with col.container(key=t[j], border=True, height=200, width=200, horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
#         if st.button(st.session_state.bingo_terms[i], type="tertiary", width="stretch"):
#             st.write("AHHH")
#         j = j+1