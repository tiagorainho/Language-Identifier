from typing import DefaultDict, List, Tuple
from FCM import FCM
import math
from argparse import ArgumentParser



class Lang:

    name: str
    fcm_list: List[FCM]


    def __init__(self, language:str = "", parameters: List[Tuple[int, float]] = [(5, 0.1)]) -> None:
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
        for fcm in self.fcm_list:
            total += self.amount_of_information(text, fcm) * fcm.k # peso
        return total / sum([fcm.k for fcm in self.fcm_list])


    # returns the mean entropy for the sample text
    def amount_of_information(self, text:str, fcm: FCM) -> List[float]:
        entropies = self.num_bits(text, fcm)
        return sum(entropies) / len(entropies)


    #continue here
    def estimated_num_bits(self, text:str):
        values = []
        for fcm in self.fcm_list:
            entropies = [bits*fcm.k for bits in self.num_bits(text, fcm)]
            values.append(entropies) # peso

        lst = []
        for i in range(len(text)-5):
            total = 0
            for entropies in values:
                if i < len(entropies):
                    total += entropies[i]
            lst.append(total/sum([fcm.k for fcm in self.fcm_list]))
        return lst


    def num_bits(self, text:str, fcm:FCM) -> List[float]:
        entropies = []
        text = text.lower()

        last_characters = text[:fcm.k]
        for i in range(fcm.k, len(text)):
            current_char = text[i] #não devia ser i - self.fcm.k?
            
            entropies.append(-math.log2(fcm.probability_e_c(current_char, last_characters)))

            last_characters = last_characters[1:] + current_char
        return entropies


    def __repr__(self):
        return f'{self.name}'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--modeltext", metavar="modeltext", type=str, required=True,
                        help="File representing the class")
    parser.add_argument("--t", metavar="analysistext", type=str, required=True,
                        help="File to analyze")
    parser.add_argument("--alpha", metavar="alpha", type=float, required=False, default=1,
                        help="Variable responsible for smoothing")
    parser.add_argument("--k", metavar="sliding window", type=int, required=False, default=5,
                        help="Size of shifting window")
    return parser.parse_args()
        

if __name__ == '__main__':
    
    args = parse_args()
        
    lang = Lang('english', parameters= [(args.k, args.alpha)])
    lang.train(args.modeltext)
    file = open(args.t, 'r')
    text = ""
    for line in file.readlines():
        text += line
    
    num_bits = round(lang.amount_of_information(text, lang.fcm_list[0]), 3)
    print(f"Estimated number of bits required to compress t, using the computed model {args.modeltext}:\n{num_bits}")


    

