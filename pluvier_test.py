import sys
import json
import inspect
import numpy as np
from src.steno import Steno
from src.steno import Word

class TestPluvier: 

    one_syllabe_words = {
        "TAS" : "tasse",

#        "SUS" : "suce",
#        "S" : "ce",
        "WEU" : "vie",
        "WEUT" : "vite",
        "TEUP" : "type",
        "TPEUL" : "fil",
#         "-TS" : "être",
        "PHAEB": "mienne",

    }
    i_words = {
        "W*EUS" : "visse",
        "RAPD" : "rapide",
#        "TKWEUS" : "édifice",
 #       "TPORPL/TKABL" : "formidable",
        "WEUS" : "vis",
#        "APBLG/OEUPBDZ": "adjoindre",
    }


    prefix_word = {
        "SPWAPBD" : "entende",
        "SPWAPBGS" : "intention",

    }

    suffix_word = {
        "WHROUR" : "velours",
        "TPROEURD": "froideur",
        #    "WLOEFS" : "voulez-vous"
#        "PWAER" : "bière", abbrev
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

    corpus = False
    def read_corpus(self):
        if self.corpus:
            return self.corpus
        print('read corpus')
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
                            cgramortho = entry[28],
                            genre = entry[4],
                            number = entry[5],
                            info_verb = entry[10],
                            syll = entry[22],
                            orthosyll = entry[27]
                            )
                words.append(word)
        return words


    def setup_method(self, test_method):
        self.corpus = self.read_corpus()


    def steno(self,word, force_verb = False):
        self.steno_class=Steno(self.corpus)
        self.steno_class.force_verb=False
        if force_verb:
            self.steno_class.force_verb = True
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
        self.assertSame({

            #'WA' : 'va', #contradiction lesson 19
#                         'WU' : 'vue',
                         'WOT' : 'vote',
                         'RAF' : 'rave',
#                         'SAF' : 'save'
                         })
    def test_lesson4_ortho_star_verb(self):
        self.assertSame({
            'WOE' : 'veau',
            'WO*E' : 'vaut', 
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
#            "KOEUPB": "coin",
#            "KOEUPBS": "coince",
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
#                          'TRAEU' : 'trait',
                          'AEUD' : 'aide',
#                          'SAEU*' : 'sait'
                         })

    def test_lesson8_Z(self):
        self.assertSame({

            'ROZ' : 'rose', # was ROEZ
            'RAZ' : 'rase',
            'SAEUZ' : 'seize'
        })

 #skip lesson 9 on numbers
    def test_lesson9_numbers(self):
        self.assertSame({
            #'TK' : 'deux',
                          'PHRABG' : 'plaque',
                          'HRAEUS' : 'laisse'
                         })

    def test_lesson10_HR_for_L_BG_for_K_ending(self):
        self.assertSame({ 'HREUR' : 'lire',
                          'PHRABG' : 'plaque',
                          'HRAEUS' : 'laisse'
                         })
        
    def test_lesson11_TK_for_d_FL_for_F(self):
        self.assertSame({ #'TK' : 'de',
                          'TKU' : 'du',
                          'TKOUT' : 'doute',
#                          'WEUFL' : 'vif',
#                          'WEUF' : 'vive'

                         })
        
    def test_lesson11_AU_for_ui(self):
        self.assertSame({ "PAU" : "puis",
                          "KAUT" : "cuite",
                          'KAUS' : 'cuisse',
                          'SAUFR' : 'suivre'
                         })
        
    def test_lesson11_AU_for_long_A(self):
        self.assertSame({ "PAUT" : "pâte",
                          "RAUP" : "râpe"
                         })

    def test_lesson12_PW_for_Binit_PL_for_Mfinal(self):
        self.assertSame({ # 'PWO' : 'beau',
#                          'PWOR' : 'bord',
                          'KAPL' : 'came',
#                          'AEUPL*' : 'aime'
                         })

    def test_lesson12_ortho_aSem_for_ieme(self):
        self.assertSame({'HAUT/A*EPL': 'huitième',
                         "SAEUZ/A*EPL": "seizième",
                         # should be "SAEUZ/A*EPL": "seizième",
                         })
        
    def test_lesson12_AOEU_for_ieu(self):
        self.assertSame({'WAOEU' : 'vieux',
                         'HRAOEU' : 'lieu',
#                         'AOEU' : 'yeux',
#                         'KRAOEU' : 'curieux' kur/aoeu
                         })


    def test_lesson12_ortho_rightR_infinitif(self):
        self.assertSame({'PARL/-R' : 'parler',
                         "SOUL/W-R" :"soulever",
                         "TW-R" : "tuer",
                         "TWED" : "tuée"
                         })

    def test_lesson12_ortho_rightD_passe_compose(self):
        self.assertSame({'PARL/-D' : 'parlé',
#                         'SU/-D' : 'sué'
                         },True)
        
    def test_lesson13_TP_for_F_init_PB_for_N_final(self):
        self.assertSame({"TPEUL": "fil",
                         "TPAUT": "fuite",
                         "TPRAEU": "frais",
 #                        "POPBT": "ponte",
                         "TOPB": "ton",
                         "TPOPB": "fond", 


                         })

    def test_lesson13_RE_prefix(self):
        self.assertSame({ #"R-/TPHRU": "reflux" ,
 #                         "R-FR": "refaire",
                          "R-L/WE": "relevé",
                          "R-LGS": "relation",
#                          "R-LT": "réalité",

                         }, False)

        
    def test_lesson13_AE_for_ie(self):
        self.assertSame({ "PAE" : "pied",
                          "HAER": "hier",
                          "SHRAR/AE":"salarié",
                          "SAEL" : "ciel",
                          "PAES": "pièce",
                          "TAERS": "tierce",
                         })

    def test_lesson13_AER_suffix_ier_iere(self):
        self.assertSame({"K-S/A*ER": "caissière",
                         "WOEUL/AER": "voilier",
                         "TE/A*ER": "théière",
                         })

    #TODO
    def test_lesson13_inversion_ses_son(self):
        return True 

    def test_lesson13_LEFT_R_can_be_read_as_i_infrontof_a_or_o(self):
        self.assertSame({ 
                          'TKRABL' : 'diable',
# conflit brioche            'WROL' : 'viol'
                         })

    # H- COTE gauche pour les groupement -> not to todo ?

    def test_lesson13_S_alone_for_imparfait(self):
        self.assertSame({"KRABG/-S": "craquais",
                         "PAS/-S": "passais",
                         "KOUR/-S": "courais",
                         })
        
    def test_lesson13_RS_alone_for_conditionnel(self):
        self.assertSame({
#            "TP-RS": "ferait",

                        "KRABG/-RS": "craquerait",
                         "KO*U/-RS": "courrait",
                         "PAS/-RS": "passerait",
                         })

    def test_new_stl_RAEU_alone_for_futur_simple(self):
        self.assertSame({
#            "TP-RS": "ferait",

                        "RAPBDZ/AEU": "rendrai",
#                         "KOU/-RS": "courrait",
                         "PAS/-RS": "passerait",
            
                         })

    def test_lesson13_AI_alone_for_nom_ai(self):
        self.assertSame({
            "TEUR/AEU": "tiret",
            "TEUR/-S": "tirais",
            "SORB/AEU": "sorbet",
            "TPEUL/AEU": "filet",
                         })
    def test_lesson13_G_alone_for_ant_participe_present(self):
        self.assertSame({"KREU/-G": "criant",
                         "SA/-G": "saillant",

 
 #                        "REU/-G": "riant",
                         "KOUR/-G": "courant",
                         })

    def test_lesson13_BLG_alone_for_quel(self):
        self.assertSame({
            "SEBLG": "séquelle",
            "HR-BLG": "lequel",
        })

        

    def test_lesson13_RP_for_peur_RL_for_leur(self):
        self.assertSame({"TRARP": "trappeur",
                         "RAURL" : "râleur"
 #                        "WRL": "voleur", #should be WORL ?
                         })

    def test_lesson14_PH_for_M_initial(self):
        self.assertSame({
                         "PHAOEU": "mieux",
                         "PHEUZ": "mise",
                         "PHARL": "malheur",
                         })

#    def test_lesson14_LG_for_la(self):
    def test_lesson14_OEU_for_oi_OEUN_for_oin(self):
        self.assertSame({
            "ROEU": "roi",
#            "PWOEU": "bois",
            #            "TPOEUPB": "foin",
#            "PWO*EUT": "boite",
                         })

    def test_lesson14_e_never_inside_word_and_star_for_re_suffix(self):
        self.assertSame({
#            "R-L/WE": "relevé",
            "TK-G/R*E": "degré",
#            "TKG/R*E": "degré",
#            "TKRE": "degré",
                         })

    def test_lesson14_star_N_for_ending_on(self):
        self.assertSame({
            "PH-L/*PB": "melon",
#            "PHOPB": "mon",
#            "PH-PB": "million",
                         })


    def wrong_lesson14_star_S_for_ste(self):
        self.assertSame({"P*EUS": "piste",
                         "HR*EUS": "liste",
                         })

    def test_lesson15_TPH_for_N_initial(self):
        self.assertSame({
#            "TPHU" : "nu",
            "TPHO*EU": "noie",
            "TPHOEU": "noix",
#            "TPHEUD" : "nid", TODO if exists put D
                         })

    def test_lesson15_GBS_for_final_X(self):
        self.assertSame({ "TPEUBGS": "fixe",
                          "TABGS": "taxe",
                         })

#    def test_lesson15_H_n_Negation(self):


    def test_lesson15_AOU_is_oui(self):
        self.assertSame({"AOU": "oui",
                         "TPAOUB": "fouine",
                         })

        
    def test_lesson15_ez_star_EZ_and_REZ_for_rez(self):
        self.assertSame({"TROUF/*EZ": "trouvez",
                         "PARL/*EZ": "parlez",
                         "PARL/R*EZ": "parlerez",
                         })

    def test_lesson16_KWR_for_y_and_G_for_j(self):
        self.assertSame({
#            "KWROT": "yacht", #mistake in lesson : kwrat
#            "KWRAT/US": "hiatus", #strange hier is not kwr...
            "PAG": "page",
            "PHARG": "marge", #'maRZ'
                         })


    def TODO_lesson16_conj_Y_for_il(self):
        self.assertSame({ 
                          "KWROEUD": "il doit",
                          "KWRAOF": "il veut",
                         })
        
    def test_lesson16_PBLG_for_dj_and_bj_median(self):
        self.assertSame({
            "APBLG/TEUFL" : "adjectif",
            "OPBLG/TEUFL": "objectif",
            "R-G": "rejet",
                         })

    def test_lesson17_SKWR_for_J_initial_and_SWR_for_Z_initial(self):
        self.assertSame({
#should be ?            "SKWR-L/-D": "gelé",
#           "SKWR-LD": "gelée",
 #           "SKWRL/-D": "gelé",
            "SKWROEUPB": "joint",
            "SWROUPL": "zoom",
#            "SKWRA*EUT": "jette",
                         })
#TODO ?
    def lesson17_nom_propre_ending_y_AO_star_E(self):
        self.assertSame({
            "HAR/AO*E": "Harry",
                         })

    def test_lesson17_final_ette_is_separate_star_T(self):
        self.assertSame({ "TOEUL/*T": "toilette",
                          "POPL/*T": "pommette",
                         })

    def test_lesson18_TKPW_for_sound_gue_initial_KW_for_qwe(self):
        self.assertSame({
            #"TKPWOU": "goût",
                         "TKPWAPB": "gant",
                         "TKPWAFL": "gaffe",
                         "AD/KWA": "adéquat",
                         "AD/KWAT": "adéquate",
                         })

    def test_lesson18_AIB_for_aine_sound(self):
        self.assertSame({
            "SAEUB": "saine",
            "TKPWAEUB": "gaine",
 #           "TKEUBGS/A*EUB": "dizaine",
#            "KEUPBZ/A*EUB": "quinzaine",
                         })

    def test_lesson19_KP_for_X_in_egz_sound_followed_by_woyel(self):
        self.assertSame({
            "KPEUL": "exil",
            "KPUT": "exécute",
            "KPEUG": "exige",
                          })

    def test_lesson19_W_is_we_sound(self):
        self.assertSame({

            "SWAEU": "souhait",
                         })

    def test_lesson19_starEB_ending_ene(self):
        self.assertSame({
            "SEUR/*EB": "sirène",
#            "KPEUG/*EB": "oxygène",
            
                         })

    def test_lesson19_WstarE_ending_ue_oue(self):
        self.assertSame({
            "AF/W*E": "avoué",
            "TKEUL/W*E": "dilué",
            "TRAPL/W*E": "tramway",
            #
                         },False)

    def test_lesson19_WstarEL_ending_uel(self):
        self.assertSame({
        "WEUZ/W*EL": "visuel",
        "TKPWRAD/W*EL": "graduel",
#                         "ABT/W*EL": "habituel",
                         })



    def test_lesson19_separate_starZ_ending_a_sound(self):
        self.assertSame({
#            "R-P/*Z": "repas",
            "SAG/A": "saga",
                         "SAG/*Z": "saga",
                         "KOUP/*Z": "coupa",
#                         "WOBGZ": "avocat",
#                         "WEUFR/*Z": "vivra",#removed i
                         })

    def test_lesson21_CH_init_is_SH_final_is_FP(self):
        self.assertSame({
 #           "SHAER": "cher",
                        "KAFP": "cache",
                       "SHOEU": "choix",
#            "SHO": "chaud",

                        "RUFP": "ruche",
    #        "SHE": "chez",

                         })
        
    def test_lesson21_starEL_el_ortho_final(self):
        self.assertSame({
#            "KRU/*EL": "cruel",
#            "K-PB/*EL": "conditionnel",
#           "K-PBL": "conditionnel",
            "TPEUS/*EL": "ficelle",
                         })

    def test_lesson21_RT_RTS_for_ortho_teur_trice(self):
        self.assertSame({
            "HRAEURT": "lecteur",
            "ARTS": "actrice", # ABG/*RTS
#            "HRAEUBG/RTS": "lectrice",
#            "HRAEURTS": "lectrice",
                         })

    def test_lesson22_B_is_final_ne(self):
        self.assertSame({
            "PWOB": "bonne",
            "SKWROEB": "jaune",
            "SKWRAOB": "jeune",
            "SKWRAOBS": "jeunesse",
        })


    def test_lesson22_AEN_ien_sound_AEB_for_ienne_sound_star_for_suffix(self):
        self.assertSame({"PHAEPB": "mien",
                         "PHAEB": "mienne",
                         "HRAEPB": "lien",

#                         "SWAEPB": "souvient",
#                         "KWA*EPB": "convient",
                         })

    def test_lesson22_AOUB_for_sound_ouine(self):
        self.assertSame({
            "TPAOUB": "fouine",
#            "STKPWAOUB": "égoïne",
                         })

    def test_lesson22_GZ_for_sound_zion_and_zon(self):
        self.assertSame({
#            "OGZ": "occasion",
            "TPUGZ": "fusion",
#            "SAEUGZ": "saison",
                         })

    def test_lesson23_natural_combo_initial_consonne(self):
        self.assertSame({
#            "STKPWOPB": "second",
#            "STPAEUR": "sphère", #'sfER'
            "STRAT": "strate",
            "STEUL": "style",
            "SKRUT": "scrute",
            "STRAT": "strate",
            "STEUL": "style",
            "SKRUT": "scrute",
            "SKOUR": "secours",
#            "SPHREUD": "splendide",
#            "SPH-": "semaine",
            "SPREUPBT": "sprint",
#            "SRA": "sera",
            "TKPWHRAS": "glace",
#            "TKPWREU": "gris", conflit avec agricole
            "TKREUPB": "drain", #'dR5'
#            "TPHRAOR": "fleur", #'fl9R'
#            "TPRAEUL": "frêle",#'fREl'
#            "TROU": "trou",
            "KHRAS": "classe",
            "KRAPB": "cran",
            "PWHROBG": "bloc",
            "PWREUPB": "brin",
            "PHRUPL": "plume",
            "PREUZ": "prise",
            "WHROUR": "velours",
            "WRAEU": "vrai",

                         })

    def test_lesson22_final_natural_consonnes(self):
        self.assertSame({
            "SOLD": "solde",
            "TORS": "torse",
            "TPORPL": "forme",
            "TKOUBL": "double", #'dubl'
            "TART": "tarte",
            "KARP": "carpe",
#            "KOFR": "coffre", 
            "KORB": "corne",
            "KULT": "culte",
            "KOPBT": "conte",
            "SOPBD": "sonde","PARBG": "parc",
            "PARL": "parle",
            "PABGT": "pacte",
            "PHORG": "morgue",
#            "HRAPS/R-R": "laps",
            "HROPBG": "longue",
            "SOUFL": "souffle",
            "HAEURB": "herbe",
#            "AFPT": "achète", # a-SEt
#             "ORPBLG": "orge", #'ORZ'
            "OPT": "opte", 
#            "APBL/W*E": "enlevé",


        })

    def test_lesson25_KH_for_sound_mne(self):
        self.assertSame({
            "KHAS": "menace", #m°-nas
            "KHU": "menu",
            "KAL/O/KHAER":"calomnier",
            "APB/KH-R": "emmener",
            "APB/PHL-R": "emmêler",
            
#            "KHAOR": "mineur",
            "KHUT": "minute",
            "KHAUZ/AER": "menuisier",
        })
        
    def test_lesson25_AE_for_starting_letter_a_word(self):
        self.assertSame({
#            "AE/WEUD": "avide",
            "AE/TKOR": "adore",
            "AE/TKAOEU": "adieu",
            "AE/PHORS": "amorce",
            "AE/TKOPT": "adopte",

            })

        #TODO  il y a et preposition lesson 26
    def test_lesson26_AEN_for_sound_ian(self):
        self.assertSame({
            "SAEPBS": "science", #'sj@s'
        })
        
    def test_lesson26_final_NS_for_ortho_ance_or_ence(self):
        self.assertSame({
#            "KROEUPBS": "croissance",
# should be            "SAURPBS": "assurance", but assumed is
            "AE/SURPBS" : "assurance",
            "SEURBG/OEPB/STAPBS" : "circonstance",
            "SPHREPBS": "suppléance",
            "STPRAPBS": "souffrance",


        })

        
    def test_lesson26_final_ND_for_ortho_ande(self):
        self.assertSame({
            "WEUPBD": "viande",
            "TPREUPBD": "friande",
#            "TPREUPBDZ": "friandise",
        })

    def test_lesson26_KT_for_ortho_cte(self):
        self.assertSame({
            "ABGT": "acte",
            "TKEUBGT": "dicte",
            "PABGT": "pacte",
            "TRABGT": "tract",
#            "KHRAEUBGT": "collecte",
        })
    def test_lesson26_KEOEN_for_prefix_con(self):
        self.assertSame({
#            "KOEPB/SAEPBS": "conscience",
            "KOEPB/KAF": "concave",
            "KOEPB/KHRUR": "conclure",
# ordre du slash            "KOEPB/TOUR": "contour",
        })            
    def test_lesson27_STK_for_starting_des_and_dec_following_by_woyel(self):
        self.assertSame({
#            "TKAEUS/*EUPB": "dessin",
            "STKEUR": "désir",
#            "STKAPBDZ": "descendre",
            "STKU": "dessus",
#            "STKOU": "dessous",
            "STKAEUR": "désert",
            #"STK*EUR": "désire",

        })
        
        
    def test_lesson27_DAOE_for_starting_ortho_de(self):
        self.assertSame({
            #"TKAOE/KOUDZ": "découdre",
#                         "TKAOE/KOFP/-R": "décocher",
#                         "TKAOE/PREPB": "déprend",
            #lesson 56
    
                         })
    def test_lesson27_ending_sounds_tre_ntre_rtre_dre_ndre_bre_rbre_pre_rpre(self):
        self.assertSame({
            "ATS": "astre",
#            "KOPBTS": "ncontre",
#            "REPBDZ": "rendre",
            "SOBS": "sobre",
            "PHARBS": "marbre",
            "POURPS": "pourpre",
#            "SHREUPBDZ": "cylindre",
            "SKWREUFR": "givre",
            "WEUTS": "vitre",
            "TARTS": "tartre",
            "PHOUDZ": "moudre",
            "PHORDZ": "mordre",
            "ARBS": "arbre",
            "PROPS": "propre",
            "HREUTS": "litre",
            "ORDZ": "ordre",
            "KADZ": "cadre",
        })
        
    def test_lesson28_Kstar_for_prefix_com_and_KM_for_comm(self):
        self.assertSame({
            # 2 ways to write KPAR
            "KPHAPBS/-D" : "commencé",
            "K*/PAR": "compare", #'k§-paR'
            "KPAR": "compare", #'k§-paR'
#            "K*/PHROE": "complot",
            "K*/PHRO": "complot",

 #           "KPHROE": "complot",
            "K*/PABGT": "compact",
            "K*/PWATS": "combattre",
#            "K*/PA*": "compas",
 #          "KPHEUBG": "communique",
            "KPH": "comme",
#            "KPHA": "comment",
            "KPHAEURS": "commerce",


        })

        
        
    def test_lesson28_FBG_for_sound_fic_and_fec(self):
        self.assertSame({"TRAFBG": "trafic",
#                         "AFBG/TE": "affecté"
                         })

        
    def test_lesson29_STPH_for_sound_sne(self):
        self.assertSame({
            "STPHOB": "snob",
            "STPHABG": "snack",
 #           "STPHEUPL": "synonyme",
#            "SPHA": "cinéma",
            "STPHEUTS": "sinistre",
 #           "STPHOPB": "sinon",
 
        })

    def test_lesson29_GSstarB_or_GZ_for_sound_tionne_and_zionne(self):
        self.assertSame({
            #"TPOPBGS": "fonction",
 #                        "STAGS/*B": "stationne",
            "STAGZ": "stationne",
 #                        "PAGS": "passion",
                         "PAGZ": "passionne",
 #                        "POEGZ": "positionne",
                         })
    def test_lesson29_GZ_for_sound_zion(self):
        self.assertSame({
            #"TKWEUGZ": "division",
                         "WEUGZ": "vision",
                         "TPUGZ": "fusion",
                #         "TPUGZ/*B": "fusionne",
                         })
    def test_lesson29_GS_for_cien_and_GZ_for_cienne(self):
        self.assertSame({
            "PHAG/EUGS": "magicien",
            "PHAG/EUGZ": "magicienne",
#            "POL/TEUGS": "politicien",
        })

        # test fail due to starting of word
    def test_lesson29_BGS_suffix_for_cation(self):
        self.assertSame({
 #           "EUD/TP*EUBGS": "identification",
#            "HRAGS": "location",
           "WEFRBGS": "vérification",
#        "KPHEUBGS": "communication",
                         })

    def test_lesson29_AO_for_diphtong_io(self):
        self.assertSame({
            "PWRAOFP": "brioche",
            "PHAOP": "myope",
            "PAOFP": "pioche",
#            "HRAOPB": "lion",
#            "KPHAOPB": "camion",

        })
    def test_lesson30_SPW_for_prefix_ent_int_end_ind(self):
        self.assertSame({
            "SPWAPBDZ": "entendre", 
            "SPWORS": "entorse",
            "SPWAPBT": "entente",
            "SPWAPBGS": "intention",
#            "SPWEUBG": "indique",
            "SPWUR": "endure",
#            "SPWRER": "entrer",
            "SPWREUG": "intrigue",
            "SPWAEPB": "indien",

        })

    def test_lesson30_SP_R_for_prefix_super_and_MULT_for_multi(self):
        self.assertSame({
#            "SP-R/TPHRU": "superflu",
#            "STPEUGS": "superficiel",
#            "PHULT/PHR*EU": "multiplie",
 #           "PHULT/TKPWREUPB": "multigrains",
            "PHULT/TPORPL": "multiforme"})
        
    def test_lesson30_INTS_for_prefix_inter(self):
        self.assertSame({
#            "EUPBTS/*D": "interdit",
    #        "EUPBTS/-DZ": "interdire",
     #       "SPWAEURD": "interdit",
            "SPWAEURDZ": "interdire"})
        
    def test_lesson30_W_for_F_initial(self):
        self.assertSame({"WHEU": "fini",
                         "WHEUS": "finisse",
                         "WHAL": "final",
                         "WHEUGS": "finition",
                         })
        
    def test_lesson30_I_for_y(self):
        self.assertSame({ "EU" : "y" })                    


    def test_lesson31_FT_for_ending_vite_or_cite(self):
        self.assertSame({ #"ABG/TEUFT": "activité",
                          "PAS/EUFT": "passivité",
            "EUPB/WAPBT/EUFT": "inventivité",
                      #     "EBG/TREUFT": "électricité",
                         })

    def test_lesson31_ending_RD_for_deur_RG_for_gueur_RN_for_neur_AOstarR_for_eur(self):
        self.assertSame({
            "TPROEURD": "froideur",
            "REURG": "rigueur",
            "ARD/AO*R": "ardeur",
            "STKEURD": "décideur",
#            "PWORPB": "bonheur",
            "WEURG": "vigueur",
        })

    def test_lesson31_rightW_is_F_after_SD(self):
        self.assertSame({"STKWOE": "défaut",
                         "STKWAPB": "défend",
                         "STKWOUL": "défoule",
                         "STKWAEURL": "déferle",
#                         "STKWEURB": "définir",

        })
    def test_lesson32_WHR_for_sound_vle(self):
        self.assertSame({
            "WHROUR": "velours",
#            "WHRAE": "vouliez",
            "WHROEUR": "vouloir",

        })
    def test_lesson32_sounds_FRB_mbe_FRBL_mble_FRBS_mbre_FRPS_mpre(self):
        self.assertSame({
            "TRAFRBL": "tremble",
            "TOFRB": "tombe",
#            "HREUFRB/R-R": "limbe",
            "PHAFRBS": "membre",
#            "KOFRBL": "comble",
            "PWOFRB": "bombe",
#            "TRAFRBL": "tremble",

            "TEUFRBS": "timbre",
            "PHROFRB": "plombe",
            "ROFRPS": "rompre",
            
        })
    def test_lesson32_suffix_starIFL_for_if_and_starIF_for_ive(self):
        self.assertSame({
            "PAS/*EUFL": "passif",
            "PHAS/*EUFL": "massif",
#            "PAS/*EUF": "passive",
#            "PHOT/*EUF": "motive",
 #           "PHOEUF": "motive",
            "SPORT/*EUF": "sportive",

        })

    def  test_lesson33_sounds_PBGS_ntion_and_onction_starBGS_ction_PBGSstarB_or_GZ_ntionne_and_nctionne_PBGSR_ntionner_IGZ_itionne(self):
        self.assertSame({
            "PHAPBGS": "mention",
            "TAPBGS": "tension",

            "PHAPBGZ": "mentionne",
#            "TPOPBGS/*B": "fonctionne",
#            "SPWAPBGS": "intention",
#            "TKEUS/TEUPBGS": "distinction",
#            "TPR*EUBGS": "friction",
#            "SATS/TPA*BGS": "satisfaction",

        }
                        )
        
    def test_lesson33_TS_sound_tre_taire_or_ture_starT_sound_ette_and_AstarAIR_ortho_aire_EBS_sound_ener(self):
        self.assertSame({
            "EBS/SKWREU": "énergie",
#            "TPHOTS": "notaire",
                "SUTS": "suture",
            "KREUTS": "critère",
            "TOEUL/*T": "toilette",
#            "TPHEURG": "énergie",
                "HRAEUTS": "lettre",
            "EPLTS": "émettre",
            "PAEURPLTS": "permettre", #my
            "WHAEUTS": "fenêtre",
            "WHROPBTS": "volontaire",

        })
    def test_lesson33_RGS_ending_rtion_or_ration(self):
        self.assertSame({"PORGS": "portion",
                         "ORPGS": "opération",
                         "APL/HRAORGS": "amélioration",
                         "HREUB/ERGS": "libération",
                         "PHOD/ERGS": "modération",
#                         "PHOD/RAGS": "modération",
#                         "SHRAB/RAGS": "élaboration",
#                         "RERGS": "rémunération",

        })        
    def test_lesson34_sounds_SW_swe_TW_twe_STW_stwe_DW_dwe_and_dve_FPL_sme(self):

        self.assertSame({
#            "SOEUPB": "soin",

 #??           "SWAR/E": "soirée",
           "SWAEU": "souhait",
            "SWAEUT": "souhaite",

#"TKWORS": "divorce",
#            "PORT/W*R": "portuaire",
            "PREUFPL": "prisme",
            "SARBG/AFPL": "sarcasme",
            #            "TPRUBG/TWAO*": "fructueux",

        })
    def test_lesson35_sounds_FRP_mpe_FRPL_mple_FRPT_mpte_PL_ple(self):
        self.assertSame({
            "RAFRPL/EUR": "remplir",
            "KAFRP": "campe",
# not in lexique :             "STAFRP": "étampe",
            "TRAFRP": "trempe",
            "TROFRP": "trompe",
            "SOUPL": "souple",
            "PROFRPT": "prompte",
            "TAFRP": "tempe",
            "HRAFRP": "lampe",
            "TKPWREUFRP": "grimpe",
            "TAFRPL": "temple",
 #           "AFRPL": "ample",
            "KOUPL": "couple",
            "POFRP": "pompe",

        })

    def test_lesson38_starL_suffixe_elle(self):
        self.assertSame({
#            "TKEPBLGTS": "dentelle",
#            "AT/*EL": "attelle",
            "HOELGTS": "hôtel",
            # have to resolve prefix /suffix proposition
            "KARLGTS": "cartel",
            "PHOLGTS": "motel",
            "PHORLGTS": "mortel",

        })
    def test_lesson38_RB_ending_cis_ci_rbe_and_rne(self):
        self.assertSame({
            "PHORB": "morne",
            "-FRB": "verne",
            "PRERB": "précis",
 #           "ARB": "assis",
            "WOEURB": "voici",
#            "STPEURB": "superficie",
            "PRERBZ": "précise",
#            "S-RB": "ceci",
#            "SKAEURB": "concerne",

            "PWORB": "borne",
            "PWARB": "barbe",

        })

    def test_lesson39_KOEN_starting_con(self):
        self.assertSame({
            "KOEPB/TAPB": "content",
#            "KOEPB/TAPBT": "contente",
        },False)
        
    def test_K_starting_con_2_ways_to_write(self):
        self.assertSame({
            "STAPB": "content",
            "KOEPB/TAPB": "content",
#            "KOPBT/APB": "content",
 
 #          "KOPBT/APBT": "contente",

            "KOEPB/TAPBT": "contente",
        },False)

    def test_lesson40_start_by_co_followed_by_rr_or_ll_then_o_omitted(self):
        self.assertSame({
#            "KROB/O*R": "corrobore",
            "KHROBG": "colloque",
            "KHRAEUBGT/*EUFL": "collectif",
#            "KRUPGS": "corruption",
#            "KR-BGT": "correct",
            "KHRAEUBGT": "collecte",

        })
    def test_lesson40_FL_sound_val_vail_vel(self):
        self.assertSame({
#            "AFL": "aval", or AEFL ??
            "TRAFL": "travail",
            "TPHOUFL": "nouvelle",
 #           "TRA*FL": "travaille",
        })

    def test_lesson40_EU_for_eu(self):
        self.assertSame({
#            "REUS/*EUR": "réussir",
            "REUS/EU": "réussi",
 #           "RAOPB": "réunion",

        })

#TODO
    def test_lesson40_inverted_words(self):
        self.assertSame({
#            "KOEUL": "colis",
 #           "SKWROEUL": "joli",
            "KOEUP": "copie",
            "TPOEUL": "folie",
        })

    def test_lesson41_PLT_for_sound_ment_FPLT_for_sound_vement(self):
        self.assertSame({
            "WRAEUPLT": "vraiment",
            "THR-PLT": "tellement",
#            "TKOPLT": "document",
#            "TKPW-PLT": "gouvernement",
            "WEUFPLT": "vivement",
            "TKPWRAFPLT": "gravement",
            "UBG/-PLT": "uniquement",

        })

    def test_lesson41_inverse_ending_word(self):
        self.assertSame({
            "TPHREUPL": "film",
#            "TKOPLT": "document",
#            "TKPW-PLT": "gouvernement",
            "PWHRUB": "bulbe",
            "WHRAF": "valve",
            "SEULG": "sigle",

        })

    def test_lesson41_RK_sound_cre_and_FRKS_for_ncre(self):
        self.assertSame({
#            "AURBG": "acre",
            "TPHARBG": "nacre",  
#            "AFRBGS": "ancre",
 #           "SKARBG": "consacre",
            "AFRBGS": "ancre",
            
           "KAFRBGS": "cancre",
#            "SARBG": "sacre",

        })

#    def test_lesson41_FR_infrontof_BGS_is_n(self):
#        self.assertSame({
#        })

    def test_lesson41_FRPB_sound_nqu_FRBLG_ncle(self):
        self.assertSame({
#            "KEPBT": "enquête",
#            "KPAOEU": "anxieux",
            "OFRBLG": "oncle",
 #           "EUFRBG/A*E": "inquiet",
#            "PET/OFRBG": "pétoncle", shoube : ?
            "PET/OFRBLG": "pétoncle",

        })
    def test_lesson41_FRLG_sound_ngl(self):
        #same pb upper transfor FR as n
        self.assertSame({
            "OFRLG": "ongle",
 #           "SKWRUFRLG": "jungle",
            "TREUFRLG": "tringle",
            "AFRLG": "angle",

        })

    def test_lesson42_NG_sound_ngue(self):
        self.assertSame({
            "HRAPBG": "langue",
 #           "TKEUS/TEUPBG": "distingue",
            "HROPBG": "longue",

        })

    def test_lesson42_PBLG_sound_final_nge(self):
        self.assertSame({
            "APBLG": "ange",
            "RAPBLG": "range",
            "HREUPBLG": "linge",
            "PHAPBLG": "mange",
            "HRAPBLG": "lange",

        })
        
    def test_lesson42_PG_final_sound_gne(self):
        self.assertSame({
            "PAEUPG": "peigne",
            "SEUPG": "signe",
            "SAEUPG": "saigne",
            "HREUPG": "ligne",
#            "PHAPG/TPEUBG": "magnifique",

        })

    def test_lesson43_endingFR_sound_fre_and_vre_FRB_sound_fer_vaire_erve(self):
        self.assertSame({
            "OFR": "offre",
            "HREUFR": "livre",
            "TKEUFR": "diffère",
            
#            "SFR-": "souffre",
#            "OFRB": "offert",
            "TRAFRB": "travers",
            "EUFR": "ivre",
            "WEUFR": "vivre",
            "SOUFR": "soufre",
            "KOUFRB": "couvert",
#            "WAEUFRB": "verve",
#            "AFRB": "arrive",
#            "UFRB": "univers",
            "KOUFR": "couvre",
            "TKEUFRBS": "diverse",

            })

    def test_lesson43_TRANS_prefix_trans(self):
        self.assertSame({
            "TRAPBS/PEUR": "transpire",
#            "TR*EUT": "transite",
            "TRAPBS/PAEURS": "transperce",


            })

    def test_lesson44_final_FRPB_sound_rche(self):
        self.assertSame({
#            "AFRPB": "arche",
   #         "TOFRPB": "torche",
#            "AFRPB/*EUF": "archives",
            "PHAFRPB": "marche",
#            "AFRPB/T*BG": "architecte",
            "TPOUFRPB": "fourche",


            })

    def test_lesson44_final_FRPB_sound_anche(self):
        self.assertSame({
#            "HAFRPBLG": "hanche",
#            "PHAFRPBLG/*T": "manchette",
            "TRAFRPBLG": "tranche",
            "TPRAFRPBLG": "franche", 
            "PHAFRPBLG": "manche",
#            "PWHRAFRPBLG": "blanche",
 #           "TKPWREUFRPBLG/AO*": "grincheux",
 #           "SPAFRPBLG/-R": "épancher",
 #           "HRUFRPBLG": "lunch",
# TODO nch transfo voyelles
            })


    def test_TODO_lesson44_SRAGS_sound_ciation(self):
        self.assertSame({
#            "AORBGS": "association",
 #           "EUB/EUGS": "initial",
 #           "TPHEGS": "négociation",


            })

    def test_lesson45_ending_ITD_ite_LT_ilite_BT_bite_BLT_bilite(self):
        self.assertSame({
#            "K-PBT": "quantité",
            "AELGT": "égalité",
#            "PROBT": "probité",
            "TKWALT": "dualité",
            "HUPL/EULT": "humilité",
#            "ROBLT": "responsabilité",
            "PROBLT": "probabilité",
 #           "POBLT": "possibilité",

            })

    def test_lesson45_WA_sound_ua(self):
        self.assertSame({
 #           "STWAGS": "situation",
#            "TPHRUBG/TWAGS": "fluctuation",
            "PHAPBS/WALT": "mensualité",
            })

    def test_lesson46_ending_RL_rural_BL_bla_ble_RBL_rbal_rible_RT_rite(self):
        self.assertSame({
            "RURL": "rural",
#            "TKPWHROBL": "global",
            "PHURL": "mural",
            "WEURL": "viral",
            "WAEURBL": "verbal",
#            "RABL": "raisonnable",
#            "ORBL": "honorable",
#            "HOR/*EUBL": "horrible",
            "WAEURBL": "verbal",

#            "PRAORT": "priorité",
 #           "SKURT": "sécurité",
  #          "OBS/KURT": "obscurité",


            })


    def test_lesson47_GS_sound_gr_BS_sound_bre(self):
        self.assertSame({
            "AGS/KOL": "agricole",
#            "AGS/KURT": "agriculteur",
#            "AGS/TPHOPL": "agronome",
            "ABS/WRAGS": "abréviation",


            })

    def test_lesson47_FRS_ending_voir(self):
        self.assertSame({
            "AFRS": "avoir",
#            "R-FRS": "revoir",
            "POUFRS": "pouvoir",
            "SAFRS": "savoir",


            })
#todo : 
    def test_todo_lesson47_DAOEZ_for_starting_des_not_followed_by_steno_woyel(self):
        self.assertSame({
 #           "STKHREUBS": "déséquilibre",
#           "TKAOEZ/SPWEG/R*E": "désintégré",
            "STKARPL": "désarme",
            "TKAOEZ/KHREUBS": "déséquilibre",

            })

    def test_lesson48_KWR_for_i_followed_by_woyel_inside_word(self):
        self.assertSame({
            "SPWOUZ/KWRA*S": "enthousiaste",
 #           "WR*EU": "varie",
 #           "WRAGS": "variation",
 #           "AZ/KWRAEUBG": "asiatique",
            })


    def test_lesson48_GT_ending_th(self):
        self.assertSame({
            "PHEUGT": "mythe",
            })

    def test_lesson49_LOstarEG_logue_LOstarIG_logie_LOstarIS_logiste_LOstarIK_logique(self):
        self.assertSame({
            "RAOD/HRO*EUS" : "radiologiste",
#           "PWHROEUG": "biologie",
 #           "SHRO*EUBG": "psychologique",
 #           "TPHAOP/HRO*EG": "pneumologue",
            })

    def test_lesson49_LGS_ending_lation(self):
        self.assertSame({
            "R-LGS": "relation",
#            "WROLGS": "violation",
            })

    def test_lesson50_LZ_sound_ille_RLZ_sound_reille(self):
        self.assertSame({
            "HABLZ": "habille",
#            "AEUG/AULZ": "aiguille",
            "AB/AEULZ": "abeille",
            "PWEULZ": "bille",
            "TPEULZ": "fille",
#            "ORLZ": "oreille",
            "SAOLZ": "seuil",
            "PALZ": "paille",
            })


    def test_lesson51_NL_for_nl_nal(self):
        self.assertSame({
#            "TPHRAEUF": "enlève",
#            "APBL/W*E": "enlevé",
            "PWAPBL": "banal",
            "KAPBL": "canal",
            "PWRAPBL": "branle",


            })

    def test_lesson51_RBL_for_rnl_OstarEX_pluriel_aux_(self):
        self.assertSame({
#            "SKWROURB/O*EBGS": "journaux",
            "SKWROURBL": "journal",
            "TABL/O*EBGS": "tableaux",
            "PHAPBT/O*EBGS": "manteaux",
#            "POT/O*EBGS": "poteaux",


            })

    def test_lesson51_STstarE_ending_site(self):
        self.assertSame({
#en            "UFRB/ST*E": "université",
            "TKEUFRB/ST*E" :"diversité",
    #        "TKWAEURS/EUTD": "diversité",


            })

    def test_lesson51_WH_start_fin_fen(self):
        self.assertSame({
            "WHAL": "final",
            "WHOULZ": "fenouil",
            "WHAEUTS": "fenêtre",


            })


    def test_lesson52_PGS_sound_ption_pation(self):
        self.assertSame({
#            "PRAOUPGS": "préoccupation",
            "OPGS": "option",
            "OPGS/*EL": "optionnel",
#            "EUPBS/KREUPGS": "inscription",
#            "STKREUPGS": "description",
            "KRUPGS": "corruption",
#            "TKAOE/SAEUPGS": "déception",


            })

    def test_lesson52_S_sound_ps_stl_modified(self):
        self.assertSame({
 #            "SHRO*EG": "psychologue",
#            "SAOD/TPHEUPL": "pseudonyme",
# should be in tao :           "SEUFP/*EUBG": "psychique",
             "SEUFP/EUBG": "psychique",
 #           "SHRO*EUG": "psychologie",
#            "SKRATS": "psychiatre",


            })

    def test_lesson4_N_sound_pn(self):
        self.assertSame({
            "TPHAO": "pneu",
#            "TPHAOP/HRO*EG": "p bienneumologue",
#            "TPHAOP/HRO*EUG": "pneumologie",


            })

    def test_lesson53_TH_sound_ten(self):
        self.assertSame({
            "THAS": "tenace",
            "THU": "tenu",
            "THEUS": "tennis",
            "THAFT": "ténacité",
            "THALZ": "tenaille",
            "TH-G": "tenant"
            })


    def test_lesson53_VH_sound_ven(self):
        self.assertSame({
#            "WHEUPL/A*O": "venimeux",
#            "WHA*EZ": "veniez",
 #           "WHAEUGS": "vinaigre",

            "WHEUPB": "venin",
            "WHU": "venu",
            "EPB/WHEUPL": "envenime",
            "APB/WEU": "envie",

            })

    def test_lesson53_PG_sound_gne(self):
        self.assertSame({
#            "TOEUPG/-R": "témoigner",
            "SEUPG": "signe",
            "APG/OE": "agneau",
            "AB/OE": "anneau",

            "SEUPG/AL": "signal"
#            "SHAEL": "signal",

#            "SHATS": "signature",
#            "SEUPG/TP*EU": "signifie",


            })

    def test_lesson54_KP_sound_exce_exci(self):
        self.assertSame({
            "KPAEUPGS": "exception",

 #           "KPAEUS/*EUFL": "excessif",

  #          "KPEBG/RA*BL": "exécrable",
            "KPAEUL": "excelle",
            "KPEUGZ": "excision",
            "KPEUT": "exit",
#            "KP*EUT": "excite",


            }, False)

    def test_lesson54_BGS_start_ex_follow_by_consonne(self):
        self.assertSame({
            "-BGS/PAPBGS": "expansion",
#            "-BGS/PEU/-R": "expier",
            "-BGS/TEURP/-R": "extirper",
#            "-BGS/KWAGS": "excavation",
            })


#TODO     def test_lesson54_AIBGS_prefi_ex(self): ex-employe ...


    def test_lesson55_s_infrontof_c_or_p_can_be_omitted(self):
        self.assertSame({
            "AEUBG/HRAER": "escalier",

            "AEUP/OEUR": "espoir",
            # "AEUP/*ER": "espère",
            # "SPOEUR": "espoir",
            # "SUP/AEU": "suspect",
            # "SPAEU": "suspect",

            # "SPER": "espère",
            #             "SKALD": "escalade",
            # "SKHRAED": "escalade",
            # "SKHRAER": "escalier",
            # "SPAS": "espace",


            })
    def test_lesson55_terminaisons_MS_for_masse(self):
        self.assertSame({
            "APLS" : "amasse"
        })
    def test_lesson56_STK_starting_de(self):
        self.assertSame({
            "STKPHAFRPB": "démarche",
            "STKPHRAS": "déplace",
            "STKPHROR": "déplore",
 #           "STKPRAEUGS": "dépression",
 #          "STKPRAEUS/*EUF": "dépressive","STKPWOURS/-R": "débourser",
#            "STKWEUFT": "déficit",
            "STKPWEUL": "débile",

            })

    def test_lesson56_EG_ending_ige_starEG_iger(self):
        self.assertSame({
            "PHEUT/EG": "mitigé",
            "ER/*EG": "ériger",
 #           "SREUG": "ériger",

            }, False)


    def test_lesson56_ending_LZ_lise_BLZ_bilise_RLZ_ralise(self):
        self.assertSame({

#            "R-L": "réel",
#            "STRAL": "central",

#            "R-LZ": "réalise",
#            "TEULZ": "utilise",
 #           "PHOBLZ": "mobilise",
            "STRALZ": "centralise",
#            "EUBLZ": "immobilise",
#            "HRERLZ": "libéralise",
#            "WHALZ": "finalise",


            })

    def test_lesson57_KPW_starting_voyel_and_followed_by_mp_or_mb(self):

        self.assertSame({
            "KPWEUR": "empire",
            "KPWREUPL": "imprime",
#            "KPWOB": "impossible",
#            "KPWRAEUGS": "impression",
            "KPWOFP": "empoche",
            "KPWRAS": "embrasse",
            "KPWHRAEUPL": "emblème",
            "KPWHREUBG": "implique",
            "KPWREUPBT": "empreinte",
            "KPWHRAPBT": "implante",
#            "KPWEUG": "ambiant",
            "KPWHRAPB": "implant",


            })

    def test_lesson58_SK_starting_ch_sh_followed_consonne_in_LH(self):
        self.assertSame({
#            "SKWAL": "cheval",
#            "SKWAOBGS": "cheveux",
 #           "SKHEUL": "chenil",
            "SKWAEU": "chevet",
            "SKHRAEU": "chalet",
            "SKWAL/AEU": "chevalet",
            "SKHROUP": "chaloupe",

            })

    def test_lesson58_ortho_SZ_ending_ce(self):
        self.assertSame({
#            "HRA/R-R": "las",
            "HRAS": "lasse",
#            "HRASZ": "lace",
            "HRASZ/AEU": "lacet",
#            "HRA/-S": "lassait",

            })


    def test_lesson59_G_separate_stroke_ant(self):
        self.assertSame({
            "PART/-G":"partant"
            })

    def test_lesson59_G_en(self):
        self.assertSame({

            })

    def test_lesson59_TPH_start_in_followedby_woyel(self):
        self.assertSame({
            "TPHAPT": "inapte",
            "TPHAEURT": "inerte",
            "TPHEUB/EUGS": "inhibition",
#            "TPHOPBGS": "inondation",
#            "TPHOD/O*R": "inodore",
      #      "TPHAB/EUGS": "inanition",
            "TPHOPBD": "inonde",
 #           "TPHUPL/*EUPB": "inhumain",


            })

    def test_lesson59_STPH_start_ins_ens_followed_by_woyel(self):
        self.assertSame({
            "STPHULT": "insulte",
#            "STPH*U": "insinue",
#            "STPHEUB/U": "insinue",
 #           "STPHER/-R": "insérer",
            "STPHEU": "ainsi",
            "STPHEUPD": "insipide",
#            "STPHATS/-F": "insatisfait",

            })

    def test_lesson60_star_ending_word_ou(self):
        self.assertSame({
            "PHAT/O*U": "matou",
#            "KOUR/O*U": "courroux",


            })


    def test_lesson60_FK_ending_sque(self):
        self.assertSame({
            "PWEUFBG": "bisque",
            "TKEUFBG": "disque",
            "KAOFBG": "kiosque",
#            "KROFBG": "kiosque",
            "REUFBG": "risque",
            "PHUFBG": "musc",
            "PAUFBG": "puisque",
            "KAFBG": "casque",
#            "PR-FBG": "presque",
            
            })

    def test_lesson60_TS_ending_ture(self):
        self.assertSame({
            "KULTS": "culture",
#            "TRATS": "température",
#            "TPATS": "facture",
#            "TPHRATS": "filature",
            "TPRATS": "fracture",
            "STRUTS": "structure",
            "RATS": "rature",
#            "KWEUTS": "confiture",

            })

    def test_lesson60_HOstarN_ending_gnon(self):
        self.assertSame({
#            "SHO*PB": "champignon",
            "SHAFRP/HO*PB": "champignon",
            "PWOURG/HO*PB": "bourguignon",

            })

    def test_new_rule_imparfait_3p(self):
        self.assertSame({
            "SRAEUPBT": "seraient", #todo
            "AL/AEUPBT" : "allaient",
        })

    def test_stl_new_rule_PR_pre_prefix(self):
        self.assertSame({
            "PR-PLTS": "permettre",
            "ART/*Z": "arrêta",
#            "ARPT": "apporte",
#            "ARPT/-S": "apportais",
#            "RARPT": "rapporte",
#            "PRAOUP": "préoccupe", 

        })

    def test_stl_new_rule_inverse_ap_prefix(self):
        self.assertSame({
            "PAORT": "apporte",
            "PHRAODZ": "applaudir",

            "PAORT/-S": "apportais",
            "RARPT": "rapporte",
#            "PRAOUP": "préoccupe", 

        })


    def test_stl_new_rule_fg_for_sound_vant(self):
        self.assertSame({
            "AFG": "avant",
            "SOUFG": "souvent",
            "AFGTS": "aventure",
        
#            "AOUP": "préoccupe", 

        })

    def test_new_rule_SP_prefix_SUP_MTS_suffixe_mentaire(self):
        self.assertSame({
            "SPHREPLT": "supplément", 
            "SPHREPLTS": "supplémentaire", 
            "KPHREPLTS": "complémentaire",
            "KPHAEUTS" : "commettre",
            "SOUPLTS": "soumettre", 
            "KPHAPBTS" : "commentaire",
            "PARL/-PLTS": "parlementaire",
        })

    def test_new_rule_imparfaitoet_2p(self):
        self.assertSame({
 #           "AL/-TS" : "allait"
            "R-PBTS/AEUT" : "rentrait",
            "AL/AEUT" : "allait",
        })

    def test_new_rule_start_H(self):
        self.assertAllMatching("hameau", ["HAPL/OE"])


    def test_new_rule_e_ee(self):
        self.assertSame({
#            "KWR/-D" : "joué",
            "TRET/-D" : "traité",
            "TRET/ED" : "traitée",
            "SHRAR/AE":"salarié",
            "SHRAR/AED":"salariée",
            "HAUL/ED" : "hâlée", 
            "PWHREUPBD/-D": "blindé",

        })


    def test_stl_new_rule_FPG_for_chage(self):
        self.assertSame({
#            "AQT" : "adore",
#            "W" : "voyais",
            "TPOEFPG" : "fauchage",

        })

    def test_stl_new_rule_aot_for_auto(self):
        self.assertSame({
#            "AQT" : "adore",
#            "W" : "voyais",
            "AOT/KAR" : "autocar",

        })


    def test_stl_new_rule_FT_for_ste(self):
        self.assertSame({
#            "AQT" : "adore",
            "KPEUFT": "existe",
            "PEUFT": "piste",
            "KEUFT": "kyste",
            "HREUFT": "liste",
        })


    def test_stl_new_rule_verb_it(self):
        self.assertSame({
#            "AQT" : "adore",
            "SAUF/EUT": "suivit",

        })

    def test_stl_new_rule_AOU_for_eo(self):
        self.assertSame({
#            "AQT" : "adore",
            "PRAOUBG/UP": "préoccupe",
            "TPHAOUFL/EUT": "néophyte",

        })

    def test_stl_new_rule_vation(self):
        self.assertSame({
#            "AQT" : "adore",
            "TK-PLD": "demande",
            "TK-PLD/-S": "demandais",            
            "REFRBGS": "réservation",
            "R-FRBGS": "réversion"
        })

        
    def test_fightingwith_o(self):
        self.assertSame({
            "TPOET": "faute",
#            "WHROL": "viol",
            "HOE": "haut",
            "HOELGTS": "hôtel",
            "HOES": "hausse",
            "HOET": "haute",
            "HRO": "lot",
#            "HROEG": "loge", # cant be LOG because LOG='elles en ont'
            "K*/PHRO": "complot",
            "KHROETS": "clôture",
            "KOBG": "coke",
#            "KOEL": "colle", # cant be KOL because it's 'qu'on le'
            "KOET": "côte",
#            "KOEUL": "colis",
            "KOEZ": "cause",
         #   "KPHROE": "complot",
#            "KPOES": "exauce",
            "KPWOE": "impôt",
            "KPWOEFP": "embauche",
            "KRO": "croc",
#            "KROEL": "contrôle",
            })

    

    def test_lesson18_double_conson_can_eliminate_letter(self):
        self.assertSame({
            "WHRAG": "village",
#            "TKPWR-": "guerre",
            "TPRUR": "fourrure",
                         })


        
    def test_todo_lesson22_OIB_for_sound_oine_and_starOIB_for_suffixe_oine(self):
        self.assertSame({
            "TKOEUB": "douane",
# also work            "TKWAB": "douane",
            #"PHOEUB": "moine",
            "PEU/O*EUB": "pivoine", 
                         })
    def test_not_appears(self):
        self.assertSame({
            "ERBG/EUR": "écrire",
#            "AP/RAEU": "après",
            
#            "TKWOEUB": "écris",
       })
#            "iu": "congédié" could be ED without LZ,
    def test_wrong_words(self):
        self.assertSame({
            #           "EUPBLG/-R": "imaginer",
#            "KOU": "coucher",
            "DES": "design",
            "GANK": "gangrener",
                        "ANK": "enquiller",
            "EUPBTS/WHEUR":"intervenir",
            "R-D/WHEUR":"redevenir",
            'PWAEPB/WHU':"bienvenu",

                        "TR":"trimbalant",
            "MON":"monstre",

            "NTRE":"notre",

            "PAT": "patte",
            "PAUT": "pâte",

            "APBLG/OPB/*BGS": "adjonction",
            "ES": "escarpée",
            "SPWOUZ/KWRAFPL" : "enthousiasme",
            "EG/-LZ" : "église",
            "TPHRAFRB/-R":"flamber",

            "SP-R" : "super",
            "S-FR" : "suffirait",
            "TPHRAFRB/-R" : "flamber",
            "ABG/-GZ/-R": "actionner",
            "AE/PROPS/A*ER": "approprier",
            "APB/WA*ER":"envier",
            "PHAPGT/EUT": "magnétite",
#            "EPHAPGT/EUT": "méridionale",
            "PROP/AG/-PBD": "propagande",
            "TPEUBG/HREUTD": "fiscalité",
            "AEUS/TWR*" : "estuaire",
            "KOPBG/ED/A*ED": "congédiée",
            "KOPBG/ED/AED": "congédié",
            "AD/-PLTS" : "admettre",
            "ABG/-GZ/-PLT": "actionnement",
            "WOEUL/AG": "voilage",   
            "PHORD/-LZ/-R": "mordiller",
            "K-T/-R": "quêter",
            "KH": "min",
            "KH-R": "miner",
            "PWORT/SH": "bortsch",
            "PWOUL/-FRBS/ED" :"bouleversée",
            "EUPB/TPRA*BGS": "infraction",
            "PWOL/SH-F/EUFT" : "bolcheviste",
            "PHAPB/EUFL/AEUS/-PLT": "manifestement",
            "PWUL" :"bulle",
            "STKPHRAS/-T" :"déplacent",
            "SHAEUFRPB/-G" :"cherchant",
            "R-T/OURB/-T" :"retournent",
    #"/-PBS" :"suffit",
#            "KPEUFT/-PBS" :"existence",
            "A*E/KOFRPL" :"accomplit",
#            "ME" :"modèle",
            "OERT" :"auteur",
            "KO*U": "coup",
            "HOET/AO*R": "hauteur",
            "HOERT": "hauteur", 
#            "A/TRAFRPBLG/ "affranchir",
#            "PL": "plaisez",
            "-DZ": "dire",
            "R-PBTS/-R": "rentrer",
            "STK-FRLG/EUPBG": "déglingue",
#            "OEA" : "entendaient",
            "SKR-PL/-D" :"charmé",
        })
            
    def todo_vio_WR_WA(self):
        self.assertSame( {"WROLGS": "violation"})
        
    def assertSame(self, words, force_verb=True):
        found = False
        namefunc=str(sys._getframe().f_back.f_code.co_name).replace('test_','')
#        namefunc=inspect.stack()[1][3]
        with open('lessons/json/'+str(namefunc)+'.json', "w") as d:
            myjson=json.dumps(words, indent = 4, ensure_ascii=False )
            d.write(myjson)
        with open('lessons/typey_type/'+str(namefunc)+'.type', "w") as d:
            for elem in words.items():
                d.write(elem[1]+'	'+elem[0]+"\n")

        return self.assertAll(words, force_verb)
        self.assertSounds(words)

        for elem in words.items():
            first_elem =""

            stenos = self.steno(elem[1], force_verb)
            assert elem[0] in stenos
            return True
            if elem[0] in stenos:
#                found = True
#                assert elem[0] in stenos
                continue

                print('test found' , sten_str)               
#            for sten_str in self.steno(elem[1], force_verb):
                first_elem = sten_str
                
 
#                if  elem[0] == sten_str:

            if not found :
                assert elem[0] in stenos

            found = False
#            return True
    def assertAll(self, words, force_verb=True):
        found = False

        self.assertSounds(words)

        for elem in words.items():
            first_elem =""

            stenos = self.steno(elem[1], force_verb)
            assert elem[0] in stenos
            if elem[0] in stenos:
                found = True
                assert elem[0] in stenos
                continue

 #                print('test found' , sten_str)               
#            for sten_str in self.steno(elem[1], force_verb):
                first_elem = sten_str
                
 
#                if  elem[0] == sten_str:

            if not found :
                assert elem[0] in stenos

            found = False
#            return True


    def test_verb_matching(self):
        self.assertAllMatching('parlez' , ["PARL/*EZ"])


    def test_verb_matching_ter(self):
        self.assertAllMatching('terminer' , ['-TS/PHEUB/-R', 'TAEURPL/EUB/-R'])

    def test_verb_matching_importee(self):
        self.assertAllMatching('importée' ,['EUPB/-RPT/ED', 'KPWORT/ED'])

    def test_stl_verb_matching_gouvern(self):
        self.assertAllMatching('gouverne' , ["TKPWOUFRB"])

    def test_verb_matching_allais(self):
        self.assertAllMatching('allais' , ['AE/HR/-S', 'AL/-S', 'HR/-S'] )

    def test_verb_matching_courait(self):
        self.assertAllMatching('courait' , ['KOUR/AEUT'] )

    def test_verb_matching_salarier(self):
        self.assertAllMatching('salarier' , ['SHRAR/AER'] ) 

    def test_verb_matching_salarie(self):
        self.assertAllMatching('salarié' , ['SHRAR/AE'] ) 

    def test_nom_matching_adhesion(self):
        self.assertAllMatching('adhésion' , ['AD/EGZ', 'AD/-GZ'] ) 

    def test_nom_matching_existerai(self):
        self.assertAllMatching('existerais' , ['KPEUFT/-RS'] ) 

    def test_nom_matching_escarpee(self):
        self.assertAllMatching('escarpée' , ['AD/EGZ'] ) 

    def test_nom_matching_anneau(self):
        self.assertAllMatching('anneau' , ['AE/TPHOE', 'AB/OE'] ) 

    def test_nom_matching_agneau(self):
        self.assertAllMatching('agneau' , ['AE/-PG/OE', 'APG/OE'] ) 

    def test_nom_matching_confirme(self):
        self.assertAllMatching('confirme' , ['STPEURPL', 'KOPB/TPEURPL', 'KOEPB/TPEURPL', 'KWEURPL']) 

    def test_verb_matching_salarie(self):
        self.assertAllMatching('salariée' , ['SHRAR/AED'] ) 

    def test_verb_matching_ralier(self):
        self.assertAllMatching('rallier' , ['-RL/AER','RAL/AER'] ) 

    def test_verb_matching_elle_laisse(self):
        self.assertAllMatching('haïsse' , ["HAEUS"])

        
    def assertAllMatching(self,word, words) :
        steno_class=Steno(self.corpus)
        print(steno_class)
        for elem in self.steno(word):
            assert elem in words
        return True
                

    def  assertSounds(self,words):
        steno_class=Steno(self.corpus)
        for elem in words.items():
            word = steno_class.find(elem[1])
            print(elem[1],vars(word))
            
    def all_tao_entry(self):
        with open('resources/tao_la_salle.json') as json_file:
            data = json.load(json_file)
        found = []
        not_found = []
        for elem in data.items():
            if elem[0] in self.steno(elem[1]):
                found.append(elem[1])
            else:
                not_found.append(elem[1])

        print("FOUND: ",found)
        print("\nNOT FOUND: ",not_found)
        assert False

    def generate_dic(self):
        picked = []
        with open('resources/Lexique383.tsv') as f:
            data = f.readlines()
            
        for line in data:
            entry = line.split('\t')
            word = entry[0]
            picked.append(word)
        translated_word = {}
        with open('resources/dicofr.json', "w") as d:
            for word in picked:
                for steno in np.unique(self.steno(word)):
                    if steno in translated_word  and translated_word[steno] == word: 
                        continue
                    translated_word[steno] = word
                    d.write("'"+steno + "':'"+ word+"',\n")
           
