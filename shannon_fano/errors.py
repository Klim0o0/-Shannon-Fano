class ArchiveError(Exception):
    message: str


class CompressorEmptyFilesError(ArchiveError):
    message = 'error: empty files'


class CompressorFileNotExistError(ArchiveError):
    message = 'error: empty files'


class DecompressorBrokenArchiveError(ArchiveError):
    message = 'error: archive is broken, cannot be decompressed'

    def __init__(self, broken_files):
        self.message += str(broken_files)


class DecompressorArchiveNotExistError(ArchiveError):
    message = 'error: archive not exist'
