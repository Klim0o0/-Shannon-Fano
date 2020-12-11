class CompressorEmptyFilesError(BaseException):
    message = 'error: empty files'


class CompressorFileNotExistError(BaseException):
    message = 'error: empty files'


class DecompressorBrokenArchiveError(BaseException):
    message = 'error: archive is broken, cannot be decompressed'

    def __init__(self, broken_files):
        self.broken_files = broken_files


class DecompressorArchiveNotExistError(BaseException):
    message = 'error: archive not exist'
