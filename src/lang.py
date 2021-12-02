from typing import List, Tuple
from FCM import FCM
import math


class Lang:

    name: str
    fcm: FCM
    lang_threshold: float


    def __init__(self, language:str, threshold:float = 2, k:int = 5, alpha:float = 0.5) -> None:
        self.name = language
        self.lang_threshold = threshold
        self.fcm = FCM(k=k, alpha=alpha, alphabet='')


    def train(self, file_name:str) -> None:
        with open(file_name, 'r') as file:
            for line in file.readlines():
                if len(line) < self.fcm.k: continue
                self.fcm.update(line.lower())

    
    # returns the entropy for the sample text
    def entropy_per_character(self, text:str) -> float:
        s = 0
        text = text.lower()

        last_characters = text[:self.fcm.k]
        for i in range(self.fcm.k, len(text)):
            current_char = text[i]
            
            s += - math.log2(self.fcm.probability_e_c(current_char, last_characters))

            last_characters = last_characters[1:] + current_char
        return s/(len(text)-self.fcm.k)
    
    def __repr__(self):
        return f'{self.name}'


def classify(language_classifiers:List[Lang], text:str, threshold:float=4) -> Tuple[Lang, float] or Tuple[None, float]:
    language_classifications = [(lang_classifier, lang_classifier.entropy_per_character(text)) for lang_classifier in language_classifiers]
    language, entropy = min(language_classifications, key=lambda t: t[1])
    return (language if entropy <= threshold else None, entropy)
    

if __name__ == '__main__':

    languages = [
        ('english', ['datasets/MIL-TALE/1/00README'])
    ]

    language_classifiers = []

    for language, language_datasets in languages:

        lang = Lang(language)

        for language_dataset in language_datasets:
            lang.train(language_dataset)

        language_classifiers.append(lang)

    classification = classify(language_classifiers, 'the directory in which this file', threshold=4)
    
    print(classification)
    

