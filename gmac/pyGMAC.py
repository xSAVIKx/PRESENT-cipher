import random

from gmac.util.galue_fields import setGF2, i2P, ldMultGF2
from present.miniPresent import MiniPresent

__author__ = 'Iurii Sergiichuk'


def generate_IV():
    IV = random.getrandbits(16)
    IV = IV & 0xFFF0 | 1
    return IV


class GMAC(object):
    _state_after_gHash = 0

    def __init__(self, key, field_degree=16, field_polynom=0b10001000000001011):
        self._initial_field_polynom = field_polynom
        self._field_degree = field_degree
        self._key = key
        setGF2(self._field_degree, i2P(self._initial_field_polynom))

    def generate(self, open_text, IV):
        open_text_copy = open_text
        result = 0
        sub_key = self._get_subkey(self._key)
        # print "key=" + str(self._key),
        # print "\tIV=" + str(IV),
        # print "\tsub_key=" + str(sub_key),
        while (open_text_copy > 0):
            open_text_block = open_text_copy & 0xFFFF
            # print "\topenTextBlock=" + str(open_text_block),
            gctr = self._GCTR(IV, self._key)
            # print "\tgctr=" + str(gctr),
            gHash = self._gHash(open_text_block, sub_key)
            # print "\tgHash=" + str(gHash),
            self._state_after_gHash = gHash
            result = gHash ^ gctr
            # print "\tresult=" + str(result)
            open_text_copy >>= 16
        return result

    def _gHash(self, open_text_block, sub_key):
        text_block = i2P(open_text_block)
        s_key = i2P(sub_key)
        F = 0
        for i in xrange(len(text_block)):
            F = ldMultGF2(i2P(F ^ text_block[i]), s_key)
        return F

    def _GCTR(self, IV, key):
        cipher = MiniPresent(key)
        IV_copy = IV
        encrypted_IV = 0
        shift_amount = 0
        while (IV_copy):
            IV_eight_bit_block = IV_copy & 0xFF
            encrypted_IV_eight_bit_block = cipher.encrypt(IV_eight_bit_block)
            encrypted_IV += encrypted_IV_eight_bit_block << shift_amount
            shift_amount += 8
            IV_copy >>= 8
        return encrypted_IV

    def _get_subkey(self, key, init=0x0):
        cipher = MiniPresent(key)
        return cipher.encrypt(init)

    def get_state(self):
        return self._state_after_gHash


if __name__ == "__main__":
    subkey = long('235', base=10)
    g = GMAC(subkey)
    # IV = generate_IV()
    IV = 21313
    open_text_block = long('17927', base=10)
    result = g.generate(open_text_block, IV)
    print result
