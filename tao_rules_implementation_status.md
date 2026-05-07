ANALYSE DES RÈGLES TAO - STATUT D'IMPLÉMENTATION
Généré le : 2026-05-07
Source : src/steno.py, src/steno_encoding.py vs TAO_Rules_Organized.md / TAO_rules.md


== RÈGLES NON IMPLÉMENTÉES ==

-- Phonétiques --

| Règle                              | Chord attendu | Statut                                               |
|------------------------------------|---------------|------------------------------------------------------|
| Son "ste" (piste, poste)           | *S            | Différent — le code utilise -FT ou ST (new rule)     |
| Son "oine" (douane) IPA wan        | OIB           | Différent — implémenté WOIB (W en plus)              |
| Son "mbe" (jambe, limbe)           | -FRB inline   | Différent — /OFRB, /EUFRB (stroke séparé)            |
| Son "mble" (comble, tremble)       | -FRBL inline  | Différent — /OFRBL, /AFRBL (stroke séparé)           |
| Son "mbre" (ombre, timbre)         | -FRBS inline  | Différent — /OFRBS, /EUFRBS (stroke séparé)          |
| Son "mpre" (compre)                | -FRPS inline  | Différent — /OFRPS (stroke séparé)                   |
| Son "mpe" (trompe, campe)          | -FRP inline   | Différent — /OFRP, /AFRP (stroke séparé)             |
| Son "mple" (simple, ample)         | -FRPL inline  | Différent — /OFRPL, /AFRPL (stroke séparé)           |
| Son "mpte" (compte, prompt)        | -FRPT         | ABSENT                                               |
| Son "ngue"                         | -NG           | ABSENT                                               |
| Son "nction/ntion" général         | -PBGS         | Partiel — seulement 5ksj§ couvert                    |
| Son "ctionner"                     | -PBGS/-R      | ABSENT                                               |
| Son "itionne"                      | IGZ           | ABSENT                                               |
| Son "cre" (ancre)                  | -RK           | ABSENT                                               |
| Son "~kʁ" avec nasale (cancre)     | -FRKS         | ABSENT                                               |
| Son "nqu" (banque)                 | -FRBG         | ABSENT                                               |
| Son "nqul" (bancal)                | -FRBLG        | ABSENT                                               |
| Son "on" en terminaison            | *N stroke sep | Différent — § → ON direct (pas stroke séparé)        |
| Diphtongue "io" (bio, kiosque)     | AO            | Différent — jO → RO dans CHUNKS                      |
| Son "stwe"                         | STW           | ABSENT                                               |
| Son "dwe/dve" (divorce)            | DW            | ABSENT                                               |
| Final "xte" (texte)                | *-BGS         | ABSENT                                               |

-- Orthographiques --

| Règle                              | Chord attendu | Statut                                          |
|------------------------------------|---------------|-------------------------------------------------|
| Suffixe "ième" (huitième)          | A*EM          | ABSENT                                          |
| Suffixe "ance" / "ence"            | -NS           | COMMENTÉ dans ORTHO_SUFFIXES (désactivé)        |
| Suffixe "uel" (uel, uelle)         | W*EL          | Différent — /WEL (sans étoile)                  |
| Suffixe "eur" général              | AO*R          | Différent — /AOR (sans étoile)                  |
| Suffixe "aire" (notaire)           | A*IR          | Différent — ER→AIR (sans étoile)                |
| Suffixe "logiste"                  | LO*IS         | Différent — /HRO*EUS dans SUFFIXES              |
| Suffixe "gnon" (bourguignon)       | HO*N          | Proche — /HO*PB (pas exact)                     |
| Suffixe "ral" / "nal"              | -NL           | ABSENT                                          |
| Son "tude" (attitude, habitude)    | -TD           | ABSENT                                          |
| CH/SH initial (leçon 58, SK-)      | SK-           | Différent — S → SH (SK- non distingué)          |
| Préfixe "multi"                    | MULT          | Différent — implémenté PHULT                    |
| Préfixe "inter"                    | INTS          | Différent — implémenté EUPBTS                   |

-- Générales / Spécifiques --

| Règle                                        | Statut                                                       |
|----------------------------------------------|--------------------------------------------------------------|
| Omission du "i" médian (rapide → RAPD)       | Logique écrite mais DÉSACTIVÉE (try_to_remove_woyel commenté)|
| Étoile verbe/nom homophones                  | Partiel — add_star non appelé dans newtransform()            |
| Brief KWA = "il y a"                         | Non généré (dans tao_la_salle.json manuellement)             |
| Brief SWA = "s'il a"                         | Non généré                                                   |
| Brief SKWA = "s'il y a"                      | Non généré                                                   |
| Brief SKWHR = "je le"                        | Non généré                                                   |
| Brief *UT = forme interrogative (parles-tu)  | Non généré                                                   |
| Brief -Z seul = "est"                        | Non généré                                                   |
| Brief *LG = particule "-là"                  | Non généré                                                   |
| Chiffres phonétiques (SUN=100, PHRIL=1000)   | NON GÉNÉRÉS                                                  |
| Épellation / fingerspelling (leçon 20)       | NON GÉNÉRÉE                                                  |
| -FRBGS = virgule collée                      | NON GÉNÉRÉ                                                   |
| -RPBGS = point collé                         | NON GÉNÉRÉ                                                   |


== RÈGLES IMPLÉMENTÉES DIFFÉREMMENT ==

| Règle                             | Attendu       | Implémenté   | Note                                    |
|-----------------------------------|---------------|--------------|-----------------------------------------|
| Préfixe "con"                     | KOEN          | KOPB         | Notation différente (OE vs O+PB)        |
| Suffixe "uel"                     | W*EL          | /WEL         | Sans étoile                             |
| Son "ste"                         | *S            | -FT          | Règle intentionnellement modifiée       |
| Terminaisons en "on"              | *N séparé     | ON direct    | Pas de stroke séparé                    |
| Étoile féminin (new-lexique)      | (non dans TAO)| add_star()   | Nouvelle règle ajoutée hors théorie TAO |


== RÈGLES CORRECTEMENT IMPLÉMENTÉES ==

-- Phonétiques (sons) --

| Règle                        | Chord | Règle                        | Chord   |
|------------------------------|-------|------------------------------|---------|
| F initial                    | TP-   | V initial                    | W-      |
| B initial                    | PW-   | D initial                    | TK-     |
| L initial                    | HR-   | M initial                    | PH-     |
| G/gue initial                | TKPW- | J initial (ʒ)                | SKWR-   |
| Z initial                    | SWR-  | N initial                    | TPH-    |
| V final                      | -F    | K final                      | -BG     |
| M final                      | -PL   | N final                      | -PB     |
| n/ne final                   | -B    | soft j final                 | -G      |
| O long (haut, sauve)         | OE    | Son "eu" (eux, seul)         | AO      |
| Son "è" (père, trait)        | AEU   | Son "i" (lit, pile)          | EU      |
| Son "ou" (tout, tour)        | OU    | Son "ui"/"a long" (pluie)    | AU      |
| Son "ieu" (vieux, yeux)      | AOEU  | Son "ié/iè" (pied, tiers)    | AE      |
| Son "oi" (roi, bois)         | OEU   | Son "oin" (soin, coin)       | OEU+PB  |
| Son "oui" (oui, Louis)       | AOU   | Son "ien" (chien)            | AEN     |
| Son "ouine"                  | AOUB  | Son "ienne"                  | AEB     |
| Son "aine" (peine)           | AIB   | Son "éu" diphtongue          | EU      |
| Son "ia" (cria)              | RA    | Son "ua" (situation)         | WA      |
| CH initial                   | SH-   | CH final                     | -FP     |
| QWE                          | KW    | Son "tw" (fructueux)         | TW      |
| Son "sw" (swaziland)         | SW    | fre/vre final                | -FR     |
| rche                         | -FRPB | nche                         | -FRPBLG |
| ciation                      | SRAGS | ille                         | -LZ     |
| reille                       | -RLZ  | gne final                    | -PG     |
| nge/dj/bj                    | -PBLG | sion/zon                     | -GZ     |
| ction                        | *BGS  | ption                        | -PGS    |
| tre/ture                     | -TS   | X/ks final                   | -BGS    |
| -ment                        | -PLT  | -vement                      | -FPLT   |
| vle (vouloir)                | WHR-  | ngl (angle)                  | -FRLG   |
| sne                          | STPH- | mbe → stroke séparé          | /OFRB   |
| mble → stroke séparé         | /OFRBL| mbre → stroke séparé         | /OFRBS  |
| mpre → stroke séparé         | /OFRPS| mpe → stroke séparé          | /OFRP   |
| mple → stroke séparé         | /OFRPL|                              |         |

-- Orthographiques --

| Règle                        | Chord   | Règle                       | Chord    |
|------------------------------|---------|-----------------------------|----------|
| Infinitif 1er groupe         | /-R     | Passé composé               | /-D      |
| Imparfait "ait"              | /-S     | Conditionnel "rait"         | /-RS     |
| Participe présent "ant"      | /-G     | Verbe en "ez" (vous)        | /*EZ     |
| Suffixe "ier"                | AER     | Suffixe "ière"              | A*ER     |
| Suffixe "ène"                | *EB     | Suffixe "aine"              | A*IB     |
| Suffixe "ué/oué"             | W*E     | elle/el                     | *EL/EL   |
| teur/trice                   | *RT/*RTS| quel/quelle                 | -BLG     |
| -t-elle/tel                  | -LGTS   | peur                        | -RP      |
| leur/ral                     | -RL     | deur                        | -RD      |
| gueur                        | -RG     | neur                        | -RN      |
| rtion/ration                 | -RGS    | vité/cité                   | -FT      |
| cis/-ci/rbe/rne              | -RB     | tion/cien                   | -GS      |
| cation                       | -BGS    | ité                         | ITD      |
| ilité                        | -LT     | bité                        | -BT      |
| bilité                       | -BLT    | bal/ble                     | -BL      |
| rbal/rible                   | -RBL    | voir                        | -FRS     |
| th (mythe)                   | -GT     | lation                      | -LGS     |
| pluriel "aux"                | O*EX    | sité                        | ST*E     |
| logue                        | LO*EG   | logie                       | LO*IG    |
| lise                         | -LZ     | bilise                      | -BLZ     |
| préfixe "com"                | K*      | préfixe "comm"              | KPH      |
| préfixe "con"                | KOPB    | préfixe "cons"              | KOPBS    |
| préfixe "fin/fen"            | WH      | préfixe "dé/des"            | STK      |
| préfixe "dés" + voyelle      | TKAOEZ  | préfixe "trans"             | TRAPBS   |
| préfixe "re"                 | R-      | empr/embr initial           | KPW      |
| ce (homonymie)               | -SZ     |                             |          |
