
import math
from argparse import ArgumentParser
from typing import Dict, List, Set

# Finite Context Model
class FCM:


    def __init__(self, k:int, alpha:float, alphabet:str=''):
        self.finitecontext: Dict[str, List[str, int]] = dict()
        self.k: int = k
        self.alpha: float = alpha
        self.characters: Set[chr] = set(alphabet)
        self.cardinality:int = len(self.characters)


    def update(self, text: str):
        self.load_alphabet(text)
        self.cardinality = len(self.characters)
        last_characters = text[:self.k]
        for i in range(self.k, len(text)):
            current_char = text[i]
            # add to finite context model
            occurences = self.finitecontext.get(last_characters)
            if occurences != None:
                found = False
                for tpl in occurences:
                    if tpl[0] == current_char:
                        found = True
                        new_tpl = (tpl[0], tpl[1]+1)
                        occurences.remove(tpl)
                        # insert in the beginning because its more probable to find in the next search
                        occurences.insert(0, new_tpl)
                        break
                if not found:
                    # insert in the end because its probable not commom
                    occurences.append((current_char,1))
            else:
                self.finitecontext[last_characters] = [(current_char,1)]
            last_characters = last_characters[1:] + current_char


    def load_alphabet(self, text:str):
        self.characters = self.characters.union(set(text))


    def probability_e_c(self, event: str, context: str):
        Psc = Nec = 0
        tuple_list = self.finitecontext.get(context)
        if tuple_list == None: return 1/self.cardinality
        for t in tuple_list:
            Psc += t[1]
            if t[0] == event:
                Nec = t[1]
        return (Nec + self.alpha) / (Psc + self.alpha * self.cardinality)


    def calculate_entropy(self):
        H = 0
        # calculate sum of all Psc
        sum_Psc = sum([t[1] for tuple_list in self.finitecontext.values() for t in tuple_list])
        for context, tuple_list in self.finitecontext.items():
            Hc = Pec = 0
            Psc = sum(t[1] for t in tuple_list)
            for t in tuple_list:
                Pec = (t[1] + self.alpha) / (Psc + self.alpha * self.cardinality)
                information_amount = - math.log2(Pec)
                Hc += information_amount * Pec
            if self.alpha != 0 and self.cardinality > len(tuple_list):
                # in case there are 0 occurences, calculate Pec for 0
                Pec = (self.alpha) / (Psc + self.alpha * self.cardinality)
                information_amount = - math.log2(Pec)
                # multiply by number of null cells (0 occurences) of the context row
                Hc += (information_amount * Pec) * (self.cardinality - len(tuple_list))
            H += Hc * Psc/sum_Psc
        return H


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--files", metavar="files", nargs="+", type=str, required=True,
                        help="List of files to train the model")
    parser.add_argument("--alpha", metavar="alpha", type=float, required=False, default=1,
                        help="Variable responsible for smoothing")
    parser.add_argument("--k", metavar="k", type=int, required=False, default=5,
                        help="Size of shifting window")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    fcm = FCM(k=args.k, alpha=args.alpha)
    for file in args.files:
        with open(file) as f:
            print(f"Reading file {f.name}")
            fcm.update(f.read())

    print(f"Calculating entropy")
    print(f"Entropy: { fcm.calculate_entropy() }")

