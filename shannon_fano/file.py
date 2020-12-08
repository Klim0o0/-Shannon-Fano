class File:
    def __init__(self, path: str, data: bytes, hash: bytes):
        self.path = path
        self.data = data
        self.hash = hash
