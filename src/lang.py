from typing import List, Tuple
from FCM import FCM
import math
from argparse import ArgumentParser


class Lang:

    name: str
    fcm_list: List[FCM]

    optimal_k:float
    min_k_weight:float
    max_k_weight:float
    weight_factor:float
    orientation_strength:float
    thinness:float
    thickness:float

    def __init__(self, language:str = "", parameters: List[Tuple[int, float]] = [(5, 0.1)]) -> None:
        self.optimal_k = 5
        self.min_k_weight = 0.2
        self.max_k_weight = 5
        self.weight_factor = 1
        self.orientation_strength = 10
        self.thinness = 1
        self.thickness = 3

        self.name = language
        self.fcm_list = [FCM(k=k, alpha=alpha) for k, alpha in parameters]


    def train(self, file_name:str) -> None:
        with open(file_name, 'r') as file:
            for line in file.readlines():
                for fcm in self.fcm_list:
                    if len(line) < fcm.k: continue
                    fcm.update(line.lower())


    def estimated_information(self, text:str):
        total = 0
        sum_k_weights = 0
        for fcm in self.fcm_list:
            weighted_k = self.calculate_fcm_weight(fcm)
            total += self.amount_of_information(text, fcm) * weighted_k
            sum_k_weights += weighted_k
        return total / sum_k_weights


    # returns the mean entropy for the sample text
    def amount_of_information(self, text:str, fcm: FCM) -> List[float]:
        entropies = self.num_bits(text, fcm)
        return sum(entropies) / len(entropies)

    def calculate_fcm_weight(self, fcm:FCM):
        return self.min_k_weight+(self.max_k_weight-self.min_k_weight)/(self.weight_factor+self.thinness*((fcm.k-self.optimal_k)/self.thickness)**4)**self.orientation_strength

    def estimated_num_bits(self, text:str):
        values = []
        sum_k_weights = 0
        for fcm in self.fcm_list:
            entropies = self.num_bits(text, fcm)
            
            # use weighted k to assign different weights on each k
            weighted_k = self.calculate_fcm_weight(fcm)
            weighted_entropies = [weighted_k * value for value in entropies]
            sum_k_weights += weighted_k

            values.append(weighted_entropies)

        lst = []
        for i in range(len(text)):
            total = 0
            for entropies in values:
                # use all fcms even when the larger ones (using their last value -> tail)
                total += entropies[i] if i < len(entropies) else entropies[-1]
            lst.append(total/sum_k_weights)
        return lst


    def num_bits(self, text:str, fcm:FCM) -> List[float]:
        entropies = []
        text = text.lower()

        last_characters = text[:fcm.k]
        for i in range(fcm.k, len(text)):
            current_char = text[i]
            
            entropies.append(-math.log2(fcm.probability_e_c(current_char, last_characters)))

            last_characters = last_characters[1:] + current_char
        return entropies


    def __repr__(self):
        return f'{self.name}'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--files", metavar="model text", type=str, required=True, nargs='*',
                        help="Files representing the class")
    parser.add_argument("--t", metavar="analysis text", type=str, required=True,
                        help="File with the text to analyze")
    parser.add_argument("--alpha", metavar="alpha", type=float, required=False, default=0.5,
                        help="Variable responsible for smoothing")
    parser.add_argument("--k", metavar="sliding window", type=int, required=False, default=5,
                        help="Size of shifting window")
    return parser.parse_args()

if __name__ == '__main__':
    
    args = parse_args()

    lang = Lang(parameters=[(args.k, args.alpha)])
    for file_name in args.files:
        lang.train(file_name)
    with open(args.t, 'r') as file:
        text = ''.join([line for line in file.readlines()])
    
    num_bits = round(lang.amount_of_information(text, lang.fcm_list[0]), 3)
    print(f"Estimated number of bits required to compress t, using the computed model {args.modeltext}:\n{num_bits}")
