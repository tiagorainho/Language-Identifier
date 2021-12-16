from lang import Lang
from argparse import ArgumentParser
from typing import List, Tuple


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--file", metavar="file", type=str, required=True,
                        help="File to analyze")
    parser.add_argument("--threshold", metavar="threshold", type=int, required=False, default=4,
                        help="Threshold")
    return parser.parse_args()    

def find_lang(language_classifiers:List[Lang], text:str, threshold:float) -> Tuple[Lang, float] or Tuple[None, float]:
    language_classifications = [(lang_classifier, lang_classifier.estimated_information(text)) for lang_classifier in language_classifiers]
    language, entropy = min(language_classifications, key=lambda t: t[1])
    return (language if entropy <= threshold else None, entropy)

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
        # ('portuguese', ['dataset/por_PT.latn.Portugese.comb-devtest-test-120-200.txt','dataset/por_PT.latn.Portugese.comb-devtest-test-80-120.txt', 'dataset/por_PT.latn.Portugese.comb-devtest-test-20-40.txt']),
        # ('italian', ['dataset/ita_IT.latn.Italian.comb-train.utf8', 'dataset/ita_IT.latn.Italian.comb-test-120-200.txt']),
        # ('latin', ['dataset/lat_VA.latn.Latin.comb-train.utf8']),
        ('polish', ['dataset/pol_PL.latn.Polish.comb-train.utf8']),
        # ('spanish', ['dataset/spa_ES.latn.Spanish.comb-test-120-200.txt', 'dataset/spa_ES.latn.Spanish.comb-devtest-test-80-120.txt'])
    ]

    language_classifiers = []

    for language, language_datasets in languages:

        lang = Lang(language, [(5, 0.1), (7, 0.1)])

        for language_dataset in language_datasets:
            lang.train(language_dataset)

        language_classifiers.append(lang)

    
    classification = find_lang(language_classifiers, text_to_classify, threshold=args.threshold)
    
    print(classification)