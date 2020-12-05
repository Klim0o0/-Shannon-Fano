from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder

with open('q.txt', 'rb') as file:
    content = file.read()

encoded = ShannonFanoEncoder.encode(content, 'rq.txt')

with open('ar', 'wb') as file:
    file.write(encoded)

with open('ar', 'rb') as file:
    content = file.read()

decode = ShannonFanoDecoder.decode(content)
