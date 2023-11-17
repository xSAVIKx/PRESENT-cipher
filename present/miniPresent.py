# coding=utf-8

__author__ = 'Iurii Sergiichuk'


class MiniPresent:
    # import string
    def __init__(self, key, rounds=4):
        self.rounds = rounds
        self.roundkeys = generateRoundkeys16(string2number(key), self.rounds)


    def encrypt(self, block):
        string_input = False
        state = block
        state = string2number(block)
        string_input = True            
        for i in range(self.rounds - 1):
            state = addRoundKey(state, self.roundkeys[i])
            state = sBoxLayer(state)
            state = pLayer(state)
        cipher = addRoundKey(state, self.roundkeys[-1])
        if string_input:
            return number2string_N(cipher, self.get_block_size())
        return cipher

    def decrypt(self, block):
        string_input = False
        state = block
        state = string2number(block)
        string_input = True
        for i in range(self.rounds - 1):
            state = addRoundKey(state, self.roundkeys[-i - 1])
            state = pLayer_dec(state)
            state = sBoxLayer_dec(state)
        decipher = addRoundKey(state, self.roundkeys[0])
        if string_input:
            return number2string_N(decipher, self.get_block_size())
        return decipher

    def get_block_size(self):
        return 2

# 0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
Sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
Sbox_inv = [Sbox.index(x) for x in range(16)]
PBox = [0, 5, 2, 3, 7, 6, 1, 4]
PBox_inv = [PBox.index(x) for x in range(8)]


def generateRoundkeys16(key, rounds):
    roundkeys = []
    
    for i in range(1, rounds + 1):  # (K1 ... K32)
        # rawkey: used in comments to show what happens at bitlevel
        roundkeys.append((key >> 8)&0xFF)
        # 1. Shift
        key = ((key & (2 ** 9 - 1)) << 7) + (key >> 9)
        # 2. SBox
        # key = (Sbox[key >> 15] << 15) + (Sbox[(key >> 12) & 0xF] << 12) + (key & (2 ** 12 - 1))
        key =Sbox[key >> 15]
        # 3. Salt
        # rawKey[62:67] ^ i
        key ^= i << 8
    return roundkeys


def addRoundKey(state, roundkey):
    return state ^ roundkey


def sBoxLayer(state):
    output = 0
    for i in range(2):
        output += Sbox[( state >> (i * 4)) & 0xF] << (i * 4)
    return output


def sBoxLayer_dec(state):
    output = 0
    for i in range(2):
        output += Sbox_inv[( state >> (i * 4)) & 0xF] << (i * 4)
    return output


def pLayer(state):
    output = 0
    for i in range(8):
        output += ((state >> i) & 0x01) << PBox[i]
    return output


def pLayer_dec(state):
    output = 0
    for i in range(8):
        output += ((state >> i) & 0x01) << PBox_inv[i]
    return output


def string2number(i):
    """ Convert a string to a number

    Input: string (big-endian)
    Output: long or integer
    """
    from codecs import getencoder
    encoder_hex = getencoder('hex')
    if type(i) == bytes:
        return int(encoder_hex(i)[0], 16)
    elif type(i) == int:
        return i
    return int(encoder_hex(bytes(i.encode("UTF-8")))[0], 16)


def number2string_N(i, N):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of string
    Output: string (big-endian)
    """
    from codecs import getdecoder
    decoder_hex = getdecoder('hex')
    s = '%0*x' % (N * 2, i)
    return decoder_hex(s)[0]


if __name__ == "__main__":
    key = 0x0
    plain_1 = 0
    plain_2 = 255
    plain_3 = 1025
    print(plain_1)
    print(plain_2)
    print(plain_3)
    cipher = MiniPresent(key)
    encrypted_1 = cipher.encrypt(plain_1)
    encrypted_2 = cipher.encrypt(plain_2)
    encrypted_3 = cipher.encrypt(plain_3)
    print(encrypted_1)
    print(encrypted_2)
    print(encrypted_3)

    decrypted_1 = cipher.decrypt(encrypted_1)
    decrypted_2 = cipher.decrypt(encrypted_2)
    decrypted_3 = cipher.decrypt(encrypted_3)
            
    print(int.from_bytes(decrypted_1, byteorder='big'))
    print(int.from_bytes(decrypted_2, byteorder='big'))
    print(int.from_bytes(decrypted_3, byteorder='big'))