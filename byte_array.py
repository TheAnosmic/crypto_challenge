from binascii import unhexlify
from collections import Iterable
from string import printable


class ByteArray(object):
    """
    Helper class to string manipulations.
    """

    def __init__(self, source):
        self._source = source
        self._source_int_list = None
        self._all_printable = None

    def get_source_string(self):
        """
        To indicate that there is no set at all.
        """
        return self._source

    @property
    def source_int_list(self):
        if not self._source_int_list:
            self._source_int_list = [ord(c) for c in self._source]
        return self._source_int_list

    @property
    def is_all_printable(self):
        if self._all_printable is None:
            self._all_printable = all(map(lambda c: c in printable, self._source))
        return self._all_printable

    @classmethod
    def from_hex(cls, source):
        return cls(unhexlify(source))

    @classmethod
    def from_int_list(cls, source):
        # Probably will be doing the calculate of int_list again,
        # but decided to leave it like that cuz not better solution found.
        return cls(''.join(chr(i) for i in source))


    def __str__(self):
        if self._all_printable:
            return self._source
        return '%r' % self._source

    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, str(self))

    def _iter_couple(self, other):
        if not isinstance(other, Iterable):
            return NotImplemented
        if isinstance(other, basestring):
            other = ByteArray(other)
        return zip(self.source_int_list, iter(other))

    def __xor__(self, other):
        """
        the xor stops when the shortest element exhausts.
        @param other: must be an iterable of ints.
        @type other: [int]
        @return: Text of the xored texts.
        """
        return ByteArray.from_int_list([i ^ j for i, j in self._iter_couple(other)])

    def __and__(self, other):
        return ByteArray.from_int_list([i & j for i, j in self._iter_couple(other)])

    def __or__(self, other):
        return ByteArray.from_int_list([i | j for i, j in self._iter_couple(other)])

    def __iter__(self):
        return iter(self.source_int_list)

    def __cmp__(self, other):
        if isinstance(other, basestring):
            return cmp(self._source, other)
        if isinstance(other, ByteArray):
            return cmp(other._source, self._source)
        return NotImplemented

    def hamming_distance(self, other):
        if isinstance(other, basestring):
            other = ByteArray(other)
        if not isinstance(other, ByteArray):
            raise NotImplementedError("Other must be a string or a ByteArray (Not %s)" % type(other))
        def comparator(x, y):
            return x + bin(y[0] ^ y[1]).count("1")
        return reduce(comparator, self._iter_couple(other), 0)

    # def hamming_distance(self, chunk_size, chunk_one_start):
    #     def f(x, y):
    #         return x + bin(y[0] ^ y[1]).count("1")
    #
    #     chunk_one_end = chunk_one_start + chunk_size
    #     c1 = self.source_int_list[chunk_one_start:chunk_one_end]
    #     c2 = self.source_int_list[chunk_one_end:chunk_one_end + chunk_size]
    #     return reduce(f, zip(c1, c2), 0)