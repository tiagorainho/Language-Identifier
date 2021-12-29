from collections import defaultdict
from lang import Lang
from argparse import ArgumentParser
from typing import List
import matplotlib.pyplot as plt
from languages import languages, languages_colors as lang_colors
import json


def locatelang(language_classifiers:List[Lang], text:str, threshold:float, smooth_window:int=15, show:bool=False):
    if show:
        plt.title('languages')
        plt.xlabel('characters')
        plt.ylabel('bits')
    language_entropies = dict()
    for lang_classifier in language_classifiers:
        smoothed_entropies = smooth_values(lang_classifier.estimated_num_bits(text), smooth_window)
        language_entropies[lang_classifier] = smoothed_entropies
        if show:
            xaxis = [i for i in range(0, len(smoothed_entropies))]
            plt.plot(xaxis, smoothed_entropies)
            plt.text(xaxis[-1], smoothed_entropies[-1], f' {lang_classifier}')
    if show:
        plt.plot(xaxis, [threshold]*len(xaxis))
        plt.show()

    language_analysis = []
    last_language = lambda: None if len(language_analysis)==0 else language_analysis[-1][0]
    default_none = None
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
    for i in range(len(values)):
        if i < len(values)-(smooth_factor-1):
            # when its the normal median
            smoothed_values.append(sum(values[i:i+smooth_factor])/smooth_factor)
        else:
            # when its a median with less than the sliding window
            smoothed_values.append(sum(values[i:])/(len(values)-i))

    return smoothed_values

def calculate_accuracy(results, truth, size):
    values = defaultdict(set)
    for i, (lang, start) in enumerate(truth):
        end = size if i+1 == len(truth) else truth[i+1][1]
        values[str(lang)].update(range(start, end))
    
    correct_chars = 0
    for i, (lang, start) in enumerate(results):
        end = size if i+1 == len(results) else results[i+1][1]
        lang_values = values[str(lang)]
        correct_chars += len(set(range(start, end)).intersection(lang_values))
    
    return correct_chars / size

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--file", metavar="file", type=str, required=True,
                        help="File to analyze")
    parser.add_argument("--threshold", metavar="threshold", type=int, required=False, default=4,
                        help="Threshold")
    parser.add_argument("--languages", metavar="languages", type=str, required=False, default=[], nargs='*',
                        help="Languages to use as models")
    parser.add_argument("--alpha", metavar="alpha", type=float, required=False, default=[0.5], nargs='*',
                        help="Variable responsible for smoothing")
    parser.add_argument("--k", metavar="sliding window", type=int, required=False, default=[5], nargs='*',
                        help="Size of shifting window")
    parser.add_argument("--graph_smoothing", metavar="smooth window", type=int, required=False, default=15,
                        help="graph smoothing")
    parser.add_argument("--show", metavar="show", type=bool, required=False, default=False,
                        help="show graph")
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
        language_datasets = languages[language]
        lang = Lang(language, k_alpha_list)
        language_classifiers.append(lang)
        for language_dataset in language_datasets:
            lang.train(language_dataset)
    
    # text_to_classify = ''.join([text_to_classify[0] for _ in range(15)])+text_to_classify # sliding window a começar com extrapolacao
    results = locatelang(language_classifiers=language_classifiers, text=text_to_classify, threshold=args.threshold, smooth_window=args.graph_smoothing, show=args.show)

    print('-'*20)
    for i, (lang, idx) in enumerate(results):
        if i >= len(results)-1:
            next_idx = len(text_to_classify)
        else:
            next_lang, next_idx = results[i+1]
        
        print(f"{lang_colors[str(lang)]}{text_to_classify[idx:next_idx]}{lang_colors['None']}", end='')
    print(lang_colors['None'], '-'*20)

    return_result = []
    for i, (lang, start) in enumerate(results):
        if lang == None: continue
        end = len(text_to_classify) if i+1 == len(results) else results[i+1][1]-1
        coord = (lang, start, end)
        return_result.append(coord)
    
    print('\nLanguage locations:\n', return_result)

    # this only applies to the specific file "multiple.txt"
    truth = json.load(open("truth.txt"))
    
    accuracy = calculate_accuracy(results, truth, len(text_to_classify))
    print(f'accuracy: {round(accuracy*100, 2)}%')
