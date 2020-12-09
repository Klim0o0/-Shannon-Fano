import unittest
from pathlib import Path
from random import randint

from shannon_fano.compressor import Compressor
from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder


class EncoderDecoderTests(unittest.TestCase):

    def setUp(self):
        self.encoder = ShannonFanoEncoder
        self.decoder = ShannonFanoDecoder

    def test_encode_decode(self):
        for i in range(100):
            source = bytearray()
            for j in range(15):
                source.extend(bytes(range(randint(0, 256))))

            source_file_path = 'qwe.txt'
            decoded = self.decoder.decode(
                self.encoder.encode(source, source_file_path))
            self.assertEqual(1, len(decoded))
            self.assertEqual(source, decoded[0].data)
            self.assertEqual(source_file_path, decoded[0].path)


if __name__ == '__main__':
    unittest.main()
