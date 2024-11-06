#!/usr/bin/python
# coding: utf-8
import sys
import re
import numpy as np
import json

from src.steno import Steno
from src.dicoverbs import Dico_Verbs
from src.word import Word


Dico_Verbs().generate()
