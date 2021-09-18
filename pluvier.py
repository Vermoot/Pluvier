import sys

class Word:
        def __init__(self, word, phonetics, lemme, cgram, genre, number, info_verb, syll):
            self.word = word
            self.phonetics = phonetics
            self.lemme = lemme
            self.cgram = cgram
            self.genre = genre
            self.number = number
            self.info_verb = info_verb
            self.syll = syll.split("-")

source = sys.argv[1]
corpus = []

with open(source) as f:
    corpus = f.readlines()

words = []
for line in corpus:
   entry = line.split("\t")
   word = Word(word = entry[0],
               phonetics = entry[1],
               lemme = entry[2],
               cgram = entry[3],
               genre = entry[4],
               number = entry[5],
               info_verb = entry[10],
               syll = entry[22],
               )
   words.append(word)

for word in words:
    if "inf" in word.info_verb:
        print(word.syll)
