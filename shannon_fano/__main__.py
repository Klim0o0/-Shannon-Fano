from pathlib import Path

from bitarray import bitarray

from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.compressor import Compressor

with open('../ar_t/t1.txt', 'rb') as file:
    content = file.read()

encoded = ShannonFanoEncoder.encode(content, '2TagCloud.exe')

with open('ar', 'wb') as file:
    file.write(encoded)

with open('ar', 'rb') as file:
    content = file.read()

decode = ShannonFanoDecoder.decode(encoded)

print('done')
comperessor = Compressor(ShannonFanoEncoder())
encoded = comperessor.compress(
    [Path('../ar_t')])

with open('s', 'wb') as file:
    file.write(encoded)

decompressor = Decompressor(ShannonFanoDecoder())
print(decompressor.decompress('s', './secret'))
