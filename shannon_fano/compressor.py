import os
from hashlib import md5
from pathlib import Path
from random import randint
from typing import List

from shannon_fano.errors import CompressorFileNotExistError


class Compressor:
    def __init__(self, encoder):
        self.encoder = encoder

    def compress(self, targets: List[str], archive_name: str):

        if archive_name is None:
            archive_name = Path(targets[0]).stem
        archive_path = Path(archive_name)

        targets_paths: List[Path] = []
        for target in targets:
            target_path = Path(target)
            if not target_path.exists():
                raise CompressorFileNotExistError()
            targets_paths.append(target_path)
        head = bytes(randint(0, 255) for i in range(16))
        tail = md5(head).digest()

        with archive_path.open('wb') as archive_file:
            archive_file.write(head)
            for target_path in targets_paths:
                for file_path in self.collect_files(target_path):
                    with file_path.open('rb') as file:
                        self.encoder.encode(file, archive_file,
                                            str(file_path.relative_to(
                                                target_path.parent)))
            archive_file.write(tail)

    @classmethod
    def collect_files(cls, target: Path) -> List[Path]:
        if target.is_file():
            yield target

        for address, dirs, files in os.walk(str(target)):
            for file in files:
                yield Path(address) / file
