import re

from tokenizer import tokenize
from constants import PS_OR_PE, DIACRITIC
from typing import List


def normalize(tokens: List[str]) -> List[str]:
    normalized = []
    for token in tokens:
        # a diacritic that starts a word gets placed in a single token
        if re.match(PS_OR_PE, token) or re.match(DIACRITIC, token):
            continue
        # diacritics
        token = re.sub(DIACRITIC, '', token)
        # dots
        token = token.replace('ى', 'ي') \
            .replace('ة', 'ه')
        # alef typing mistakes
        token = re.sub(r'اا|ااا', 'ا', token)
        # alef
        token = re.sub(r'[أإآ]', 'ا', token)
        normalized.append(token)
    return normalized


print(tokenize("(السلام) [عليكم] {ورحمة} الله"))
print(normalize(tokenize("(السلام) [عليكم] {ورحمة} الله")))
print(normalize(tokenize("{هذا} «يوسف» عبد الفتاح")))
print(normalize(tokenize("أَهْلاً وسَهلاً بِكُم هلَّا")))
print(normalize(tokenize("ىأآإئؤة")))
