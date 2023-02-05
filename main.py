from tokenizer import tokenize, TokenStream
from normalizer import normalize
from ordered_set import OrderedSet
import re


def preprocess(text: str) -> OrderedSet[TokenStream]:
    sentences = OrderedSet()
    # todo: recognize floating point numbers
    for sentence in re.split(r'[؟!.،:؛]', text):
        sentences.add(normalize(tokenize(sentence)))
    return sentences


for tokens in preprocess("السلام عليكم، السلام عليكم، أنا يوسف، هل تسمعني؟"):
    print(tokens)
