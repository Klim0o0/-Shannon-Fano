import queue
from pathlib import Path
from typing import List, Set

from shannon_fano.encoder import Encoder


class Compressor:
    def __init__(self, encoder: Encoder):
        self.encoder: Encoder = encoder

    def compress(self, targets: List[str]):
        encoded_data = bytearray()
        targets_paths: List[Path] = []
        for target in targets:
            targets_paths.append(Path(target))
        files_paths: List[Path] = self.collect_files(targets_paths)
        for file_path in files_paths:
            with file_path.open('rb') as file:
                p=file.read()
                print(p)
                print(file)
                encoded_data.extend(
                    self.encoder.encode(p, str(file_path.parts)))
        return encoded_data

    @classmethod
    def collect_files(cls, targets: List[Path]) -> List[Path]:
        files: List[Path] = []
        dirs: queue.Queue[Path] = queue.Queue()
        for target in targets:
            if target.is_dir():
                dirs.put(target)
            else:
                files.append(target)

        while not dirs.empty():
            directory = dirs.get()
            if directory.is_dir():
                for sub_dir in directory.glob('*'):
                    dirs.put(sub_dir)
            else:
                files.append(directory)

        return files
