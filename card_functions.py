"""This module contains functions that create and modifiy the bingo cards.

Functions
---------
    **get_card_terms(rowlen, terms, custom_terms, excluded_terms) -> pandas.DataFrame**
        gets set of terms to build bingo card with.
    **split_terms(word, max_terms) -> tuple[str, int]**
        splits terms that exceed the maximum length to fit in field.
    **create_bingo_card(rowlen, bingo_terms) -> tuple[Figure, Axis]**
        creates the bingo card figure to be displayed as an image.
    **update_bingo_card -> output**
        description
    **add_custom_terms -> output**
        description
    **remove_custom_terms -> output**
        description

Requirements
------------
- matplotlib
- numpy
- random
- streamlit
- pandas
"""
##########################################################################################################################################################
## IMPORTS
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox
import numpy as np
import random
random.seed(random.random())
import streamlit as st
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axis import Axis
##########################################################################################################################################################
def get_card_terms(rowlen:int, terms:pd.DataFrame, custom_terms:list[str], excluded_terms:list[str]) -> pd.DataFrame:
    """Get set of terms to build bingo card with (entirely random or with custom terms added/removed).

    Arguments
    ---------
        rowlen          (int)               : number of fields making up one row of the card
        terms           (pandas.DataFrame)  : all possible terms
        custom_terms    (list[str])         : list of terms to include
        excluded_terms  (list[str])         : list of terms to exclude

    Returns
    -------
        bingo_data      (pandas.DataFrame)  : terms chosen for the current card
    """
    
    if (len(custom_terms) == 0) & (len(excluded_terms) == 0):
        # Randomly samle all terms (-1 for free field) if no customisation has been defined
        bingo_terms = random.sample(list(terms["terms"]), rowlen * rowlen -1) 
    else:
        if len(excluded_terms) != 0:
            # Filter out unwanted terms from overall pool
            remaining_terms = [i for i in terms["terms"] if i not in excluded_terms]
        else:
            # Take all possible terms
            remaining_terms = terms["terms"].copy()
        if len(custom_terms) != 0:
            # Only randomly sample the amount of unspecified terms
            random_terms = random.sample([i for i in remaining_terms if i not in custom_terms], rowlen * rowlen - (len(custom_terms)+1))
            # Add custom terms to pool
            bingo_terms = random_terms + custom_terms
        else:
            # Randomly sample from remaining terms (if only exclusion is set)
            bingo_terms = random.sample(remaining_terms, (rowlen * rowlen) - 1)
        # Shuffle terms
        random.shuffle(bingo_terms)
    # Get terms and descriptions for selected terms
    bingo_data = terms.loc[terms.terms.isin(bingo_terms)].reset_index(drop=True)
    # Insert "Free" in the center
    bingo_data.loc[(rowlen*rowlen)//2-0.5] = ["FREE", None]
    # Reindex to keep order after insertion
    bingo_data = bingo_data.sort_index().reset_index(drop=True)
    return bingo_data

##########################################################################################################################################################
def split_term(word:str, max_chars:int) -> tuple[str, int] :
    """ Splits terms that exceed the maximum length to fit inside the fields.

    Arguments
    ---------
        word        (str) : word to be checked for splitting
        max_chars   (int) : maximum characters for one line

    Returns
    -------
        row_words   (str) : split word
        penalty     (int) : font size penalty (to be subtracted from standard size)
    """
    # If term is too long
    if len(word) > max_chars:
        # Initialise penalty
        penalty = 0
        # Split term at whitespaces
        words = word.split(" ")
        # Get length of longest word in term
        longest_word = max([len(w) for w in words])
        # If longest word is too long
        if longest_word > max_chars:
            # Get too long words and index
            lw = [[idx, w] for idx, w in enumerate(words) if len(w) > max_chars]
            # Initialise shift array to keep track of word positions
            shift = [0*i for i in range(0,len(words))]
            # For every word exceeding the maximum
            for w in lw:
                if len(w[1]) > max_chars:
                    if "/" in w[1]:
                        # Split words divided by /
                        w[1] = w[1].replace("/", "/ ", 1).split(" ", maxsplit=1)
                    elif "-" in w[1]:
                        # Split words divided by -
                        w[1] = w[1].replace("-", "- ", 1).split(" ", maxsplit=1)
                    else:
                        # Set penalty according to word length
                        penalty = max(len(w[1]) - max_chars, 0)
                        # Reset word in its place (for consistency)
                        w[1] = [w[1]]
                
                # If first word was too long
                if w[0] == 0:
                    # Set shift based on word length
                    shift[0] = len(w[1])-1
                    # Add remaining words to first array element
                    w[1].extend(words[1:])
                    # Set first array element as term
                    words = w[1]
                else:
                    # Set shift based on word length
                    shift[w[0]] = len(w[1])-1
                    # Sum up previous shifts
                    prev_shift = sum(shift[:w[0]])
                    # Set previous words + current + following as term
                    words = words[:w[0]+prev_shift] + w[1] + words[w[0]+1+prev_shift:]
        
        # Initialse output structures
        word_num = 1 # counter
        word_len = len(words[0]) # number of words
        row_words = words[0] # saving bin
        
        while word_num < len(words):
            # If word combination is shorter than maximum
            if word_len + len(words[word_num]) < max_chars:
                # Sum word length (+ whitespace)
                word_len = word_len + len(words[word_num]) + 1
                # Join words
                row_words = row_words + " " + words[word_num]
                # Raise counter
                word_num = word_num + 1
            else:
                # Add linebreak between words
                row_words = row_words + "\n" + words[word_num]
                # Add linebreak to word count
                word_len = len(words[word_num]) + 1
                # Raise counter
                word_num = word_num +1
        # Return structured term + penalty
        return row_words, penalty
    else:
        # Return term as is
        return word, 0

##########################################################################################################################################################
def create_bingo_card(rowlen:int, bingo_terms:pd.Series) -> tuple[Figure, Axis]:
    """Create bingo card figure and save file to be displayed.

    Arguments
    ---------
        rowlen      (int)           : number of fields making up one row of the card
        bingo_terms (pandas.Series) : terms chosen for the current card

    Returns
    -------
        fig (matplotlib.Figure)     : created plot figure
        ax  (matplotlib.Axis)       : created plot axes
    """
    # Initialise figure and axis
    fig, ax = plt.subplots(figsize=(10,10))
    # Define tickspacing
    ax.set_xticks(np.arange(0, rowlen + 1))
    ax.set_yticks(np.arange(0, rowlen + 1))
    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # Insert grid
    ax.grid(color='white', linewidth=1)
    # Remove ticks
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False, color="white")
    # Add border
    ax.spines[["top", "bottom", "left", "right"]].set_color("white")
    # Remove background colour
    fig.patch.set_facecolor('none')
    ax.set_facecolor((0, 0, 0, 0.001))
    # For every term
    for i, word in enumerate(bingo_terms):
        # Define coordinates
        x = (i % rowlen) + 0.5
        y = (i // rowlen) + 0.5
        # Split terms that exceed a certain length
        word, penalty = split_term(word, 18)
        # Define base fontsize
        base_fontsize = 18 if word == "FREE" else 12
        # Set minimum fontsize
        fontsize = max(base_fontsize - penalty, 8)  
        # Write terms into plot
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
    # Add stamp to FREE field
    ax.add_artist(AnnotationBbox(st.session_state.stamp, (2.5, 2.5), xycoords='data', frameon=False, box_alignment=(0.5,0.5)))   
    # Set layout 
    plt.tight_layout()
    # Save figure as image file
    fig.savefig(st.session_state.bingo_card)
    return fig, ax

##########################################################################################################################################################
def update_bingo_card(fig, ax, xy, task):
    """ Explanation.

    Arguments
    ---------
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)

    Returns
    -------
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
    """
    if task == "add":
        ax.add_artist(AnnotationBbox(st.session_state.stamp, xy, xycoords='data', frameon=False, box_alignment=(0.5,0.5)))
    elif task == "remove":
        xy_stuff = [[i, artist.xy] for i, artist in enumerate(ax.artists)]
        for present_xy in xy_stuff:
            if present_xy[1] == xy:
                ax.artists[present_xy[0]].remove()
    fig.savefig(st.session_state.bingo_card)
    return fig, ax

##########################################################################################################################################################
def add_custom_terms():
    """ Explanation.

    Arguments
    ---------
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)

    Returns
    -------
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
    """
    st.session_state.custom_terms = st.session_state.custom_change
    for ct in st.session_state.custom_terms:
        if ct not in st.session_state.bingo_terms:
            st.session_state.confirmed_refresh = True
##########################################################################################################################################################
def remove_custom_terms():
    """ Explanation.

    Arguments
    ---------
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)
        arg (data-type, optionality) : description (default=)

    Returns
    -------
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
        out (data-type|data-type , optionality) : description
    """
    st.session_state.excluded_terms = st.session_state.exclusion_change
    for et in st.session_state.excluded_terms:
        if et in st.session_state.bingo_terms:
            st.session_state.confirmed_refresh = True