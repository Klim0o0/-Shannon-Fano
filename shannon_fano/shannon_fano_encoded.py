from typing import *
from collections import defaultdict


class ShannonFanoEncoded:
    def __init__(self, text: str):
        self.dictionary: Dict[str, str] = self.get_dictionary(text)
        self.encoded: str = self.encode(text, self.dictionary)

    @classmethod
    def get_dictionary(cls, text) -> Dict[str, str]:
        frequency: Dict[str:int] = defaultdict(int)
        for i in text:
            frequency[i] += 1

        return {}

    @classmethod
    def encode(cls, text, dictionary) -> str:
        return ""
