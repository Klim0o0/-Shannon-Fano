from pathlib import Path

from shannon_fano.decoder import Decoder
from shannon_fano.errors import DecompressorBrokenArchiveError, \
    DecompressorArchiveNotExistError


class Decompressor:

    def __init__(self, decoder: Decoder):
        self.decoder = decoder

    def decompress(self, archive_path: str, target_dir: str):
        archive = Path(archive_path)
        if not archive.exists():
            raise DecompressorArchiveNotExistError()
        archive_bytes = archive.read_bytes()
        files = self.decoder.decode(archive_bytes)
        broken_files = []
        for file in files:
            if file.data is None:
                broken_files.append(file.path)
                continue

            file_path = Path(target_dir + '\\' + file.path)
            parents = file_path.parents
            for i in range(len(parents) - 1, -1, -1):
                if not parents[i].exists():
                    parents[i].mkdir()
            file_path.write_bytes(file.data)
        if len(broken_files) != 0:
            raise DecompressorBrokenArchiveError(broken_files)
