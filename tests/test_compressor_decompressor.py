import unittest
from pathlib import Path

from shannon_fano.compressor import Compressor
from shannon_fano.decompressor import Decompressor
from shannon_fano.encoder_decoder import ShannonFanoDecoder
from shannon_fano.encoder_decoder import ShannonFanoEncoder


class CompressorDecompressorTests(unittest.TestCase):

    def setUp(self):
        self.compressor = Compressor(ShannonFanoEncoder())
        self.decompressor = Decompressor(ShannonFanoDecoder())

        self.original_file1 = Path('./folder_to_compress/f1.txt')
        self.original_file2 = Path('./folder_to_compress/sub_folder/f2.txt')
        self.parent_folder = Path('./decompressed/folder_to_compress')
        self.sub_folder = Path('./decompressed/folder_to_compress/sub_folder')
        self.file1 = Path('./decompressed/folder_to_compress/f1.txt')
        self.file2 = Path(
            './decompressed/folder_to_compress/sub_folder/f2.txt')

        self.create_folders_for_file(self.original_file1)
        self.create_folders_for_file(self.original_file2)
        self.original_file1.write_bytes(bytes(range(256)))
        self.original_file2.write_bytes(bytes(range(256)))

    @staticmethod
    def create_folders_for_file(path: Path):
        if not path.parent.exists():
            path.parent.mkdir(parents=True)

    def test_compress_decompress(self):
        self.compressor.compress(['./folder_to_compress'], 'archive')
        self.decompressor.decompress('./archive.sf', './decompressed',
                                     [],
                                     True)

        self.assertTrue(self.parent_folder.exists())
        self.assertTrue(self.sub_folder.exists())
        self.assertTrue(self.original_file1.exists())
        self.assertTrue(self.original_file2.exists())
        self.assertTrue(self.file1.exists())
        self.assertTrue(self.file2.exists())
        self.assertEqual(self.original_file1.read_bytes(),
                         self.file1.read_bytes())
        self.assertEqual(self.original_file2.read_bytes(),
                         self.file2.read_bytes())

    def test_compress_decompress_some_files(self):
        self.compressor.compress(['./folder_to_compress'], 'archive')
        self.decompressor.decompress('./archive.sf', './decompressed', [
            str(Path('folder_to_compress') / self.original_file1.name)], True)

        self.assertTrue(self.parent_folder.exists())
        self.assertFalse(self.sub_folder.exists())
        self.assertTrue(self.original_file1.exists())
        self.assertTrue(self.original_file2.exists())
        self.assertTrue(self.file1.exists())
        self.assertFalse(self.file2.exists())
        self.assertEqual(self.original_file1.read_bytes(),
                         self.file1.read_bytes())

    def test_get(self):
        self.compressor.compress(['./folder_to_compress'], 'archive')

        self.assertEqual(self.decompressor.get_file_names('./archive.sf'),
                         str(Path('folder_to_compress/f1.txt'))
                         + '\n'
                         + str(Path('folder_to_compress/sub_folder/f2.txt'))
                         + '\n')

    def tearDown(self):
        self.remove_if_exist(Path('./archive.sf'))
        self.remove_if_exist(self.file1)
        self.remove_if_exist(self.file2)
        self.remove_if_exist(self.original_file1)
        self.remove_if_exist(self.original_file2)
        self.remove_if_exist(self.sub_folder)
        self.remove_if_exist(self.parent_folder)
        self.remove_if_exist(Path('./folder_to_compress/sub_folder'))
        self.remove_if_exist(Path('./folder_to_compress/'))
        self.remove_if_exist(Path('./decompressed'))

    @staticmethod
    def remove_if_exist(path: Path):
        if not path.exists():
            return
        if path.is_file():
            path.unlink()
        else:
            path.rmdir()


if __name__ == '__main__':
    unittest.main()
