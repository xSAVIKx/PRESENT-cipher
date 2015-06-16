import random

from gmac.pyGMAC import generate_IV, GMAC

__author__ = 'Iurii Sergiichuk'


def generate_16_bits():
    m = random.getrandbits(16)
    while (m == 0):
        m = random.getrandbits(16)
    return m


def test_n1():
    tests_amount = 100
    keys_amount = 2 << 16
    n1_max_average = 0
    n1_ghash_max_average = 0
    for i in xrange(tests_amount):
        n1_list = []
        n1_ghash_list = []
        for j in xrange(tests_amount):
            n1 = 0
            n1_ghash = 0
            for key in xrange(keys_amount):
                IV1 = generate_IV()
                IV2 = generate_IV()
                while (IV1 == IV2):
                    IV2 = generate_IV()
                gmac = GMAC(key)
                m1 = generate_16_bits()
                m2 = generate_16_bits()
                while (m1 == m2):
                    m2 = generate_16_bits()
                C1 = gmac.generate(m1, IV1)
                ghash_C1 = gmac.get_state()
                C2 = gmac.generate(m2, IV2)
                ghash_C2 = gmac.get_state()
                if C1 == C2:
                    n1 += 1
                if ghash_C1 == ghash_C2:
                    n1_ghash += 1
            n1_list.append(n1)
            n1_ghash_list.append(n1_ghash)
        n1_max_average += max(n1_list)
        n1_ghash_max_average += max(n1_ghash_list)
    n1_max_average /= tests_amount
    n1_ghash_max_average /= tests_amount
    return (n1_max_average, n1_ghash_max_average)


if __name__ == "__main__":
    n1_result = test_n1()
    with open('./n1_result.txt', 'w+') as n1_result_file:
        n1_result_file.write(str(n1_result))
