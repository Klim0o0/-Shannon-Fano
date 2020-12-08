import collections
from typing import Dict

from bitarray import bitarray
from hashlib import md5
from shannon_fano.encoder import Encoder


class ShannonFanoEncoder(Encoder):
    @classmethod
    def encode(cls, file_data: bytes, file_path: str) -> bytes:
        encoding_dictionary = cls.get_encoding_dictionary(file_data)
        encoded_data: bytes = cls._encode(file_data, file_path,
                                          encoding_dictionary)
        return encoded_data

    @classmethod
    def _encode(cls, file_data: bytes, file_path: str,
                encoding_dictionary) -> bytes:
        encode_data = bytearray()
        encode_data.extend(cls._get_file_path_data(file_path))
        encode_data.extend(cls._get_dictionary_data(encoding_dictionary))
        encode_data.extend(
            cls._get_encoded_file_data(file_data, encoding_dictionary))
        encode_data.extend(cls._compose_data(md5(file_data).digest()))
        return encode_data

    @classmethod
    def _get_encoded_file_data(cls, file_data: bytes,
                               encoding_dictionary) -> bytes:
        encoded_data: bitarray = bitarray()
        encoded_data.encode(encoding_dictionary, file_data)
        encoded_data_bytes = bytearray(encoded_data.tobytes())

        empty_bits_count = 8 - len(encoded_data) % 8
        if empty_bits_count == 8:
            empty_bits_count = 0

        encoded_data_bytes.append(empty_bits_count)
        return cls._compose_data(bytes(encoded_data_bytes))

    @classmethod
    def _get_file_path_data(cls, file_path) -> bytes:
        return cls._compose_data(bytes(file_path, 'utf-8'))

    @classmethod
    def _compose_data(cls, data: bytes):
        composed_data = bytearray()
        data_unit = bytearray()
        for byte in data:
            data_unit.append(byte)
            if len(data_unit) == 255:
                composed_data.append(255)
                composed_data.extend(data_unit)
                data_unit.clear()

        if len(data_unit) != 0:
            composed_data.append(len(data_unit))
            composed_data.extend(data_unit)
        composed_data.append(0)
        return composed_data

    @classmethod
    def _get_dictionary_data(cls, encoding_dictionary: [int, bitarray]):
        encoding_dictionary_data: bitarray = bitarray()

        for key in encoding_dictionary.keys():
            code = encoding_dictionary[key]
            encoding_dictionary_data.frombytes(bytes([key, len(code)]))
            encoding_dictionary_data.extend(code)

        return cls._compose_data(encoding_dictionary_data.tobytes())

    @classmethod
    def get_encoding_dictionary(cls, file_data: bytes) -> Dict[int, bitarray]:
        symbols = list(set(file_data))
        frequency: Dict[int:int] = cls.get_frequency(file_data)

        symbols.sort(key=lambda s: frequency[s])
        symbols.reverse()
        encoding_dictionary: Dict[int, bitarray] = {}

        cls.fill_encoding_dictionary(frequency,
                                     symbols,
                                     0,
                                     len(symbols) - 1,
                                     '',
                                     encoding_dictionary,
                                     len(file_data))
        return encoding_dictionary

    @classmethod
    def fill_encoding_dictionary(cls,
                                 frequency,
                                 symbols,
                                 start: int,
                                 end: int,
                                 code: str,
                                 encoding_dictionary: Dict[int, bitarray],
                                 length):

        if start >= len(symbols):
            return

        if start == end + 1:
            encoding_dictionary[symbols[start]] = bitarray(code + '1')
            encoding_dictionary[symbols[start + 1]] = bitarray(code + '0')
            return

        if start == end:
            encoding_dictionary[symbols[start]] = bitarray(code)
            return

        current_frequency = 0
        for i in range(start, end):
            current_frequency += frequency[symbols[i]]
            if current_frequency < int(length / 2 + 0.5):
                continue

            cls.fill_encoding_dictionary(frequency, symbols, start, i,
                                         code + '1', encoding_dictionary,
                                         current_frequency)
            cls.fill_encoding_dictionary(frequency, symbols, i + 1, end,
                                         code + '0', encoding_dictionary,
                                         length - current_frequency)
            break

    @classmethod
    def get_frequency(cls, file_data: bytes) -> Dict[int, int]:
        frequency: Dict[int, int] = collections.defaultdict(int)
        for i in file_data:
            frequency[i] += 1
        return frequency
