from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder

with open('q.txt', 'rb') as file:
    content = file.read()

encoded = ShannonFanoEncoder.encode(content, '1.txt')

with open('ar', 'wb') as file:
    file.write(encoded)
