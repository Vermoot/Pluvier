import sys
import json
from steno import Steno
from steno import Word

class TestPluvier: 

    one_syllabe_words = {
        "TAS" : "tasse",
        "PAU" : "puis",
        "KAUT" : "cuite",
        "SUS" : "suce",
        "S" : "ce",
        "WEU" : "vie",
        "WEUT" : "vite",
        "TEUP" : "type",
        "K" : "que",
        "KAR" : "car",
        "KE" : "quai",
        "WAG" : "vague",
        "KOD" : "code",
        "TPEUL" : "fil"

    }
    i_words = {
        "RAPD" : "rapide",
        "TKWEUS" : "édifice",
        "TPORPL/TKABL" : "formidable",
        "APBLG/TEUFL" : "adjectif",
#        "APBLG/OEUPBDZ": "adjoindre",
    }


    prefix_word = {
        "SPWAPBD" : "entende",
        "SPWAPBGS" : "intention",
        "R-/TPHRU": "reflux" ,
    }

    suffix_word = {
        "WLOUR" : "velours",
        #    "WLOEFS" : "voulez-vous"
        "PWAER" : "bière",
        "PAE" : "pied",
        "RAOD/HRO*EUS" : "radiologiste",
        "SPWOUZ/KWRAFPL" : "enthousiasme",
        "SPWOUZ/KWRA*S" : "enthousiaste",
        "AFRS" : "avoir",
        "POUFRS" : "pouvoir" ,
        "RURL" : "rural",
        "WEURL" : "viral",
        "KOFRBL" : "comble",
        "PAPBGS" : "pension",
        "TERBL" : "terrible",
        "THR-PLT" : "tellement",
        #    "ATS/LO*EG" : "astrologue", marche pas mauvaise casse des syllabes
        #    "HAER" : "hier",
        #    "TLOIK" : "technologique",
        #    "SLO*IG" : "psychologie",
    "PAER" : "pierre",
    }

    right_ch_sound = {
        "AFRPB" : "arche",
        "TOFRPB" : "torche",
        "AFRPB/T*K" : "architecte",
        "PHAFRPBLG" : "manche",
        "PWHRAFRPBLG" : "blanche",

#        "SKHRAEU": "chalet",
#        "SKWAL" : "cheval",
    }


    def read_corpus(self):
        words = []
        source = "resources/Lexique383.tsv"
        with open(source) as f:
            corpus = f.readlines()


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
        return words


    def setup_method(self, test_method):
        self.corpus = self.read_corpus()


    def steno(self,word):
        self.steno_class=Steno(self.corpus)
        return self.steno_class.transform(word)

    
    def test_oneSyllabeWords(self):
        for elem in self.one_syllabe_words.items():
            assert elem[0] == self.steno(elem[1])

    def test_omittedIWords(self):
       for elem in self.i_words.items():
           assert elem[0] == self.steno(elem[1])

    def test_prefixWords(self):
       for elem in self.prefix_word.items():
           assert elem[0] == self.steno(elem[1])


    def test_suffixWords(self):
       for elem in self.suffix_word.items():
           assert elem[0] == self.steno(elem[1])

    def test_rightSound(self):
       for elem in self.right_ch_sound.items():
           assert elem[0] == self.steno(elem[1])

        
    def all_tao_entry(self):
        with open('resources/tao_la_salle.json') as json_file:
            data = json.load(json_file)
        found = []
        not_found = []
        for elem in data.items():
            if elem[0] == self.steno(elem[1]):
                found.append(elem[1])
            else:
                not_found.append(elem[1])

        print("FOUND: ",found)
        print("\nNOT FOUND: ",not_found)
        assert false

            

