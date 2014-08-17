"""
All things that starts with crypto_ch* are
    from the challenges from http://cryptopals.com/
"""

from unittest import TestCase
from binascii import hexlify

from byte_array import ByteArray
from key import Key
from text import Text


HELLO_WORLD = "Hello World"
HELLO_WORLD_NO_SPACE = "HelloWorld"


class ByteArrayTests(TestCase):
    def test_source_int_list(self):
        # Taking shorter length check, cuz unittest did not print
        #   the whole list when i used a long one (and failed).
        checked = HELLO_WORLD[:4]
        self.assertEqual(ByteArray(checked).source_int_list, [ord(i) for i in checked])

    def test_eq(self):
        self.assertEqual(ByteArray(HELLO_WORLD), HELLO_WORLD)
        self.assertEqual(ByteArray(HELLO_WORLD), ByteArray(HELLO_WORLD))
        self.assertNotEqual(ByteArray(HELLO_WORLD), "Not Hello World")
        self.assertNotEqual(ByteArray(HELLO_WORLD), ByteArray("Hello World Not"))

    def test_from_hex(self):
        hexed = hexlify(HELLO_WORLD)
        s = ByteArray.from_hex(hexed)
        self.assertEqual(s, HELLO_WORLD, "From hex not matching: %r (should be %r)" % (s, HELLO_WORLD))
        crypto_ch_1_feed = "49276d206b696c6c696e6720796f757220627261696e206c696b65" \
                           "206120706f69736f6e6f7573206d757368726f6f6d"
        crypto_ch_1_exp = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG1" \
                          "1c2hyb29t".decode("base64")
        ba = ByteArray.from_hex(crypto_ch_1_feed)
        self.assertEqual(ba, crypto_ch_1_exp)

    def test_xor(self):
        s = ByteArray(HELLO_WORLD_NO_SPACE)
        case_swapped = s ^ [0b100000] * len(HELLO_WORLD_NO_SPACE)
        self.assertEqual(case_swapped, HELLO_WORLD_NO_SPACE.swapcase())
        crypto_ch_2_feed = ByteArray.from_hex("1c0111001f010100061a024b53535009181c")
        crypto_ch_2_xor = ByteArray.from_hex("686974207468652062756c6c277320657965")
        crypto_ch_2_exp = ByteArray.from_hex("746865206b696420646f6e277420706c6179")
        self.assertEqual(crypto_ch_2_feed ^ crypto_ch_2_xor, crypto_ch_2_exp)

    def test_hamming_distance(self):
        crypto_ch6_candidate1 = ByteArray("this is a test")
        crypto_ch6_candidate2 = ByteArray("wokka wokka!!!")
        crypto_ch6_hamming_dist = 42 - 5
        self.assertEqual(crypto_ch6_candidate1.hamming_distance(crypto_ch6_candidate2),
                         crypto_ch6_hamming_dist)


class KeyTests(TestCase):
    def test_one_char_key(self):
        key = Key("a")
        self.assertEqual(ByteArray("\x00\x00\x00") ^ key, "aaa")

    def test_repeating_xor_key(self):
        crypto_ch_5_feed = ByteArray("Burning 'em, if you ain't quick and nimble\nI go crazy"
                                     " when I hear a cymbal")
        crypto_ch_5_key = Key("ICE")
        crypto_ch_5_exp = ByteArray.from_hex("0b3637272a2b2e63622c2e69692a23693a2a"
                                             "3c6324202d623d63343c2a26226324272765"
                                             "272a282b2f20430a652e2c652a3124333a65"
                                             "3e2b2027630c692b20283165286326302e27"
                                             "282f")
        self.assertEqual(crypto_ch_5_feed ^ crypto_ch_5_key, crypto_ch_5_exp)


class TextTests(TestCase):
    def test_byte_array_to_lower(self):
        self.assertEqual(Text.byte_array_to_lower(ByteArray(HELLO_WORLD)), HELLO_WORLD.lower())

    def test_find_one_char_key(self):
        crypto_ch3_feed = ByteArray.from_hex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
        crypto_ch3_solution = "Pbbxvat ZP'f yvxr n cbhaq bs onpba".decode("rot13") # no plain-text for u
        found = crypto_ch3_feed ^ Text.find_one_char_key(crypto_ch3_feed)
        self.assertEqual(found, crypto_ch3_solution)