import collections
from typing import Dict

from bitarray import bitarray


class ShannonFanoEncoder:
    @classmethod
    def encode(cls, file_data: bytes, file_path: str) -> bytes:
        encoded_data: bitarray = bitarray()
        encoding_dictionary = cls.get_encoding_dictionary(file_data)
        encoded_data = cls._encode(file_data, file_path, encoding_dictionary)
        return encoded_data


    @classmethod
    def _encode(cls, file_data: bytes, file_path: str,
                encoding_dictionary) -> bitarray:
        encoded_data: bitarray = bitarray()
        file_name_bytes = bytes(file_path, 'utf-8')
        encoded_data.frombytes(bytes([len(file_name_bytes)]))
        encoded_data.frombytes(file_name_bytes)


        encoding_dictionary_data: bitarray = bitarray()
        for key in encoding_dictionary.keys():
            code = encoding_dictionary[key]
            encoding_dictionary_data.frombytes(bytes([key, len(code)]))
            encoding_dictionary_data.extend(code)

        encoded_data.extend(encoding_dictionary_data)


        encoded_data: bitarray = bitarray()
        for i in file_data:
            encoded_data.extend(encoding_dictionary[i])
        return encoded_data.tobytes()

    @classmethod
    def get_encoding_dictionary(cls, file_data: bytes) -> Dict[int, bitarray]:
        symbols = list(set(file_data))
        frequency: Dict[int:int] = cls.get_frequency(file_data)

        symbols.sort(key=lambda s: frequency[s])
        symbols.reverse()
        encoding_dictionary: Dict[int, bitarray] = {}
        cls.get_d(frequency,
                  symbols,
                  0,
                  len(symbols) - 1,
                  '',
                  encoding_dictionary,
                  len(file_data))
        return encoding_dictionary

    @classmethod
    def get_d(cls, frequency, symbols, start: int, end: int, code: str,
              d: Dict[int, bitarray], t):
        if start >= len(symbols):
            return
        if start == end + 1:
            d[symbols[start]] = bitarray(code + '1')
            d[symbols[start + 1]] = bitarray(code + '0')
            return

        if start == end:
            d[symbols[start]] = bitarray(code)
            return

        f = 0
        for i in range(start, end):
            f += frequency[symbols[i]]
            if f < int(t / 2 + 0.5):
                continue
            cls.get_d(frequency, symbols, start, i, code + '1', d, f)
            cls.get_d(frequency, symbols, i + 1, end, code + '0', d, t - f)
            break

    @classmethod
    def get_frequency(cls, file_data: bytes) -> Dict[int, int]:
        frequency: Dict[int, int] = collections.defaultdict(int)
        for i in file_data:
            frequency[i] += 1
        return frequency
