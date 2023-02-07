from tokenizer import tokenize, TokenStream
from normalizer import normalize
from typing import List
from constants import SENTENCE_TERMINATOR
import re


def preprocess(text: str) -> List[TokenStream]:
    tokens = normalize(tokenize(text))
    sentences = []
    n = 0
    offset = 0
    i = 0
    while i < len(tokens):
        if re.match(SENTENCE_TERMINATOR, tokens[i]) or i == len(tokens) - 1:
            current = tokens[offset:i + 1]
            if n == 0 or current != sentences[n - 1]:
                sentences.append(current)
                n += 1
            offset = i + 1
        i += 1
    return sentences


def main():
    for sentence in preprocess("السلام عليكم، السلام عليكم، أنا يوسف، هل تسمعني؟"):
        print(sentence)


main()
