from __future__ import annotations

from typing import Final
from mypy_extensions import u8

from librt.internal import (
    ReadBuffer,
    WriteBuffer,
    write_bool, read_bool,
    write_str, read_str,
    write_float, read_float,
    write_int, read_int,
    write_tag, read_tag,
    write_bytes, read_bytes,
    cache_version,
)

Tag = u8
TAG_A: Final[Tag] = 33
TAG_B: Final[Tag] = 255
TAG_SPECIAL: Final[Tag] = 239


def test_cache_version() -> None:
    assert cache_version() == 0


def test_buffer_write_and_read_int() -> None:
    b = WriteBuffer()
    write_int(b, 42)
    rb = ReadBuffer(b.getvalue())
    assert read_int(rb) == 42


def test_buffer_roundtrip() -> None:
    b: WriteBuffer | ReadBuffer
    b = WriteBuffer()
    write_str(b, "foo")
    write_bool(b, True)
    write_str(b, "bar" * 1000)
    write_bool(b, False)
    write_bytes(b, b"bar")
    write_bytes(b, b"bar" * 100)
    write_bytes(b, b"")
    write_bytes(b, b"a" * 117)
    write_bytes(b, b"a" * 118)
    write_float(b, 0.1)
    write_float(b, -1.0)
    write_float(b, -113.0)
    write_int(b, 0)
    write_int(b, 1)
    write_tag(b, TAG_A)
    write_tag(b, TAG_SPECIAL)
    write_tag(b, TAG_B)
    write_int(b, 2)
    write_int(b, 2 ** 85)
    write_int(b, 255)
    write_int(b, -1)
    write_int(b, -255)
    write_int(b, 536860911)
    write_int(b, 536860912)
    write_int(b, 1234567891)

    b = ReadBuffer(b.getvalue())
    assert read_str(b) == "foo"
    assert read_bool(b) is True
    assert read_str(b) == "bar" * 1000
    assert read_bool(b) is False
    assert read_bytes(b) == b"bar"
    assert read_bytes(b) == b"bar" * 100
    assert read_bytes(b) == b""
    assert read_bytes(b) == b"a" * 117
    assert read_bytes(b) == b"a" * 118
    assert read_float(b) == 0.1
    assert read_float(b) == -1.0
    assert read_float(b) == -113.0
    assert read_int(b) == 0
    assert read_int(b) == 1
    assert read_tag(b) == TAG_A
    assert read_tag(b) == TAG_SPECIAL
    assert read_tag(b) == TAG_B
    assert read_int(b) == 2
    assert read_int(b) == 2 ** 85
    assert read_int(b) == 255
    assert read_int(b) == -1
    assert read_int(b) == -255
    assert read_int(b) == 536860911
    assert read_int(b) == 536860912
    assert read_int(b) == 1234567891


def test_buffer_int_size() -> None:
    b: WriteBuffer | ReadBuffer
    for i in (-10, -9, 0, 116, 117):
        b = WriteBuffer()
        write_int(b, i)
        assert len(b.getvalue()) == 1
        b = ReadBuffer(b.getvalue())
        assert read_int(b) == i
    for i in (-100, -11, 118, 12344, 16283):
        b = WriteBuffer()
        write_int(b, i)
        assert len(b.getvalue()) == 2
        b = ReadBuffer(b.getvalue())
        assert read_int(b) == i
    for i in (-10000, 16284, 123456789):
        b = WriteBuffer()
        write_int(b, i)
        assert len(b.getvalue()) == 4
        b = ReadBuffer(b.getvalue())
        assert read_int(b) == i


def test_buffer_int_powers() -> None:
    # 0, 1, 2 are tested above
    b: WriteBuffer | ReadBuffer
    for p in range(2, 100):
        b = WriteBuffer()
        write_int(b, 1 << p)
        write_int(b, -1 << p)
        b = ReadBuffer(b.getvalue())
        assert read_int(b) == 1 << p
        assert read_int(b) == -1 << p


def test_buffer_str_size() -> None:
    b: WriteBuffer | ReadBuffer
    for s in ("", "a", "a" * 117):
        b = WriteBuffer()
        write_str(b, s)
        assert len(b.getvalue()) == len(s) + 1
        b = ReadBuffer(b.getvalue())
        assert read_str(b) == s

    for s in ("a" * 118, "a" * 16283):
        b = WriteBuffer()
        write_str(b, s)
        assert len(b.getvalue()) == len(s) + 2
        b = ReadBuffer(b.getvalue())
        assert read_str(b) == s
