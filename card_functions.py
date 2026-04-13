import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox
import numpy as np
import random
from datetime import datetime
import streamlit as st

def get_card_terms(rowlen, terms, custom_terms, excluded_terms):
    if (len(custom_terms) == 0) & (len(excluded_terms) == 0):
        bingo_terms = random.sample(terms, rowlen * rowlen -1) 
    else:
        if len(excluded_terms) != 0:
            remaining_terms = [i for i in terms if i not in excluded_terms]
        else:
            remaining_terms = terms.copy()
        if len(custom_terms) != 0:
            random_terms = random.sample([i for i in remaining_terms if i not in custom_terms], rowlen * rowlen - (len(custom_terms)+1))
            bingo_terms = random_terms + custom_terms
        else:
            bingo_terms = random.sample(remaining_terms, (rowlen * rowlen) - 1)
        random.shuffle(bingo_terms)
    # Insert "Free" in the center
    bingo_terms.insert((rowlen * rowlen) // 2, "FREE")
    return bingo_terms

######################################################################
def split_term(word, max_chars):
    if len(word) > max_chars:
        penalty = 0
        words = word.split(" ")
        longest_word = max([len(w) for w in words])

        if longest_word > max_chars:
            lw = [[idx, w] for idx, w in enumerate(words) if len(w) > max_chars]
            shift = [0*i for i in range(0,len(words))]
            for w in lw:
                if len(w[1]) > max_chars:
                    if "/" in w[1]:
                        w[1] = w[1].replace("/", "/ ", 1).split(" ", maxsplit=1)
                    elif "-" in w[1]:
                        w[1] = w[1].replace("-", "- ", 1).split(" ", maxsplit=1)
                    else:
                        penalty = max(len(w[1]) - max_chars, 0)
                        w[1] = [w[1]]
                
                if w[0] == 0:
                    shift[0] = len(w[1])-1
                    w[1].extend(words[1:])
                    words = w[1]
                else:
                    shift[w[0]] = len(w[1])-1
                    prev_shift = sum(shift[:w[0]])
                    words = words[:w[0]+prev_shift] + w[1] + words[w[0]+1+prev_shift:]

                    

        word_num = 1
        word_len = len(words[0])
        row_words = words[0]

        while word_num < len(words):
            if word_len + len(words[word_num]) < max_chars:
                word_len = word_len + len(words[word_num]) + 1
                row_words = row_words + " " + words[word_num]
                word_num = word_num + 1
            else:
                row_words = row_words + "\n" + words[word_num]
                word_len = len(words[word_num]) + 1
                word_num = word_num +1

        return row_words, penalty
    else:
        return word, 0

#########################################################################################################
def create_bingo_card(rowlen, bingo_terms):
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xticks(np.arange(0, rowlen + 1))
    ax.set_yticks(np.arange(0, rowlen + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='white', linewidth=1)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False, color="white")
    ax.spines[["top", "bottom", "left", "right"]].set_color("white")
    
    fig.patch.set_facecolor('none')
    ax.set_facecolor((0, 0, 0, 0.001))
    for i, word in enumerate(bingo_terms):
        x = (i % rowlen) + 0.5
        y = (i // rowlen) + 0.5

        word, penalty = split_term(word, 18)
        
        base_fontsize = 18 if word == "FREE" else 12
        fontsize = max(base_fontsize - penalty, 8)  # Set minimum fontsize
    
        ax.annotate(
            word,
            xy=(x, y),
            ha='center',
            va='center',
            fontsize=fontsize,
            fontweight='normal' if word == 'FREE' else 'normal',
            color="white",
            wrap=True
        )
    ax.add_artist(AnnotationBbox(st.session_state.stamp, (2.5, 2.5), xycoords='data', frameon=False, box_alignment=(0.5,0.5)))    
    plt.tight_layout()

    fig.savefig(st.session_state.bingo_card)
    return fig, ax

###################################################################################################
def update_bingo_card(fig, ax, xy, task):
    if task == "add":
        ax.add_artist(AnnotationBbox(st.session_state.stamp, xy, xycoords='data', frameon=False, box_alignment=(0.5,0.5)))
    elif task == "remove":
        xy_stuff = [[i, artist.xy] for i, artist in enumerate(ax.artists)]
        for present_xy in xy_stuff:
            if present_xy[1] == xy:
                ax.artists[present_xy[0]].remove()
    fig.savefig(st.session_state.bingo_card)
    return fig, ax

###################################################################################################
def add_custom_terms():
    st.session_state.custom_terms = st.session_state.custom_change
    for ct in st.session_state.custom_terms:
        if ct not in st.session_state.bingo_terms:
            st.session_state.confirmed_refresh = True

def remove_custom_terms():
    st.session_state.excluded_terms = st.session_state.exclusion_change
    for et in st.session_state.excluded_terms:
        if et in st.session_state.bingo_terms:
            st.session_state.confirmed_refresh = True