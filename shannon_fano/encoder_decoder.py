import collections
from hashlib import md5
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import List, Tuple, Dict
from bitarray import bitarray

from shannon_fano.file import File


class Decoder:

    @classmethod
    def decode(cls, archive_file, target_foldr: Path) -> \
            List[File]:
        pass


class Encoder:

    @classmethod
    def encode(cls, file, archive_file, file_path: str) -> bytes:
        pass


class ShannonFanoDecoder(Decoder):

    @classmethod
    def decode(cls, archive_file: BufferedReader, target_foldr: Path):
        broken_files = []
        while True:
            file_path_data = cls._get_data(archive_file)
            if not file_path_data:
                break
            file_path = target_foldr / cls.get_file_path(file_path_data)

            if not target_foldr.exists():
                target_foldr.mkdir(parents=True)

            decoding_dictionary = cls.get_decoding_dictionary(
                cls._get_data(archive_file))

            control_sum = cls._get_data(archive_file)

            if (cls.decode_and_write_file(archive_file, Path(file_path),
                                          control_sum,
                                          decoding_dictionary)):
                broken_files.append(file_path)
        return broken_files

    @classmethod
    def decode_and_write_file(cls, archive_file: BufferedReader,
                              file_path: Path,
                              control_sum: bytes,
                              decoding_dictionary: Dict[Tuple[bool], bytes]):
        current_control_sum = md5()

        with file_path.open('wb') as file:
            bit_buffer = bitarray()
            byte = archive_file.read(1)
            while byte[0] != 0:
                archive_byte_buffer = archive_file.read(byte[0])
                byte = archive_file.read(1)

                empty_bits = 0
                if byte[0] == 0:
                    empty_bits = archive_byte_buffer[-1]
                    archive_byte_buffer = archive_byte_buffer[
                                          0:len(archive_byte_buffer) - 1]

                bit_buffer.frombytes(archive_byte_buffer)
                bit_buffer = bit_buffer[0:len(bit_buffer) - empty_bits]
                temp_bits = bitarray()

                for bit in bit_buffer:
                    temp_bits.append(bit)
                    temp_bits_tuple = tuple(temp_bits)
                    if temp_bits_tuple in decoding_dictionary.keys():
                        file.write(decoding_dictionary[temp_bits_tuple])
                        current_control_sum.update(
                            decoding_dictionary[temp_bits_tuple])
                        temp_bits.clear()
                bit_buffer = temp_bits

        return current_control_sum.digest() == control_sum

    @classmethod
    def _get_data(cls, archive_file: BufferedReader) -> bytes:
        data = bytearray()
        byte = archive_file.read(1)
        if not byte:
            return byte

        while byte[0] != 0:
            data.extend(archive_file.read(byte[0]))
            byte = archive_file.read(1)

        return bytes(data)

    @classmethod
    def get_file_path(cls, file_path_data: bytes):
        file_path: List[str] = []
        for i in file_path_data:
            file_path.append(chr(i))
        return ''.join(file_path)

    @classmethod
    def get_decoding_dictionary(cls, encoding_dictionary_data: bytes) -> \
            Dict[Tuple[bool], bytes]:
        encoding_dictionary_bits = bitarray()
        encoding_dictionary_bits.frombytes(encoding_dictionary_data)
        index = 0
        bit = 8
        decoding_dictionary: Dict[Tuple[bool], bytes] = {}

        while len(encoding_dictionary_bits) - index > bit:
            symbol: bitarray = encoding_dictionary_bits[index:index + bit:]
            code_len_bits: bitarray = \
                encoding_dictionary_bits[index + bit:index + 2 * bit:]
            code_len = int(code_len_bits.to01(), 2)
            code = encoding_dictionary_bits[
                   index + 2 * bit:index + 2 * bit + code_len:]

            decoding_dictionary[tuple(code)] = symbol.tobytes()
            index += 2 * bit + code_len

        return decoding_dictionary


class ShannonFanoEncoder(Encoder):

    @classmethod
    def encode(cls, file: BufferedReader, archive_file: BufferedWriter,
               file_path: str):
        encoding_dictionary = cls.get_encoding_dictionary(file)
        cls._encode(file, archive_file, file_path,
                    encoding_dictionary)

    @classmethod
    def _encode(cls,
                file: BufferedReader,
                archive_file: BufferedWriter,
                file_path: str,
                encoding_dictionary):

        archive_file.write(cls._get_file_path_data(file_path))
        archive_file.write(cls._get_dictionary_data(encoding_dictionary))
        archive_file.write(cls._compose_data(cls._get_control_sum(file)))

        cls._write_encoded_file_data(file, archive_file, encoding_dictionary)

    @classmethod
    def _get_control_sum(cls, file: BufferedReader) -> bytes:
        sum = md5()
        while True:
            byte = file.read(1)
            if not byte:
                break
            sum.update(byte)
        file.seek(0, 0)
        return sum.digest()

    @classmethod
    def _write_encoded_file_data(cls, file: BufferedReader,
                                 archive_file: BufferedWriter,
                                 encoding_dictionary):
        temp_archive_file_path = Path('temp_archive_file')
        bit_buffer: bitarray = bitarray()
        with temp_archive_file_path.open('wb') as temp_archive_file:
            while True:
                byte = file.read(1)
                if not byte:
                    break
                bit_buffer.extend(encoding_dictionary[byte[0]])
                while len(bit_buffer) >= 8:
                    if len(bit_buffer) > 8:
                        temp_archive_file.write(bit_buffer[:8:].tobytes())
                        bit_buffer = bit_buffer[8::]
                    else:
                        temp_archive_file.write(bit_buffer.tobytes())
                        bit_buffer.clear()

            empty_bits_count = 8 - len(bit_buffer)
            if empty_bits_count == 8:
                empty_bits_count = 0

            if len(bit_buffer) != 0:
                temp_archive_file.write(bit_buffer.tobytes())

            temp_archive_file.write(bytes([empty_bits_count]))

        with temp_archive_file_path.open('rb') as temp_archive_file:
            while True:
                archive_bytes = temp_archive_file.read(255)
                if not archive_bytes:
                    archive_file.write(bytes([0]))
                    break
                archive_file.write(bytes([len(archive_bytes)]))
                archive_file.write(archive_bytes)

        temp_archive_file_path.unlink()
        file.seek(0, 0)

    @classmethod
    def _get_file_path_data(cls, file_path) -> bytes:
        return cls._compose_data(bytes(file_path, 'utf-8'))

    @classmethod
    def _compose_data(cls, data: bytes):
        composed_data = bytearray()
        data_unit = bytearray()
        for byte in data:
            data_unit.append(byte)
            if len(data_unit) == 255:
                composed_data.append(255)
                composed_data.extend(data_unit)
                data_unit.clear()

        if len(data_unit) != 0:
            composed_data.append(len(data_unit))
            composed_data.extend(data_unit)
        composed_data.append(0)
        return composed_data

    @classmethod
    def _get_dictionary_data(cls, encoding_dictionary: [int, bitarray]):
        encoding_dictionary_data: bitarray = bitarray()

        for key in encoding_dictionary.keys():
            code = encoding_dictionary[key]
            encoding_dictionary_data.frombytes(bytes([key, len(code)]))
            encoding_dictionary_data.extend(code)

        return cls._compose_data(encoding_dictionary_data.tobytes())

    @classmethod
    def get_encoding_dictionary(cls, file: BufferedReader) -> \
            Dict[int, bitarray]:
        symbols = set()
        frequency: Dict[int, int] = collections.defaultdict(int)
        file_len = 0
        while True:
            byte = file.read(1)
            if not byte:
                break
            frequency[byte[0]] += 1
            symbols.add(byte[0])
            file_len += 1
        file.seek(0, 0)

        symbols_list = list(symbols)

        symbols_list.sort(key=lambda s: frequency[s])
        symbols_list.reverse()
        encoding_dictionary: Dict[int, bitarray] = {}

        cls.fill_encoding_dictionary(frequency,
                                     symbols_list,
                                     0,
                                     len(symbols) - 1,
                                     '',
                                     encoding_dictionary,
                                     file_len)
        return encoding_dictionary

    @classmethod
    def fill_encoding_dictionary(cls,
                                 frequency,
                                 symbols,
                                 start: int,
                                 end: int,
                                 code: str,
                                 encoding_dictionary: Dict[int, bitarray],
                                 length):

        if start >= len(symbols):
            return

        if start == end + 1:
            encoding_dictionary[symbols[start]] = bitarray(code + '1')
            encoding_dictionary[symbols[start + 1]] = bitarray(code + '0')
            return

        if start == end:
            encoding_dictionary[symbols[start]] = bitarray(code)
            return

        current_frequency = 0
        for i in range(start, end):
            current_frequency += frequency[symbols[i]]
            if current_frequency < int(length / 2 + 0.5):
                continue

            cls.fill_encoding_dictionary(frequency, symbols, start, i,
                                         code + '1', encoding_dictionary,
                                         current_frequency)
            cls.fill_encoding_dictionary(frequency, symbols, i + 1, end,
                                         code + '0', encoding_dictionary,
                                         length - current_frequency)
            break
