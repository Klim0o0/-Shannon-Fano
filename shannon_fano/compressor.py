import queue
from pathlib import Path
from typing import List

from shannon_fano.encoder import Encoder
from shannon_fano.errors import CompressorEmptyFilesError, \
    CompressorFileNotExistError


class Compressor:
    def __init__(self, encoder: Encoder):
        self.encoder: Encoder = encoder

    def compress(self, targets: List[str], archive_name: str):

        if archive_name is None:
            archive_name = str(Path.cwd().joinpath(Path.cwd().name))
        archive_name += '.sf'
        encoded_data = bytearray()

        targets_paths: List[Path] = []
        for target in targets:
            target_path = Path(target)
            if not target_path.exists():
                raise CompressorFileNotExistError()
            targets_paths.append(target_path)

        for target_path in targets_paths:
            for file_path in self.collect_files(target_path):
                encoded_data.extend(
                    self.encoder.encode(file_path.read_bytes(),
                                        self.get_relative_path(target_path,
                                                               file_path)))

        archive_path = Path(archive_name)
        if len(encoded_data) != 0:
            archive_path.write_bytes(encoded_data)
            return 'done'
        raise CompressorEmptyFilesError()

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
