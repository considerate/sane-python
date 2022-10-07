import numpy
from pathlib import Path
import io
import typing


def read_uint32(f: io.BufferedReader) -> int:
    return int.from_bytes(f.read(4), byteorder="little", signed=False)


def write_uint32(f: io.BufferedWriter, n: int) -> int:
    return f.write(int.to_bytes(n, length=4, byteorder="little", signed=False))


def read_uint64(f: io.BufferedReader) -> int:
    return int.from_bytes(f.read(8), byteorder="little", signed=False)


def write_uint64(f: io.BufferedWriter, n: int) -> int:
    return f.write(int.to_bytes(n, length=8, byteorder="little", signed=False))


dtypes = {
    0: numpy.dtype("float32"),
    1: numpy.dtype("int32"),
    2: numpy.dtype("uint32"),
    3: numpy.dtype("float64"),
    4: numpy.dtype("int64"),
    5: numpy.dtype("uint64"),
    6: numpy.dtype("int8"),
    7: numpy.dtype("uint8"),
}

dtype_bytes = {(v.kind, v.itemsize): k for k, v in dtypes.items()}


def load_reader(f: io.BufferedReader) -> typing.Optional[numpy.ndarray]:
    magic = f.read(4)
    if magic != b"SANE":
        return None
    shapelen = read_uint32(f)
    shape = list(reversed([read_uint64(f) for _ in range(shapelen)]))
    dtype_byte = int.from_bytes(f.read(1), byteorder="little", signed=False)
    dtype = dtypes.get(dtype_byte)
    if dtype is None:
        raise ValueError(f"Got unsupported SANE data type {dtype_byte}.")
    dtype.newbyteorder("<")
    payloadlen = read_uint64(f)
    # allocate memory for the array
    array = numpy.empty(shape=shape, dtype=dtype)
    bytesread = f.readinto(array.data)
    if bytesread != payloadlen:
        raise OSError(f"Expected {payloadlen} bytes, but only got {bytesread}.")
    return array


def load_arrays(f: io.BufferedReader) -> typing.Generator[numpy.ndarray, None, None]:
    while True:
        arr = load_reader(f)
        if arr is None:
            return
        else:
            yield arr


def load(path: Path) -> numpy.ndarray:
    with open(path, "rb") as f:
        array = load_reader(f)
        assert array is not None
        return array


def save_writer(f: io.BufferedWriter, array: numpy.ndarray) -> None:
    f.write(b"SANE")
    write_uint32(f, len(array.shape))
    for dim in reversed(array.shape):
        write_uint64(f, dim)
    dtype_byte = dtype_bytes.get((array.dtype.kind, array.dtype.itemsize))
    if dtype_byte is None:
        raise ValueError(f"Cannot save {array.dtype.type} data as a SANE array.")
    f.write(int.to_bytes(dtype_byte, length=1, byteorder="little", signed=False))
    little = array.newbyteorder("<")
    write_uint64(f, little.data.nbytes)
    f.write(little.data)


def save_arrays(f: io.BufferedWriter, arrays: typing.Iterable[numpy.ndarray]) -> None:
    for arr in arrays:
        save_writer(f, arr)


def save(path: Path, array: numpy.ndarray) -> None:
    with open(path, "wb") as f:
        save_writer(f, array)
