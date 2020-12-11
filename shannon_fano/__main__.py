import argparse
import logging

from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.compressor import Compressor
from shannon_fano.errors import DecompressorArchiveNotExistError, \
    CompressorEmptyFilesError, DecompressorBrokenArchiveError, \
    CompressorFileNotExistError


def parser_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_append_compile = subparsers.add_parser('compress',
                                                  help='select .txt file'
                                                       ' with puzzle'
                                                       ' and puzzle type')

    parser_append_compile.set_defaults(function=compress)

    parser_append_compile.add_argument('archivename',
                                       help='Name for your archive (optional)',
                                       nargs='?')
    parser_append_compile.add_argument('files',
                                       help='List of files you'
                                            ' want to compress',
                                       nargs='+')
    parser_append_compile = subparsers.add_parser('decompress',
                                                  help='Decompress an archive')

    parser_append_compile.add_argument('archive', help='Archive to decompress')
    parser_append_compile.add_argument('target_folder',
                                       help='Folder to decompress')

    parser_append_compile.set_defaults(function=decompress)

    args = parser.parse_args()
    if 'function' not in args:
        print('select compress/decompress')
        return
    try:
        args.function(args)
    except KeyboardInterrupt:
        print('Interrupt compress')
    except CompressorEmptyFilesError as e:
        print(e.message)
    except CompressorFileNotExistError as e:
        print(e.message)
    except DecompressorArchiveNotExistError as e:
        print(e.message)
    except DecompressorBrokenArchiveError as e:
        print(e.message + '\nBroken files: ' + str(e.broken_files))


def compress(args):
    compressor = Compressor(ShannonFanoEncoder())
    compressor.compress(args.files, args.archivename)


def decompress(args):
    decompressor = Decompressor(ShannonFanoDecoder())
    decompressor.decompress(args.archive, args.target_folder)


if __name__ == '__main__':
    parser_arguments()
