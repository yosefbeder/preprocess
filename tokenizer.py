import re

from constants import DIACRITIC
from typing import List


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

    def tokenize(self) -> List[str]:
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
        return self.tokens


def tokenize(text: str) -> List[str]:
    return Tokenizer(text).tokenize()
