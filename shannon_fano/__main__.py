from pathlib import Path

from bitarray import bitarray
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.compresor import Compressor

with open('TagCloud.exe', 'rb') as file:
    content = file.read()

encoded = ShannonFanoEncoder.encode(content, '2TagCloud.exe')

with open('ar', 'wb') as file:
    file.write(encoded)

with open('ar', 'rb') as file:
    content = file.read()

decode = ShannonFanoDecoder.decode(encoded)

with open(decode[1], 'wb') as file:
    file.write(decode[0])
print('done')
comperessor = Compressor(ShannonFanoEncoder())
encoded = comperessor.compress(
    [Path('D:\\ЯТП\\Шпора\\Пары\\di\\TagCloud\\bin\\Debug')])

with open('s', 'wb') as file:
    file.write(encoded)
