from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder

encoded = ShannonFanoEncoder.encode('Helow Wordl!  ' * 5)
decoded = ShannonFanoDecoder.decode(encoded)

print(encoded.encoded)
print(decoded.decoded)
