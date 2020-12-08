from pathlib import Path

from shannon_fano.decoder import Decoder


class Decompressor:

    def __init__(self, decoder: Decoder):
        self.decoder = decoder

    def decompress(self, archive_path: str, target_dir: str):
        archive = Path(archive_path)
        if not archive.exists():
            return -1
        archive_bytes = archive.read_bytes()
        files = self.decoder.decode(archive_bytes)
        print(len(files))
        dirs = []
        for file in files:
            file_path = Path(target_dir+'/'+file[1])
            parents=file_path.parents
            for i in range(len(parents)-1,-1,-1):
                if not parents[i].exists():
                    parents[i].mkdir()
            file_path.write_bytes(file[0])
        return 0
