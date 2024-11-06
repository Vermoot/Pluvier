import sys
import re
import numpy as np
import json

from copy import copy, deepcopy

from src.steno import Steno
from src.word import Word

class Dictionary:

    picked = []
    words = []

    source = "resources/LexiqueMixtebyfreqfilms.csv"
    def read_corpus(self):
        words = []
        first_line = True
        with open(self.source) as f:
            corpus = f.readlines()
            
            for line in corpus:
                if first_line:
                    first_line = False
                    continue
                entry = line.split("\t")
                word = Word(
                    word = entry[0],
                    phonetics = entry[1],
                    lemme = entry[2],
                    cgram = entry[3],
                    cgramortho = entry[4],
                    genre = entry[5],
                    number = entry[6],
                    info_verb = entry[7],
                    syll = entry[8],
                    orthosyll = entry[9]
                )
                words.append(word)
                
        return words
