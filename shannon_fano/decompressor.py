from pathlib import Path

from shannon_fano.encoder_decoder import Decoder
from shannon_fano.errors import DecompressorBrokenArchiveError, \
    DecompressorArchiveNotExistError


class Decompressor:

    def __init__(self, decoder: Decoder):
        self.decoder = decoder

    def decompress(self, archive_path: str, target_dir: str):
        archive = Path(archive_path)
        if not archive.exists():
            raise DecompressorArchiveNotExistError()
        broken_files = []
        with archive.open('rb') as archive_file:
            broken_files = self.decoder.decode(archive_file, Path(target_dir))
        if len(broken_files) != 0:
            raise DecompressorBrokenArchiveError(broken_files)
