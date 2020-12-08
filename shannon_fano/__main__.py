import argparse
from hashlib import md5
from pathlib import Path

from bitarray import bitarray

from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.compressor import Compressor


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
    args.function(args)


def compress(args):
    compressor = Compressor(ShannonFanoEncoder())
    compressor.compress(args.files, args.archivename)


def decompress(args):
    decompressor = Decompressor(ShannonFanoDecoder())
    broken_files = decompressor.decompress(args.archive, args.target_folder)
    if len(broken_files) != 0:
        print('Archive have broken files')
        print(broken_files)
    else:
        print('Decompress done')


if __name__ == '__main__':
    parser_arguments()
