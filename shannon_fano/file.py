from dataclasses import dataclass


@dataclass
class File:
    path: str
    data: bytes
    hash_code: bytes
