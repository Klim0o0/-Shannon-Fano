import os
from pathlib import Path
from typing import List

from shannon_fano.errors import CompressorFileNotExistError


class Compressor:
    def __init__(self, encoder):
        self.encoder = encoder

    def compress(self, targets: List[str], archive_name: str):

        if archive_name is None:
            archive_name = Path(targets[0]).stem
        archive_name += '.sf'
        archive_path = Path(archive_name)

        targets_paths: List[Path] = []
        for target in targets:
            target_path = Path(target)
            if not target_path.exists():
                raise CompressorFileNotExistError()
            targets_paths.append(target_path)

        with archive_path.open('wb') as archive_file:
            for target_path in targets_paths:
                for file_path in self.collect_files(target_path):
                    with file_path.open('rb') as file:
                        self.encoder.encode(file, archive_file,
                                            str(file_path.relative_to(
                                                target_path.parent)))

    @classmethod
    def collect_files(cls, target: Path) -> List[Path]:
        if target.is_file():
            yield target

        for address, dirs, files in os.walk(str(target)):
            for file in files:
                yield Path(address) / file
