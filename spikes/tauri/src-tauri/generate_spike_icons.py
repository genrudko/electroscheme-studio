#!/usr/bin/env python3
"""Generate neutral deterministic spike-only Tauri icons using Python stdlib."""
from __future__ import annotations
import argparse, binascii, hashlib, struct, zlib
from pathlib import Path

SIZE = 64
BG = (72, 78, 86, 255)
GRID = (101, 109, 119, 255)
MARK = (224, 228, 233, 255)

def pixels() -> bytes:
    output = bytearray()
    for y in range(SIZE):
        for x in range(SIZE):
            color = BG
            if x % 16 == 0 or y % 16 == 0:
                color = GRID
            if (29 <= x <= 34 and 14 <= y <= 49) or (14 <= x <= 49 and 29 <= y <= 34):
                color = MARK
            output.extend(color)
    return bytes(output)

def chunk(kind: bytes, data: bytes) -> bytes:
    checksum = binascii.crc32(kind + data) & 0xffffffff
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', checksum)

def png_bytes() -> bytes:
    raw = pixels()
    rows = b''.join(b'\x00' + raw[y * SIZE * 4:(y + 1) * SIZE * 4] for y in range(SIZE))
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', SIZE, SIZE, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows, level=9))
            + chunk(b'IEND', b''))

def ico_bytes(png: bytes) -> bytes:
    header = struct.pack('<HHH', 0, 1, 1)
    entry = struct.pack('<BBBBHHII', SIZE, SIZE, 0, 0, 1, 32, len(png), 22)
    return header + entry + png

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    png = png_bytes()
    outputs = {'icon.png': png, 'icon.ico': ico_bytes(png)}
    for name, data in outputs.items():
        (args.output_dir / name).write_bytes(data)
        print(f'{name} {hashlib.sha256(data).hexdigest()} {len(data)}')

if __name__ == '__main__':
    main()
