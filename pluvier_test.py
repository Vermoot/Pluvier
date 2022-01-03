import sys
import json
from steno import Steno
from steno import Word

class TestPluvier: 

    one_syllabe_words = {
        "TAS" : "tasse",
        "PAU" : "puis",
        "KAUT" : "cuite",
#        "SUS" : "suce",
#        "S" : "ce",
        "WEU" : "vie",
        "WEUT" : "vite",
        "TEUP" : "type",
        "TPEUL" : "fil",
        "-TS" : "être",
        "PHAEB": "mienne",

    }
    i_words = {
        "RAPD" : "rapide",
        "TKWEUS" : "édifice",
        "TPORPL/TKABL" : "formidable",
        "APBLG/TEUFL" : "adjectif",
        "WEUS" : "vis",
        "WEUS*" : "visse",

#        "APBLG/OEUPBDZ": "adjoindre",
    }


    prefix_word = {
        "SPWAPBD" : "entende",
        "SPWAPBGS" : "intention",
        "R-/TPHRU": "reflux" ,
    }

    suffix_word = {
        "WHROUR" : "velours",
        "TPROEURD": "froideur",
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
        "PAB" : "panne",
        # -ne
#        "ATS/LO*EG" : "astrologue", 
        #    "HAER" : "hier",
        #    "TLOIK" : "technologique",
        #    "SLO*IG" : "psychologie",
        "PAER" : "pierre",
        "WHRUPL": "volume",
        "WHRUPL/TPHAO": "volumineux", #remove star ?!
    }

    right_ch_sound = {
        "AFRPB" : "arche",
        "TOFRPB" : "torche",
        "AFRPB/T*K" : "architecte",
        "PHAFRPBLG" : "manche",
#        "PWHRAFRPBLG" : "blanche",

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


    def test_lesson1_e_muet(self):
        self.assertSame(self.one_syllabe_words)

    
    def test_lesson2_p(self):
        self.assertSame({'PAP':'pape',
                         'SAP': 'sape',
                         'PAT': 'patte',
                         'PUS' : 'puce',
                         'TAP' : 'tape',
                         'PAS': 'passe'
                         })
    def test_lesson3_r(self):
        self.assertSame({'RA' : 'ras',
                         'RU' : 'rue',
                         'TRAP' : 'trappe',
                         'PART' : 'parte',
                         'STOR' : 'store',
                         'SORT' : 'sorte'
                      #   'RA*' : 'rat'
                         })

    def test_lesson4_w_f(self):
        self.assertSame({'WA' : 'va',
#                         'WU' : 'vue',
                         'WOT' : 'vote',
                         'RAF' : 'rave',
                         'SAF' : 'savent'
                         })
    def test_lesson4_ortho_star_verb(self):
        self.assertSame({'WOE*' : 'vaut', #star not in the right place
                         'WOE' : 'veau'
                         })

    def test_lesson5_K_L(self):
        self.assertSame({
            "K" : "que",
            "KAR" : "car",
            "KE" : "quai",
            "WAG" : "vague",
            "KOD" : "code",
            "ROEL": "rôle",
            "KOET": "côte",
#            "KOEUL": "colis", inversion
#            "KOEUP": "copie",
            "KOEUPB": "coin",
            "KOEUPBS": "coince",
                         })
    def test_lesson5_omittedIWords(self):
        self.assertSame(self.i_words)


    def test_lesson6_H_B(self):
        self.assertSame({'HOE' :'haut',
                         'HOET' : 'haute',
                         'HOT' : 'hotte',
                         'SOB' : 'sonne',
                         'PAB' : 'panne',
                         
                         })
    def test_lesson6_eu(self):
        self.assertSame({ 'SAO' : 'ceux',
                         'SAOL' : 'seul'
                         })

    def test_lesson7_G_D(self):
        self.assertSame({ "WAG" : "vague",
                          "KOD" : "code",
                          "RAG" : 'rage',
                          'SAG' : 'sage',
                          'ROUG' : 'rouge'

                         })

    def test_lesson7_AEU_ai(self):
        self.assertSame({ 'RAEU' : 'raie',
                          'TRAEU' : 'trait',
#                          'AEUD' : 'aide',
                          'SAEU*' : 'sait'
                         })

    def test_lesson8_Z(self):
        self.assertSame({'ROEZ' : 'rose',
                         'RAZ' : 'rase',
#                         'SAEUZ' : 'seize'
                         })

 #skip lesson 9 on numbers
    def test_lesson10_HR_for_L_BG_for_K_ending(self):
        self.assertSame({ 'HREUR' : 'lire',
                          'PHRABG' : 'plaque',
#                          'HRAEUS' : 'laisse'
                         })

    def test_prefixWords(self):
       for elem in self.prefix_word.items():
           assert elem[0] == self.steno(elem[1])


    def test_suffixWords(self):
        self.assertSame(self.suffix_word)

    def test_rightSound(self):
        self.assertSame(self.right_ch_sound)


    def assertSame(self, words):
        for elem in words.items():
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

            

