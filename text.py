from key import Key


class Text(object):
    """
    Contains functions to break text xored ciphers.
    all functions are static.
    """
    MOST_FREQUENT_CHARS = [ord(i) for i in "etaoi"]  # credits to wikipedia
    _LOWER_AND_KEY = Key(chr(0b100000))

    @staticmethod
    def byte_array_to_lower(byte_array):
        return byte_array | Text._LOWER_AND_KEY

    @staticmethod
    def get_key_score(byte_array, key):
        """
        Only applied to printable checks.
        non-printable return always 0.
        @type byte_array: ByteArray
        @return: integer indicating the chance of the key to be correct.
        """
        keyed_byte_array = byte_array ^ key
        if not keyed_byte_array.is_all_printable:
            return 0
        lowered_keyed_byte_array = Text.byte_array_to_lower(keyed_byte_array)
        number_of_frequent_chars = reduce(
            lambda count, char: count + lowered_keyed_byte_array.source_int_list.count(char),
            Text.MOST_FREQUENT_CHARS)
        return number_of_frequent_chars

    @staticmethod
    def find_one_char_key(byte_array):
        """
        Tries to find the right one byte key for the encrypted byte_array.
        Only applied to printable texts encryption.
        :return: found key (as Key object)
        """
        max_score = 0
        found_key = None
        for i in range(255):
            key = Key(chr(i))
            score = Text.get_key_score(byte_array, key)
            if score > max_score:
                max_score = score
                found_key = key
        return found_key



