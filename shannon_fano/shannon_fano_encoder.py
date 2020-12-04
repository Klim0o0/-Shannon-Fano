from shannon_fano.shannon_fano_encoded import ShannonFanoEncoded
from collections import defaultdict
from typing import *


class ShannonFanoEncoder:
    @classmethod
    def encode(cls, text: str) -> ShannonFanoEncoded:
        encoding_dictionary: Dict[str, str] = cls.get_encoding_dictionary(text)
        encoded: str = cls._encode(text, encoding_dictionary)
        return ShannonFanoEncoded(encoded, encoding_dictionary)

    @classmethod
    def get_encoding_dictionary(cls, text) -> Dict[str, str]:
        symbols = list(set(text))
        frequency: Dict[str:int] = defaultdict(int)
        for symbol in text:
            frequency[symbol] += 1

        for symbol in frequency.keys():
            frequency[symbol] /= len(text)
        symbols.sort(key=lambda s: frequency[s])
        symbols.reverse()
        encoding_dictionary = {}
        cls.get_d(frequency,
                  symbols,
                  0,
                  len(symbols),
                  '',
                  encoding_dictionary,
                  1)
        return encoding_dictionary

    @classmethod
    def get_d(cls, frequency, symbols, start: int, end: int, code: str,
              d: Dict[str, str], t):
        if start >= len(symbols):
            return
        if start == end:
            d[symbols[start]] = code
            return

        f = 0
        for i in range(start, end):
            f += frequency[symbols[i]]
            if f < t / 2:
                continue
            cls.get_d(frequency, symbols, start, i, code + '1', d, f)
            cls.get_d(frequency, symbols, i + 1, end, code + '0', d, t - f)
            break

    @classmethod
    def _encode(cls, text, encode_dictionary) -> str:
        encoded = ''
        for symbol in text:
            encoded += encode_dictionary[symbol]
        return encoded
