# coding=utf-8
import pygal

__author__ = 'Iurii Sergiichuk'


class MiniPresent:
    def __init__(self, key, rounds=4):
        self.rounds = rounds
        if isinstance(key, basestring):
            self.roundkeys = generateRoundkeys16(string2number(key), self.rounds)
        else:
            self.roundkeys = generateRoundkeys16(key, self.rounds)

    def encrypt(self, block):
        string_input = False
        state = block
        if isinstance(block, basestring):
            state = string2number(block)
            string_input = True
        for i in xrange(self.rounds - 1):
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
        if isinstance(block, basestring):
            state = string2number(block)
            string_input = True
        for i in xrange(self.rounds - 1):
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
Sbox_inv = [Sbox.index(x) for x in xrange(16)]
PBox = [0, 5, 2, 3, 7, 6, 1, 4]
PBox_inv = [PBox.index(x) for x in xrange(8)]


def generateRoundkeys16(key, rounds):
    roundkeys = []
    for i in xrange(1, rounds + 1):  # (K1 ... K32)
        # rawkey: used in comments to show what happens at bitlevel
        roundkeys.append((key >> 8))
        # 1. Shift
        key = ((key & (2 ** 9 - 1)) << 7) + (key >> 9)
        # 2. SBox
        key = (Sbox[key >> 15] << 15) + (Sbox[(key >> 12) & 0xF] << 12) + (key & (2 ** 12 - 1))
        # 3. Salt
        # rawKey[62:67] ^ i
        key ^= i << 8
    return roundkeys


def addRoundKey(state, roundkey):
    return state ^ roundkey


def sBoxLayer(state):
    output = 0
    for i in xrange(2):
        output += Sbox[( state >> (i * 4)) & 0xF] << (i * 4)
    return output


def sBoxLayer_dec(state):
    output = 0
    for i in xrange(2):
        output += Sbox_inv[( state >> (i * 4)) & 0xF] << (i * 4)
    return output


def pLayer(state):
    output = 0
    for i in xrange(8):
        output += ((state >> i) & 0x01) << PBox[i]
    return output


def pLayer_dec(state):
    output = 0
    for i in xrange(8):
        output += ((state >> i) & 0x01) << PBox_inv[i]
    return output


def string2number(i):
    """ Convert a string to a number

    Input: string (big-endian)
    Output: long or integer
    """
    return int(i.encode('hex'), 16)


def number2string_N(i, N):
    """Convert a number to a string of fixed size

    i: long or integer
    N: length of string
    Output: string (big-endian)
    """
    s = '%0*x' % (N * 2, i)
    return s.decode('hex')


class ResultHolder(object):
    def __init__(self, plain_text, key, encrypted_text):
        self.plain_text = plain_text
        self.key = key
        self.encrypted_text = encrypted_text

    def __unicode__(self):
        return u'plain_text = %s | key = %s | encrypted_text = %s' % (
            str(self.plain_text), str(self.key), str(self.encrypted_text))

    def __str__(self):
        return self.__unicode__()


class CoincidenceHolder(object):
    def __init__(self, results):
        self.results = results
        self.coincidence_map = {}

    def check_coincidences(self):
        for result in self.results:
            if self.coincidence_map.has_key(result.encrypted_text):
                coincidence_amount = self.coincidence_map.get(result.encrypted_text)
                coincidence_amount += 1
                self.coincidence_map[result.encrypted_text] = coincidence_amount
            else:
                self.coincidence_map[result.encrypted_text] = 1


def run_for_lab():
    results = []
    plain_text = 0
    for key in range(0, 2 << 16 - 1):
        cipher = MiniPresent(key)
        encrypted_text = cipher.encrypt(plain_text)
        decrypted_text = cipher.decrypt(encrypted_text)
        result = ResultHolder(decrypted_text, key, encrypted_text)
        results.append(result)
        print result
    coincidence_holder = CoincidenceHolder(results)
    coincidence_holder.check_coincidences()
    result_map = {}
    for i in coincidence_holder.coincidence_map.values():
        if result_map.has_key(i):
            result_amount = result_map.get(i)
            result_amount += 1
            result_map[i] = result_amount
        else:
            result_map[i] = 1
    all_values_amount = 0
    line_chart = pygal.Line()
    line_chart.title = 'Coincidence chart'
    line_chart.x_title = 'Number of identical numbers'
    line_chart.y_title = 'Number of identical numbers sets'
    for key, value in result_map.items():
        if value == 1:
            print("%d equal values were met %d time") % (key, value)
        else:
            print("%d equal values were met %d times") % (key, value)
        all_values_amount += key * value
    line_chart.x_labels = map(str, result_map.keys())
    line_chart.add('coincidence', result_map.values())
    print("all values amount = %d") % all_values_amount
    line_chart.render_to_file('coincidence_chart.svg')
    return results, coincidence_holder, result_map


if __name__ == "__main__":
    key = 0x0
    plain_1 = 0
    plain_2 = "1"
    plain_3 = "2"
    print plain_1
    print plain_2
    print plain_3
    cipher = MiniPresent(key)
    encrypted_1 = cipher.encrypt(plain_1)
    encrypted_2 = cipher.encrypt(plain_2)
    encrypted_3 = cipher.encrypt(plain_3)
    enc_1 = encrypted_1
    enc_2 = encrypted_2.encode('hex')
    enc_3 = encrypted_3.encode('hex')
    print enc_1
    print enc_2
    print enc_3

    decrypted_1 = cipher.decrypt(encrypted_1)
    decrypted_2 = cipher.decrypt(encrypted_2)
    decrypted_3 = cipher.decrypt(encrypted_3)
    decr_1 = decrypted_1
    decr_2 = decrypted_2.encode('hex')
    decr_3 = decrypted_3.encode('hex')
    print decr_1
    print decr_2.decode('hex')
    print decr_3.decode('hex')

    results = run_for_lab()