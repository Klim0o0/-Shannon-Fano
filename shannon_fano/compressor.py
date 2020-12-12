import os
import queue
from pathlib import Path
from typing import List

from shannon_fano.encoder_decoder import Encoder
from shannon_fano.errors import CompressorFileNotExistError


class Compressor:
    def __init__(self, encoder: Encoder):
        self.encoder: Encoder = encoder

    def compress(self, targets: List[str], archive_name: str):

        if archive_name is None:
            archive_name = str(Path.cwd().joinpath(Path.cwd().name))
        archive_name += '.sf'
        archive_path = Path(archive_name)

        with archive_path.open('wb') as archive_file:
            targets_paths: List[Path] = []
            for target in targets:
                target_path = Path(target)
                if not target_path.exists():
                    raise CompressorFileNotExistError()
                targets_paths.append(target_path)

            for target_path in targets_paths:
                for file_path in self.collect_files(target_path):
                    with file_path.open('rb') as file:
                        self.encoder.encode(file, archive_file,
                                            self.get_relative_path(
                                                target_path,
                                                file_path))

        return True

    @classmethod
    def get_relative_path(cls, folder_path: Path, file_path: Path) -> str:
        if folder_path == file_path:
            return file_path.name

        relative_path: List[str] = []
        for item in file_path.parts[len(folder_path.parts) - 1::]:
            relative_path.append('/' + item)
        return ''.join(relative_path)

    @classmethod
    def collect_files(cls, target: Path) -> List[Path]:

        if target.is_file():
            return [target]

        for address, dirs, files in os.walk(str(target)):
            for file in files:
                yield Path(address + '/' + file)
