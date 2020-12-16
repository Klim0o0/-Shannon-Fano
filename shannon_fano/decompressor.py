from pathlib import Path
from typing import List

from shannon_fano.errors import DecompressorBrokenArchiveError, \
    DecompressorArchiveNotExistError


class Decompressor:

    def __init__(self, decoder):
        self.decoder = decoder

    def decompress(self, archive_path: str,
                   target_dir: str,
                   files_for_decompress: List[str],
                   not_ignore_broken_files: bool):
        archive = Path(archive_path)
        if not archive.exists():
            raise DecompressorArchiveNotExistError()
        with archive.open('rb') as archive_file:
            broken_files = self.decoder.decode(archive_file,
                                               Path(target_dir),
                                               set(files_for_decompress),
                                               not_ignore_broken_files)
        if len(broken_files) != 0:
            raise DecompressorBrokenArchiveError(broken_files)

    def get_file_names(self, archive_path: str):
        with open(archive_path, 'rb') as archive_file:
            for path in self.decoder.get_file_names(archive_file):
                print(path)
