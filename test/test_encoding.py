import numpy
import hypothesis
import io
import sane_python.io as sane
import sane_python
from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays

dim = st.integers(1, 64)

t = st.sampled_from(["float32", "int8", "int32", "uint32"])


@given(arrays(shape=st.lists(dim, max_size=3), dtype=t))
def test_encode(arr):
    f = io.BytesIO()
    reader = io.BufferedReader(f)
    writer = io.BufferedWriter(f)
    sane.save_writer(writer, arr)
    writer.flush()
    f.seek(0)
    arr2 = sane.load_reader(reader)
    numpy.testing.assert_array_equal(arr, arr2)


@given(st.lists(arrays(shape=st.lists(dim, max_size=3), dtype=t), max_size=10))
def test_encode_many(arrs):
    f = io.BytesIO()
    reader = io.BufferedReader(f)
    writer = io.BufferedWriter(f)
    sane_python.save_arrays(writer, arrs)
    writer.flush()
    f.seek(0)
    arrs2 = list(sane_python.load_arrays(reader))
    assert len(arrs) == len(arrs2)
    for arr, arr2 in zip(arrs, arrs):
        numpy.testing.assert_array_equal(arr, arr2)
