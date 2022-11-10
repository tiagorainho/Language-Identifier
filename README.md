# Language Identifier

## Introduction

A Finite-Context model (FCM) is a type of Markov model, and with this model it is possible to collect statistical information from texts. This project’s main goal is to use one or more FCM to determine the similarity between a given corpus of reference texts and a target text. By calculating the similarity, it is possible to analyze in which language or languages a text was written and where the segments of the languages are located in the text. To do this, the FCM models serve as descriptions for each language so that it can be estimated how many bits would be required to compress sample texts when compared to these models. The language of the model that will require the less amount of bits will most likely be the language in which the sample text is written, since the model requires fewer bits to describe this text.

To be able to obtain this goal, three different modules were developed. The first one, lang, serves as a building point for the FCM models representing each language and can compare a sample text with a model text to estimate how many bits it would be required to compress the sample text. The second module, findlang, expands on the previous module to determine in what language a sample text was written. Lastly, the third module, locatelang analyzes a sample text and finds the language in which different segments of the text were written.

For more information read the report in ``delivery/report/report.pdf``.

## How to run

### Lang Module

```
python3 src/lang.py --files dataset/eng_AU.latn.Aboriginal_English.comb-train.utf8 
  --k 10 --alpha 0.5 --t test_files/english_text.txt
```

### Find Lang Module

```
python3 src/findlang.py --file test_files/english_text.txt --k 3 4 5 --alpha
   0.1 0.2 0.3 --threshold 4 --languages portuguese english spanish
```

### Locate Lang Module

```
python3 src/locatelang.py --file test_files/polish_texto_exemplo.txt
   --threshold 4 --show True
```


