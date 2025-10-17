from typing import Final
from mypy_extensions import u8

from librt.internal import (
    Buffer,
    write_bool, read_bool,
    write_str, read_str,
    write_float, read_float,
    write_int, read_int,
    write_tag, read_tag,
    write_bytes, read_bytes,
)

Tag = u8
TAG_A: Final[Tag] = 33
TAG_B: Final[Tag] = 255
TAG_SPECIAL: Final[Tag] = 239


def test_buffer_basic() -> None:
    b = Buffer(b"foo")
    assert b.getvalue() == b"foo"


def test_buffer_empty() -> None:
    b = Buffer(b"")
    write_int(b, 42)
    b = Buffer(b.getvalue())
    assert read_int(b) == 42


def test_buffer_roundtrip() -> None:
    b = Buffer()
    write_str(b, "foo")
    write_bool(b, True)
    write_str(b, "bar" * 1000)
    write_bool(b, False)
    write_float(b, 0.1)
    write_tag(b, TAG_A)
    write_tag(b, TAG_SPECIAL)
    write_tag(b, TAG_B)
    write_int(b, 1)
    write_int(b, 2)
    write_int(b, 2 ** 85)
    write_int(b, 1234512344)
    write_int(b, 1234512345)
    write_bytes(b, b"foobar")
    write_bytes(b, b"abc" * 1000)

    b = Buffer(b.getvalue())
    assert read_str(b) == "foo"
    assert read_bool(b) is True
    assert read_str(b) == "bar" * 1000
    assert read_bool(b) is False
    assert read_float(b) == 0.1
    assert read_tag(b) == TAG_A
    assert read_tag(b) == TAG_SPECIAL
    assert read_tag(b) == TAG_B
    assert read_int(b) == 1
    assert read_int(b) == 2
    assert read_int(b) == 2 ** 85
    assert read_int(b) == 1234512344
    assert read_int(b) == 1234512345
    assert read_bytes(b) == b"foobar"
    assert read_bytes(b) == b"abc" * 1000


def test_buffer_int_size() -> None:
    for i in (-10, -9, 0, 116, 117):
        b = Buffer()
        write_int(b, i)
        assert len(b.getvalue()) == 1
        b = Buffer(b.getvalue())
        assert read_int(b) == i
    for i in (-12345, -12344, -11, 118, 12344, 12345):
        b = Buffer()
        write_int(b, i)
        assert len(b.getvalue()) <= 9  # sizeof(size_t) + 1
        b = Buffer(b.getvalue())
        assert read_int(b) == i


def test_buffer_str_size() -> None:
    for s in ("", "a", "a" * 127):
        b = Buffer()
        write_str(b, s)
        assert len(b.getvalue()) == len(s) + 1
        b = Buffer(b.getvalue())
        assert read_str(b) == s
