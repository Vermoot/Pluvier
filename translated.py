import sys
import copy
import re
from log import Log
from cutword import Cutword
from word import Word

class Translated:
        prefix=''
        suffix= ''
        def __init__(self,word, prefix, suffix):
            self.word = word
            self.prefix = prefix
            self.suffix = suffix
        def __str__(self):
                return self.prefix

        def generate(self) :
                mylist = []
                for cutword in self.suffixes():
                        newcut=Cutword(self.phoneme)
                        newcut.set_remains(self.remains)
                        newcut.set_replaced_by(self.replace, sound)
                        mylist.append(newcut)
                return mylist

        def set_remains(self, remains):
                self.remains=remains
                return self
        def set_replaced_by(self, replace,by):
                self.replace=replace
                self.steno=by
                self.found=True
                return self
        
        def steno(self) :
                return self.steno

