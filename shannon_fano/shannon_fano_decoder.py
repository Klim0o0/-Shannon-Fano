from typing import Tuple, List
from bitarray import bitarray


class ShannonFanoDecoder:

    @classmethod
    def decode(cls, archive_data: bytes):
        index = 0
        data_list: List[bytes] = []
        while index < len(archive_data):
            data = cls.get_data(archive_data, index)
            index = data[1]+1
            data_list.append(data[0])
        print(1)
        for i in data_list:
            print(i)
        file_path_data = data_list[0]
        decoding_dictionary = cls.get_decoding_dictionary(data_list[1])

    @classmethod
    def get_decoding_dictionary(cls, encoding_dictionary_data: bytes):
        encoding_dictionary_bits = bitarray(encoding_dictionary_data)
        index = 0

        while len(encoding_dictionary_bits) - index > 7:
            pass


    @classmethod
    def get_data(cls, archive_data: bytes, index: int) -> Tuple[bytes, int]:
        data = bytearray()
        while archive_data[index] != 0:
            for i in range(1, archive_data[index] + 1):
                data.append(archive_data[index + i])
            index += archive_data[index] + 1
        return data, index
