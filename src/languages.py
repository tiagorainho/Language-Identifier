
from utils import colors

languages = {
        'english': ['dataset/eng_AU.latn.Aboriginal_English.comb-train.utf8'],
        'polish': ['dataset/pol_PL.latn.Polish.comb-train.utf8'],
        'middle_english': ['dataset/enm_UK.latn.Middle_English.PD-train.utf8'],
        'creole_french': ['dataset/acf_ST.latn.Saint_Lucian_Creole_French.bible-train.utf8'],
        'french': ['dataset/fra_FR.latn.French.comb-train.utf8'],
        'german': ['dataset/deu_DE.latn.German.comb-train.utf8'],
        'franconian_german': ['dataset/vmf_DE.latn.East_Franconian_German.wiki-train.utf8'],
        'brazilian portuguese': ['dataset/por_BR.latn.portugues.comb-train.utf8', 'dataset/por_BR.latn.portugues.comb-test-120-200.txt'],
        # 'portuguese': ['dataset/por_PT.latn.Portugese.comb-devtest-test-120-200.txt','dataset/por_PT.latn.Portugese.comb-devtest-test-80-120.txt', 'dataset/por_PT.latn.Portugese.comb-devtest-test-20-40.txt', 'dataset/portugues_ex.txt'],
        'portuguese': ['dataset/por_PT.latn.Portugese.comb-devtest-test-120-200.txt', 'dataset/portugues_ex.txt'],
        'italian': ['dataset/ita_IT.latn.Italian.comb-train.utf8', 'dataset/ita_IT.latn.Italian.comb-test-120-200.txt'],
        'latin': ['dataset/lat_VA.latn.Latin.comb-train.utf8'],
        'spanish': ['dataset/spa_ES.latn.Spanish.comb-test-120-200.txt', 'dataset/spa_ES.latn.Spanish.comb-devtest-test-80-120.txt']
    }

languages_colors = {
        'None': '\033[0m',
        'english': colors.fg.blue,
        "portuguese": colors.fg.green,
        "italian": colors.fg.yellow,
        "german": colors.fg.cyan,
        "french": colors.fg.red,
        "spanish": colors.fg.purple,
        "polish": colors.fg.darkgrey,
        "middle_english": colors.fg.lightblue,
        "creole_french": colors.fg.lightred,
        "franconian_german": colors.fg.lightcyan,
        "brazilian portuguese": colors.fg.lightgreen,
        "latin": colors.bg.green
    }