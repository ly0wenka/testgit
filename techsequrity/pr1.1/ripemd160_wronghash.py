import struct

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def ripemd160(message: bytes) -> str:
    # Початкові значення
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0

    # Функції
    def f(j, x, y, z):
        if 0 <= j <= 15:
            return x ^ y ^ z
        elif 16 <= j <= 31:
            return (x & y) | (~x & z)
        elif 32 <= j <= 47:
            return (x | ~y) ^ z
        elif 48 <= j <= 63:
            return (x & z) | (y & ~z)
        else:
            return x ^ (y | ~z)

    # Константи
    K  = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    KK = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]

    # Порядок слів
    r  = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,
        7, 4,13, 1,10, 6,15, 3,12, 0, 9, 5, 2,14,11, 8,
        3,10,14, 4, 9,15, 8, 1, 2, 7, 0, 6,13,11, 5,12,
        1, 9,11,10, 0, 8,12, 4,13, 3, 7,15,14, 5, 6, 2,
        4, 0, 5, 9, 7,12, 2,10,14, 1, 3, 8,11, 6,15,13
    ]

    rr = [
        5,14, 7, 0, 9, 2,11, 4,13, 6,15, 8, 1,10, 3,12,
        6,11, 3, 7, 0,13, 5,10,14,15, 8,12, 4, 9, 1, 2,
       15, 5, 1, 3, 7,14, 6, 9,11, 8,12, 2,10, 0, 4,13,
        8, 6, 4, 1, 3,11,15, 0, 5,12, 2,13, 9, 7,10,14,
       12,15,10, 4, 1, 5, 8, 7, 6, 2,13,14, 0, 3, 9,11
    ]

    # Зсуви
    s  = [
       11,14,15,12, 5, 8, 7, 9,11,13,14,15, 6, 7, 9, 8,
        7, 6, 8,13,11, 9, 7,15, 7,12,15, 9,11, 7,13,12,
       11,13, 6, 7,14, 9,13,15,14, 8,13, 6, 5,12, 7, 5,
       11,12,14,15,14,15, 9, 8, 9,14, 5, 6, 8, 6, 5,12,
        9,15, 5,11, 6, 8,13,12, 5,12,13,14,11, 8, 5, 6
    ]

    ss = [
        8, 9, 9,11,13,15,15, 5, 7, 7, 8,11,14,14,12, 6,
        9,13,15, 7,12, 8, 9,11, 7, 7,12, 7, 6,15,13,11,
        9, 7,15,11, 8, 6, 6,14,12,13, 5,14,13,13, 7, 5,
       15, 5, 8,11,14,14, 6,14, 6, 9,12, 9,12, 5,15, 8,
        8, 5,12, 9,12, 5,14, 6, 8,13, 6, 5,15,13,11,11
    ]

    # Padding
    bit_len = len(message) * 8
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += struct.pack('<Q', bit_len)

    # Обробка
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        X = list(struct.unpack('<16I', block))

        A1, B1, C1, D1, E1 = h0, h1, h2, h3, h4
        A2, B2, C2, D2, E2 = h0, h1, h2, h3, h4

        for j in range(80):
            T = (left_rotate(A1 + f(j, B1, C1, D1) + X[r[j]] + K[j//16], s[j]) + E1) & 0xFFFFFFFF
            A1, E1, D1, C1, B1 = E1, D1, left_rotate(C1, 10), B1, T

            T = (left_rotate(A2 + f(79-j, B2, C2, D2) + X[rr[j]] + KK[j//16], ss[j]) + E2) & 0xFFFFFFFF
            A2, E2, D2, C2, B2 = E2, D2, left_rotate(C2, 10), B2, T

        T = (h1 + C1 + D2) & 0xFFFFFFFF
        h1 = (h2 + D1 + E2) & 0xFFFFFFFF
        h2 = (h3 + E1 + A2) & 0xFFFFFFFF
        h3 = (h4 + A1 + B2) & 0xFFFFFFFF
        h4 = (h0 + B1 + C2) & 0xFFFFFFFF
        h0 = T

    return ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])


def ripemd160_file(path: str) -> str:
    with open(path, 'rb') as f:
        return ripemd160(f.read())


if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("RIPEMD-160:", ripemd160_file(file_path))