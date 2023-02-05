import re

from constants import DIACRITIC
from typing import List


class TokenStream:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    def __hash__(self):
        prime = 31
        result = 1
        for token in self.tokens:
            result = result * prime + hash(token)
        return result

    def __eq__(self, other):
        if self is other:
            return True
        length = len(self.tokens)
        if length != len(other.tokens):
            return False
        for i in range(0, length):
            if self.tokens[i] != other.tokens[i]:
                return False
        return True

    def __iter__(self):
        return iter(self.tokens)

    def __str__(self):
        return str(self.tokens)


class Tokenizer:
    def __init__(self, text: str):
        self.start = 0
        self.current = 0
        self.text = text
        self.tokens = []

    def consume(self):
        self.current += 1
        return self.cur_char()

    def get(self, idx: int):
        if idx >= len(self.text):
            return None
        return self.text[idx]

    # note: can return None
    def peek(self, amount: int):
        return self.get(self.current + amount)

    def pop(self):
        self.tokens.append(self.text[self.start:self.current])
        self.start = self.current

    def skip(self):
        self.consume()
        self.start = self.current

    def cur_char(self):
        return self.get(self.current)

    def at_end(self):
        return self.current >= len(self.text)

    def tokenize(self) -> TokenStream:
        while True:
            # whitespaces and newlines
            cur = self.cur_char()
            if cur is None:
                break
            if re.match('\\s', cur) is not None:
                self.skip()
            # words
            elif cur.isalpha():
                self.consume()
                while True:
                    cur = self.cur_char()
                    if cur is None:
                        break
                    if not cur.isalpha() and re.match(DIACRITIC, cur) is None:
                        break
                    self.consume()
                self.pop()
            # numbers and floats
            elif cur.isdigit():
                self.consume()
                while True:
                    cur = self.cur_char()
                    if cur is None:
                        break
                    if not cur.isdigit():
                        break
                    self.consume()
                if cur == '.':
                    following = self.peek(1)
                    if following is not None and following.isdigit():
                        cur = self.consume()  # '.'
                        self.consume()  # consider omitting it
                        while True:
                            cur = self.cur_char()
                            if cur is None:
                                break
                            if not cur.isdigit():
                                break
                            self.consume()
                self.pop()
            # floats starting with '.'
            elif cur == '.':
                cur = self.consume()
                if cur is None:
                    pass
                elif cur.isdigit():
                    while True:
                        cur = self.cur_char()
                        if cur is None:
                            break
                        if not cur.isdigit():
                            break
                        self.consume()
                self.pop()
                # punctuation marks
            else:
                self.consume()
                self.pop()
        return TokenStream(self.tokens)


def tokenize(text: str) -> TokenStream:
    return Tokenizer(text).tokenize()
