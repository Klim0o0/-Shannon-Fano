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
        for target_path in targets_paths:
            for file_path in self.collect_files(target_path):
                with file_path.open('rb') as file:
                    p = file.read()
                    encoded_data.extend(
                        self.encoder.encode(p,
                                            self.get_relative_path(target_path,
                                                                   file_path)))

        return encoded_data

    @classmethod
    def get_relative_path(cls, path1: Path, path2: Path) -> str:
        if path1 == path2:
            return path2.name

        s = ''
        for item in path2.parts[len(path1.parts) - 1::]:
            s += '/' + item
        return s

    @classmethod
    def collect_files(cls, target: Path) -> List[Path]:
        files: List[Path] = []
        dirs: queue.Queue[Path] = queue.Queue()
        dirs.put(target)

        while not dirs.empty():
            directory = dirs.get()
            if directory.is_dir():
                for sub_dir in directory.glob('*'):
                    dirs.put(sub_dir)
            else:
                files.append(directory)

        return files
