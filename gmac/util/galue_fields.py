# Author: Joao H de A Franco (jhafranco@acm.org)
#
# Description: Binary finite field multiplication in Python 3
#
# Date: 2012-02-16
#
# License: Attribution-NonCommercial-ShareAlike 3.0 Unported
#          (CC BY-NC-SA 3.0)
# ===========================================================
from functools import reduce

# constants used in the multGF2 function
mask1 = mask2 = polyred = None


def setGF2(degree, irPoly):
    """Define parameters of binary finite field GF(2^m)/g(x)
       - degree: extension degree of binary field
       - irPoly: coefficients of irreducible polynomial g(x)
    """
    global mask1, mask2, polyred
    mask1 = mask2 = 1 << degree
    mask2 -= 1
    if sum(irPoly) <= len(irPoly):
        polyred = reduce(lambda x, y: (x << 1) + y, irPoly[1:])
    else:
        polyred = poly2Int(irPoly[1:])


def multGF2(p1, p2):
    """Multiply two polynomials in GF(2^m)/g(x)"""
    p = 0
    while p2:
        if p2 & 1:
            p ^= p1
        p1 <<= 1
        if p1 & mask1:
            p1 ^= polyred
        p2 >>= 1
    return p & mask2


# =============================================================================
#                        Auxiliary formatting functions
# =============================================================================
def int2Poly(bInt):
    """Convert a "big" integer into a "high-degree" polynomial"""
    exp = 0
    poly = []
    while bInt:
        if bInt & 1:
            poly.append(exp)
        exp += 1
        bInt >>= 1
    return poly[::-1]


def poly2Int(hdPoly):
    """Convert a "high-degree" polynomial into a "big" integer"""
    bigInt = 0
    for exp in hdPoly:
        bigInt += 1 << exp
    return bigInt


def i2P(sInt):
    """Convert a "small" integer into a "low-degree" polynomial"""
    res = [(sInt >> i) & 1 for i in reversed(range(sInt.bit_length()))]
    if len(res) == 0:
        res.append(0)
    return res


def p2I(ldPoly):
    """Convert a "low-degree" polynomial into a "small" integer"""
    return reduce(lambda x, y: (x << 1) + y, ldPoly)


def ldMultGF2(p1, p2):
    """Multiply two "low-degree" polynomials in GF(2^n)/g(x)"""
    return multGF2(p2I(p1), p2I(p2))


def hdMultGF2(p1, p2):
    """Multiply two "high-degree" polynomials in GF(2^n)/g(x)"""
    return multGF2(poly2Int(p1), poly2Int(p2))


if __name__ == "__main__":
    # Define binary field GF(2^3)/x^3 + x + 1
    setGF2(3, [1, 0, 1, 1])

    # Alternative way to define GF(2^3)/x^3 + x + 1
    setGF2(3, i2P(0b1011))

    # Check if (x + 1)(x^2 + 1) == x^2
    assert ldMultGF2([1, 1], [1, 0, 1]) == p2I([1, 0, 0])

    # Check if (x^2 + x + 1)(x^2 + 1) == x^2 + x
    assert ldMultGF2([1, 1, 1], [1, 0, 1]) == p2I([1, 1, 0])

    # Define binary field GF(2^8)/x^8 + x^4 + x^3 + x + 1
    setGF2(8, [1, 0, 0, 0, 1, 1, 0, 1, 1])

    # Alternative way to define GF(2^8)/x^8 + x^4 + x^3 + x + 1
    setGF2(8, i2P(0b100011011))

    # Check if (x)(x^7 + x^2 + x + 1) == x^4 + x^2 + 1
    assert ldMultGF2([1, 0], [1, 0, 0, 0, 0, 1, 1, 1]) == p2I([1, 0, 1, 0, 1])

    # Check if (x + 1)(x^6 + x^5 + x^3 + x^2 + x) == x^7 + x^5 + x^4 + x
    assert ldMultGF2([1, 1], [1, 1, 0, 1, 1, 1, 0]) == p2I([1, 0, 1, 1, 0, 0, 1, 0])

    # Define binary field GF(2^571)/x^571 + x^10 + x^5 + x^2 + x
    setGF2(571, [571, 10, 5, 2, 1])

    # Calculate the product of two polynomials in GF(2^571)/x^571 + x^10 + x^5 + x^2 + x,
    # x^518 + x^447 + x^320 + x^209 + x^119 + x + 1 and x^287 + x^145 + x^82 + + x^44
    print(int2Poly(hdMultGF2([518, 447, 320, 209, 119, 1, 0], [287, 145, 82, 44])))
