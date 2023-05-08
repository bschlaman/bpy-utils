import unittest

from bpyutils.formatting.std import compact_repr


class TestCompactRepr(unittest.TestCase):
    def test_compact_repr_set_empty(self):
        target = set()
        expected = "set()"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_list_empty(self):
        target = []
        expected = "[]"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_set_short(self):
        target = {1, 2, 3}
        expected = "{1, 2, 3}"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_list_short(self):
        target = [1, 2, 3]
        expected = "[1, 2, 3]"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_list_4(self):
        target = [1, 2, 3, 4]
        expected = "[1, 2, 3, 4]"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_set_5(self):
        target = {1, 2, 3, 4, 5}
        expected = "{1, 2, ... 4, 5}"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_set_long(self):
        target = {1, 2, 3, 4, 5, 6, 7}
        expected = "{1, 2, ... 6, 7}"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_list_long(self):
        target = [1, 2, 3, 4, 5, 6, 7, 8]
        expected = "[1, 2, ... 7, 8]"
        self.assertEqual(compact_repr(target), expected)

    def test_compact_repr_unsupported_type(self):
        target = {1: 2}
        with self.assertRaises(TypeError):
            compact_repr(target)
