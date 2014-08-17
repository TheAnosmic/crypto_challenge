from itertools import cycle
from byte_array import ByteArray


class Key(ByteArray):

    def __iter__(self):
        """
        infinite iterate over the ord() of the key.
        @return: list of ints (ords of the key)
        """
        return cycle(self.source_int_list)