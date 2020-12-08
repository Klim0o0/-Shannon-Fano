from hashlib import md5
from pathlib import Path

from bitarray import bitarray

from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.compressor import Compressor

comperessor = Compressor(ShannonFanoEncoder())
comperessor.compress(
    [Path('D:/ЯТП/Шпора/Пары/di/TagCloud/bin/Debug/')], 's')

decompressor = Decompressor(ShannonFanoDecoder())
print(decompressor.decompress('s.sf', '.'))
