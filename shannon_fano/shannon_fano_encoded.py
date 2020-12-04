from typing import *


class ShannonFanoEncoded:
    def __init__(self, encoded: str, encoding_dictionary: Dict[str, str]):
        self.encoded = encoded
        self.encoding_dictionary = encoding_dictionary
