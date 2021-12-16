from lang import Lang
from argparse import ArgumentParser
from typing import DefaultDict, List
from collections import defaultdict
import matplotlib.pyplot as plt
from utils import colors
from threading import Thread

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--file", metavar="file", type=str, required=True,
                        help="File to analyze")
    parser.add_argument("--threshold", metavar="threshold", type=int, required=False, default=4,
                        help="Threshold")
    return parser.parse_args()


def locatelang(language_classifiers:List[Lang], text:str, threshold:float):
    plt.title('languages')
    plt.xlabel('characters')
    plt.ylabel('bits')
    language_entropies = dict()
    for lang_classifier in language_classifiers:
        smoothed_entropies = smooth_values(lang_classifier.estimated_num_bits(text), 15)
        language_entropies[lang_classifier] = smoothed_entropies
        xaxis = [i for i in range(0, len(smoothed_entropies))]
        plt.plot(xaxis, smoothed_entropies)
        plt.text(xaxis[-1], smoothed_entropies[-1], f' {lang_classifier}')
    plt.plot(xaxis, [threshold]*len(xaxis))
    print("done")
    t = Thread(target=plt.show(), daemon=False)
    t.start()
    

    #plt.show()

    language_analysis = []
    last_language = lambda: None if len(language_analysis)==0 else language_analysis[-1][0]
    default_none = 'None'
    for i in range(0, len(list(language_entropies.values())[0])):
        lang_bits = []
        for language, smoothed_entropies in language_entropies.items():
            lang_bits.append((language, smoothed_entropies[i]))
        lang, bits = min(lang_bits, key = lambda t: t[1])

        if bits > threshold:
            if last_language() != default_none:
                language_analysis.append((default_none, i))
        elif last_language() != lang:
            language_analysis.append((lang, i))

    return language_analysis       


def smooth_values(values, smooth_factor):
    smoothed_values = []
    for i in range(0, len(values)-(smooth_factor-1)):
        smoothed_values.append(sum(values[i:i+smooth_factor])/smooth_factor)
    return smoothed_values


if __name__ == '__main__':
    
    args = parse_args()
    
    file = open(args.file, 'r')
    text_to_classify = ""
    for line in file.readlines():
        text_to_classify += line

    languages = [
        ('english', ['dataset/eng_AU.latn.Aboriginal_English.comb-train.utf8']),
        # ('middle english', ['dataset/enm_UK.latn.Middle_English.PD-train.utf8']),
        # ('creole_french', ['dataset/acf_ST.latn.Saint_Lucian_Creole_French.bible-train.utf8']),
        # ('french', ['dataset/fra_FR.latn.French.comb-train.utf8']),
        # ('german', ['dataset/deu_DE.latn.German.comb-train.utf8']),
        # ('franconian_german', ['dataset/vmf_DE.latn.East_Franconian_German.wiki-train.utf8']),
        # ('brazilian portuguese', ['dataset/por_BR.latn.portugues.comb-train.utf8', 'dataset/por_BR.latn.portugues.comb-test-120-200.txt']),
        ('portuguese', ['dataset/por_PT.latn.Portugese.comb-devtest-test-120-200.txt', 'dataset/por_PT.latn.Portugese.comb-devtest-test-80-120.txt', 'dataset/por_PT.latn.Portugese.comb-devtest-test-20-40.txt']),
        # ('italian', ['dataset/ita_IT.latn.Italian.comb-train.utf8', 'dataset/ita_IT.latn.Italian.comb-test-120-200.txt']),
        # ('latin', ['dataset/lat_VA.latn.Latin.comb-train.utf8']),
        # ('polish', ['dataset/pol_PL.latn.Polish.comb-train.utf8']),
        ('spanish', ['dataset/spa_ES.latn.Spanish.comb-test-120-200.txt', 'dataset/spa_ES.latn.Spanish.comb-devtest-test-80-120.txt'])
    ]

    language_classifiers = []

    for language, language_datasets in languages:
        lang = Lang(language, [(5, 0.1), (7, 0.1)])
        language_classifiers.append(lang)
        for language_dataset in language_datasets:
            lang.train(language_dataset)
        
    results = locatelang(language_classifiers, text_to_classify, threshold=args.threshold)

    lang_colors = {
        'None': '\033[0m',
        'english': colors.fg.blue,
        "portuguese": colors.fg.green,
        "italian": colors.fg.yellow,
        "german": colors.fg.cyan,
        "french": colors.fg.purple,
        "spanish": colors.fg.red
    }

    for i, (lang, idx) in enumerate(results):
        if i >= len(results)-1:
            next_idx = len(text_to_classify)
        else:
            next_lang, next_idx = results[i+1]
        
        print(f"{lang_colors[str(lang)]}{text_to_classify[idx:next_idx]}{lang_colors['None']}", end='')
    print()
