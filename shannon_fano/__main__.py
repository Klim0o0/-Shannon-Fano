import argparse
import logging

from shannon_fano.decompressor import Decompressor
from shannon_fano.encoder_decoder import ShannonFanoEncoder
from shannon_fano.encoder_decoder import ShannonFanoDecoder
from shannon_fano.compressor import Compressor
from shannon_fano.errors import ArchiveError


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
        exit(1)
    return args


def compress(args):
    compressor = Compressor(ShannonFanoEncoder())
    compressor.compress(args.files, args.archivename)


def decompress(args):
    decompressor = Decompressor(ShannonFanoDecoder())
    decompressor.decompress(args.archive, args.target_folder)


if __name__ == '__main__':
    arguments = parser_arguments()
    try:
        arguments.function(arguments)
    except KeyboardInterrupt:
        print('Interrupt compress')
    except ArchiveError as e:
        print(e.message)
