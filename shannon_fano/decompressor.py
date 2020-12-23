from hashlib import md5
from pathlib import Path
from typing import List

from shannon_fano.errors import DecompressorBrokenArchiveError, \
    DecompressorArchiveNotExistError, IsNotArchiveError, ArchiveError, \
    CantOpenArchive


class Decompressor:

    def __init__(self, decoder):
        self.decoder = decoder

    def decompress(self, archive_path: str,
                   target_dir: str,
                   files_for_decompress: List[str],
                   not_ignore_broken_files: bool):

        archive = Path(archive_path)
        if not Path(archive_path).is_file() or not Path(archive_path).exists():
            raise DecompressorArchiveNotExistError()
        try:
            with archive.open('rb') as archive_file:
                broken_files = self.decoder.decode(
                    self._get_file_len(archive_file), archive_file,
                    Path(target_dir),
                    set(files_for_decompress),
                    not_ignore_broken_files)
            if len(broken_files) != 0:
                raise DecompressorBrokenArchiveError(broken_files)
        except ArchiveError as e:
            raise e
        except OSError:
            raise CantOpenArchive()

    @staticmethod
    def _get_file_len(archive_file) -> int:
        head = archive_file.read(16)
        archive_file.seek(-16, 2)
        archive_file_size = archive_file.tell()
        tail = archive_file.read(16)
        archive_file.seek(16, 0)
        if md5(head).digest() != tail:
            raise IsNotArchiveError()
        return archive_file_size

    def get_file_names(self, archive_path: str):
        if not Path(archive_path).is_file() or not Path(archive_path).exists():
            raise DecompressorArchiveNotExistError()
        try:
            with Path(archive_path).open('rb') as archive_file:
                paths: List[str] = []
                for path in self.decoder.get_file_names(
                        self._get_file_len(archive_file),
                        archive_file):
                    paths.append(path + '\n')
            return ''.join(paths)
        except ArchiveError as e:
            raise e
        except OSError:
            raise CantOpenArchive()
