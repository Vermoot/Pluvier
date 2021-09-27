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

VOWELS = {
    "a": "A",       # chat
    "e": "E",       # clé
    "2": "AO",      # eux
    "9": "AO",      # seul
    "E": "AEU",     # père
    "i": "EU",      # lit
    "o": "OE",      # haut
    "O": "O",       # mort
    "y": "U",       # cru
    "u": "OU",      # mou
    # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

}

DIPHTONGS = {
    "8i": "AU",     # pluie
    "j2": "AOEU",   # vieux
    "je": "AE",     # pied
    "jE": "AE",     # hier  # TODO IN FRONT OF A CONSONANT
    "ja": "RA",     # cria
    "jo": "RO",     # bio
    "jO": "ROE",    # fjord # TODO unsure
    "jo": "AO",     # bio # TODO Some conflict there. "-R can be read as i" (above), but the diphtongs are more important I guess?
    "jO": "AO",     # fjord
    "j§": "AO",     # av_ion_
    "wa": "OEU",    # froid
    "w5": "OEUPB",  # loin
    "wi": "AOU",    # oui
    "j5": "AEPB",   # chien
    "ey": "EU",     # r_éu_nion
    "ya": "WA",     # suave
    "ij": "-LZ",    # bille # TODO Maybe not a diphtong, but a word ending/consonant thing
}

CONSONANTS_LHS = {
    "b": "PW",      # bonjour
    "d": "TK",      # dans
    "f": "TP",      # faire, phare
    "g": "TKPW",    # gare
    "k": "K",       # quoi, car
    "l": "HR",      # la
    "m": "PH",      # mais
    "n": "TPH",     # ne
    "p": "P",       # père
    "R": "R",       # rouge
    "s": "S",       # super
    "S": "SH",      # chien
    "t": "T",       # toi
    "v": "W",       # vous
    "8": "W",       # huit
    "j": "KWR",     # hier
    "z": "SWR",     # zone
    "Z": "SKWR",    # je
}

CONSONANT_PAIRS_LHS = {
    "gz": "KP",
    "ps": "S",
    "pn": "TPH",
    "tS": "SK",         # TODO: I'd rather deviate and use KH if possible
}

CONSONANTS_RHS = {
    "v": "F",
    "l": "L",
    "b": "B",
    "n": "B",
    "g": "G",
    "d": "D",
    "z": "Z",
    "k": "BG",
    "l": "FL",
    "m": "PL",
    "n": "PB",     # TODO This doubles the "n" = "B" from earlier. Might be in only certain pre-defined cases like AIB = "aine"
    "§": "*N",     # TODO Not really a consonant, but an ending nontheless?
    "Z": "G",
    "S": "FP",
    "N": "PG",
    "v": "F",
    "v": "F",

}

CONSONANT_PAIRS_RHS = {
    "tR": "TS",
    "st": "*S",
    "ks": "BGS",
    "bZ": "PBLG",
    "dZ": "PBLG",
    "sm": "FLP",
    "st": "*S",
    "bZ": "PBLG",
    "kR": "RBG",
    "vR": "FR",
    "fR": "FR",
    "rS": "FRPB",
    "kR": "RBG",
    "kR": "RBG",
    "kR": "RBG",
}

SOUNDS_RHS = {

}


# Here we build a list of Word objects from the corpus
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

# Here we start doing stuff with Word objects
syllables = []
for word in words:
    for syll in word.syll:
        syllables.append(syll)
print(len(set(syllables)))
print(set(syllables))
