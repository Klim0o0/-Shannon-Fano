import unittest
from pathlib import Path

from shannon_fano.compressor import Compressor
from shannon_fano.decompressor import Decompressor
from shannon_fano.shannon_fano_decoder import ShannonFanoDecoder
from shannon_fano.shannon_fano_encoder import ShannonFanoEncoder


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

        self.create_folders(self.original_file1)
        self.create_folders(self.original_file2)
        self.original_file1.write_bytes(bytes(range(256)))
        self.original_file2.write_bytes(bytes(range(256)))

    def create_folders(self, path: Path):
        parents = path.parents
        for i in range(len(parents) - 1, -1, -1):
            if not parents[i].exists():
                parents[i].mkdir()

    def test_compress_decompress(self):
        self.compressor.compress(['./folder_to_compress'], 'archive')
        self.decompressor.decompress('./archive.sf', './decompressed')

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

        Path('./archive.sf').unlink()
        self.file1.unlink()
        self.file2.unlink()
        self.original_file1.unlink()
        self.original_file2.unlink()
        self.sub_folder.rmdir()
        self.parent_folder.rmdir()
        Path('./folder_to_compress/sub_folder').rmdir()
        Path('./folder_to_compress/').rmdir()
        Path('./decompressed').rmdir()


if __name__ == '__main__':
    unittest.main()
