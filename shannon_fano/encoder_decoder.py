import collections
import os
from hashlib import md5
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import List, Tuple, Dict, Set
from bitarray import bitarray
from abc import ABC, abstractmethod


class Decoder(ABC):

    @classmethod
    @abstractmethod
    def decode(cls, archive_file_size: int,
               archive_file,
               target_foldr: Path,
               files: Set[str],
               ignore_broken_files: bool):
        pass

    @classmethod
    @abstractmethod
    def get_file_names(cls, archive_file):
        pass


class Encoder(ABC):

    @classmethod
    @abstractmethod
    def encode(cls, file, archive_file, file_path: str):
        pass


class ShannonFanoDecoder(Decoder):
    @classmethod
    def decode(cls, archive_file_size: int,
               archive_file: BufferedReader,
               target_foldr: Path,
               files_for_decompress: Set[str],
               not_ignore_broken_files: bool) \
            -> List[Path]:
        broken_files: List[Path] = []
        while True:
            if archive_file.tell() + 16 == archive_file:
                break
            file_path_data = cls._get_data(archive_file)
            if not file_path_data:
                break
            local_file_path = cls.get_file_path(file_path_data)
            if len(files_for_decompress) != 0 \
                    and local_file_path not in files_for_decompress:
                cls._move_to_next_file(archive_file)
                continue

            current_file_path = target_foldr / local_file_path

            if not current_file_path.parent.exists():
                current_file_path.parent.mkdir(parents=True)

            dictionary_data = cls._get_data(archive_file)
            if len(dictionary_data) == 0:
                current_file_path.write_bytes(bytes([]))
                continue
            decoding_dictionary = cls.get_decoding_dictionary(dictionary_data)

            control_sum = cls._get_data(archive_file)

            if control_sum \
                    != cls.decode_and_write_file(archive_file,
                                                 Path(current_file_path),
                                                 decoding_dictionary) \
                    and not_ignore_broken_files:
                current_file_path.unlink()
                broken_files.append(current_file_path)
        return broken_files

    @classmethod
    def get_file_names(cls, archive_file: BufferedReader):
        while True:
            file_path_data = cls._get_data(archive_file)
            if not file_path_data:
                break
            yield cls.get_file_path(file_path_data)
            cls._move_to_next_file(archive_file)

    @classmethod
    def _move_to_next_file(cls, archive_file: BufferedReader):
        for i in range(3):
            byte = archive_file.read(1)
            if not byte:
                break
            if byte[0] == 0:
                break
            while byte[0] != 0:
                archive_file.seek(byte[0], 1)
                byte = archive_file.read(1)

    @classmethod
    def decode_and_write_file(cls,
                              archive_file: BufferedReader,
                              file_path: Path,
                              decoding_dictionary: Dict[Tuple[bool], bytes]) \
            -> bytes:
        decoded_control_sum = md5()

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
                        decoded_control_sum.update(
                            decoding_dictionary[temp_bits_tuple])
                        temp_bits.clear()
                bit_buffer = temp_bits

        return decoded_control_sum.digest()

    @classmethod
    def _get_data(cls, archive_file: BufferedReader) -> bytes:
        data = bytearray()
        byte = archive_file.read(1)
        if not byte:
            return byte

        if byte[0] == 0:
            return bytes()

        while byte[0] != 0:
            data.extend(archive_file.read(byte[0]))
            byte = archive_file.read(1)

        return bytes(data)

    @classmethod
    def get_file_path(cls, file_path_data: bytes) -> str:
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
    data_unit_size = 255
    byte = 8

    @classmethod
    def encode(cls, file: BufferedReader,
               archive_file: BufferedWriter,
               file_path: str):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        if size == 0:
            cls._encode_empty_file(archive_file, file_path)
        else:
            file.seek(0)
            cls._encode(file, archive_file, file_path)

    @classmethod
    def _encode(cls,
                file: BufferedReader,
                archive_file: BufferedWriter,
                file_path: str):

        encoding_dictionary = cls.get_encoding_dictionary(file)
        archive_file.write(cls._get_file_path_data(file_path))
        archive_file.write(cls._get_dictionary_data(encoding_dictionary))
        archive_file.write(cls._compose_data(cls._get_control_sum(file)))

        cls._write_encoded_file_data(file, archive_file, encoding_dictionary)

    @classmethod
    def _encode_empty_file(cls, archive_file: BufferedWriter,
                           file_path: str):
        archive_file.write(cls._get_file_path_data(file_path))
        archive_file.write(bytes([0]))

    @classmethod
    def _get_control_sum(cls, file: BufferedReader) -> bytes:
        sum = md5()
        while True:
            byte = file.read(1)
            if not byte:
                break
            sum.update(byte)
        file.seek(0)
        return sum.digest()

    @classmethod
    def _write_encoded_file_data(cls, file: BufferedReader,
                                 archive_file: BufferedWriter,
                                 encoding_dictionary):
        bit_buffer = bitarray()
        while True:
            byte = file.read(1)
            if not byte:
                break
            bit_buffer.extend(encoding_dictionary[byte[0]])
            while len(bit_buffer) >= cls.data_unit_size * cls.byte:
                archive_file.write(bytes([cls.data_unit_size]))
                archive_file.write(
                    bit_buffer[: cls.data_unit_size * cls.byte:].tobytes())
                bit_buffer = bit_buffer[cls.data_unit_size * cls.byte::]

        if len(bit_buffer) != 0:
            empty_bits_count = cls.byte - len(bit_buffer) % cls.byte
            if empty_bits_count == cls.byte:
                empty_bits_count = 0
            byte_buffer = bytearray(bit_buffer.tobytes())
            byte_buffer.append(empty_bits_count)

            archive_file.write(cls._compose_data(bytes(byte_buffer)))

    @classmethod
    def _get_file_path_data(cls, file_path) -> bytes:
        return cls._compose_data(bytes(file_path, 'utf-8'))

    @classmethod
    def _compose_data(cls, data: bytes) -> bytes:
        composed_data = bytearray()
        data_unit = bytearray()
        for byte in data:
            data_unit.append(byte)
            if len(data_unit) == cls.data_unit_size:
                composed_data.append(cls.data_unit_size)
                composed_data.extend(data_unit)
                data_unit.clear()

        if len(data_unit) != 0:
            composed_data.append(len(data_unit))
            composed_data.extend(data_unit)
        composed_data.append(0)
        return composed_data

    @classmethod
    def _get_dictionary_data(cls,
                             encoding_dictionary: [int, bitarray]) -> bytes:
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
        file.seek(0)

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
