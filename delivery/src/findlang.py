from lang import Lang
from argparse import ArgumentParser
from typing import List, Tuple
from languages import languages

def find_lang(language_classifiers:List[Lang], text:str, threshold:float) -> Tuple[Lang, float] or Tuple[None, float]:
    language_classifications = [(lang_classifier, lang_classifier.estimated_information(text)) for lang_classifier in language_classifiers]
    language, entropy = min(language_classifications, key=lambda t: t[1])
    return (language if entropy <= threshold else None, entropy)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--file", metavar="file", type=str, required=True,
                        help="File to analyze")
    parser.add_argument("--threshold", metavar="threshold", type=float, required=False, default=4,
                        help="Threshold")
    parser.add_argument("--languages", metavar="languages", type=str, default=[], required=False, nargs='*',
                        help="Selected languages")
    parser.add_argument("--alpha", metavar="alpha", type=float, required=False, default=[0.5], nargs='*',
                        help="Variable responsible for smoothing")
    parser.add_argument("--k", metavar="sliding window", type=int, required=False, default=[5], nargs='*',
                        help="Size of shifting window")
    return parser.parse_args()    
    

if __name__ == '__main__':

    args = parse_args()
    assert len(args.k) == len(args.alpha), 'Number of k arguments must be the same of alpha arguments'
    k_alpha_list = [(args.k[i], args.alpha[i]) for i in range(len(args.k))]
    if len(args.languages) == 0: args.languages = languages.keys()
    
    with open(args.file, 'r') as file:
        text_to_classify = ''.join([line for line in file.readlines()])

    language_classifiers = []
    for language in args.languages:
        if language not in languages: continue

        lang = Lang(language, k_alpha_list)

        language_datasets = languages[language]
        for language_dataset in language_datasets:
            lang.train(language_dataset)

        language_classifiers.append(lang)

    language, amount_of_information = find_lang(language_classifiers, text_to_classify, threshold=args.threshold)
    print(f'Classification:\nLanguage: {language}\nAmount of information: {round(amount_of_information, 2)}')