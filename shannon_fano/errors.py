class ArchiveError(Exception):
    message: str


class CantCreateArchive(ArchiveError):
    message = 'can\' create archive'


class CantWriteInArchiveOrCantReadSomeFile(ArchiveError):
    message = 'can\'t write in archive or cant read file'


class CantCreateFile(ArchiveError):
    message = 'can\' create archive'


class CantOpenArchive(ArchiveError):
    message = 'can\' open archive'


class IsNotArchiveError(ArchiveError):
    message = 'error: is not archive'


class CompressorEmptyFilesError(ArchiveError):
    message = 'error: empty files'


class CompressorFileNotExistError(ArchiveError):
    message = 'error:files not exist'


class DecompressorBrokenArchiveError(ArchiveError):
    message = 'error: archive is broken, cannot be decompressed'

    def __init__(self, broken_files):
        self.message += str(broken_files)


class DecompressorArchiveNotExistError(ArchiveError):
    message = 'error: archive not exist'
