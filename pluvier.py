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
    "5": "EUFR",    # vin
    # *N is used for "on" (§) endings. # TODO this is a vowel, but only on word endings

}

DIPHTONGS = {
    "8i": "AU",     # pluie
    "j2": "AOEU",   # vieux
    "je": "AE",     # pied
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
    "kw": "KW",
    "tS": "SK",         # TODO: I'd rather deviate and use KH if possible
}

SOUNDS_LHS = {
    "de": "STK",
    "def": "STKW",
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
    "l": "FL",      # TODO When is "l" FL or L?
    "m": "PL",
    "n": "PB",      # TODO This doubles the "n" = "B" from earlier. Might be in only certain pre-defined cases like AIB = "aine"
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
    "En": "AIB",
    "wan": "OIB",
    "jEn": "AEB",
    "win": "AOUB",
    "zj§": "GZ",
    "sj§": "GZ",
    "z§": "GZ",
    "sjOn": "GZ",   # TODO This might conflict with "zj§" just above. The rule says "either `-GS/*B` or `-GZ`*
    "zjOn": "GZ",
    "@b": "AFRB",   # jambe
    "5b": "EUFRB",  # limbe
    "§b": "OFRB",   # tombe
    "@bl": "AFRBL", # tremble
    "1bl": "EUFRBL",  # humble
    "§bl": "OFRBL",  # comble
    "@bR": "AFRBS",   # ambre
    "5bR": "EUFRBS",  # timbre
    "§bR": "OFRBS",   # ombre
    "@pR": "AFRPS",
    "5pR": "EUFRPS",
    "§pR": "OFRPS",
    "@sj§": "APBGS",    # p_ension_
    "5sj§": "EUPBGS",    # p_incions_
    "§sj§": "OPBGS",    # pron_oncions_
    "@ksj§": "APBGS",    # san_ction_
    "5ksj§": "EUPBGS",    # dist_inction_
    "§ksj§": "OPBGS",    # j_onction_
    "ksj§": "*BGS",     # a_ction_
    "isjOn": "EUGZ",
    "tR": "TS",
    "tER": "TS",
    "tyR": "TS",
    #  "Et": "*T",      # TODO: "Et" is covered by `AIT`, I don't get this. Maybe orthographic for "ette".
    "isjOn": "EUGZ",
    "isjOn": "EUGZ",
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

for word in words:
    if "@pR" in word.phonetics:
        print(word.word)
