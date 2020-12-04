from shannon_fano.shannon_fano_decoded import ShannonFanoDecoded
from shannon_fano.shannon_fano_encoded import ShannonFanoEncoded
from typing import *


class ShannonFanoDecoder:
    @classmethod
    def decode(cls, encoded: ShannonFanoEncoded) -> ShannonFanoDecoded:
        return ShannonFanoDecoded(cls._decode(encoded.encoded,
                                              cls.get_decode_dictionary(
                                                  encoded.encoding_dictionary)))

    @classmethod
    def _decode(cls, encoded: str, decode_dictionary: Dict[str, str]):
        res = ''
        temp = ''
        for i in encoded:
            temp += i
            if temp in decode_dictionary.keys():
                res += decode_dictionary[temp]
                temp = ''
        return res

    @classmethod
    def get_decode_dictionary(cls, encode_dictionary: Dict[str, str]):
        decode_dictionary: Dict[str, str] = {}
        for i in encode_dictionary.keys():
            decode_dictionary[encode_dictionary[i]] = i
        return decode_dictionary
