import struct

# Допоміжна функція
def left_rotate(x, n):
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


# Основна функція MD4
def md4(message: bytes) -> str:
    # Ініціалізаційні значення
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Паддінг
    original_len_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message += b'\x80'

    while len(message) % 64 != 56:
        message += b'\x00'

    message += struct.pack('<Q', original_len_bits)

    # Обробка блоків по 512 біт
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        X = list(struct.unpack('<16I', chunk))

        AA, BB, CC, DD = A, B, C, D

        # Раунд 1
        S = [3, 7, 11, 19]
        for i in range(16):
            if i % 4 == 0:
                A = left_rotate((A + ((B & C) | (~B & D)) + X[i]) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 1:
                D = left_rotate((D + ((A & B) | (~A & C)) + X[i]) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 2:
                C = left_rotate((C + ((D & A) | (~D & B)) + X[i]) & 0xFFFFFFFF, S[i % 4])
            else:
                B = left_rotate((B + ((C & D) | (~C & A)) + X[i]) & 0xFFFFFFFF, S[i % 4])

        # Раунд 2
        S = [3, 5, 9, 13]
        index = [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]

        for i in range(16):
            k = index[i]
            if i % 4 == 0:
                A = left_rotate((A + ((B & C) | (B & D) | (C & D)) + X[k] + 0x5A827999) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 1:
                D = left_rotate((D + ((A & B) | (A & C) | (B & C)) + X[k] + 0x5A827999) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 2:
                C = left_rotate((C + ((D & A) | (D & B) | (A & B)) + X[k] + 0x5A827999) & 0xFFFFFFFF, S[i % 4])
            else:
                B = left_rotate((B + ((C & D) | (C & A) | (D & A)) + X[k] + 0x5A827999) & 0xFFFFFFFF, S[i % 4])

        # Раунд 3
        S = [3, 9, 11, 15]
        index = [0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]

        for i in range(16):
            k = index[i]
            if i % 4 == 0:
                A = left_rotate((A + (B ^ C ^ D) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 1:
                D = left_rotate((D + (A ^ B ^ C) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, S[i % 4])
            elif i % 4 == 2:
                C = left_rotate((C + (D ^ A ^ B) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, S[i % 4])
            else:
                B = left_rotate((B + (C ^ D ^ A) + X[k] + 0x6ED9EBA1) & 0xFFFFFFFF, S[i % 4])

        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF

    return ''.join(f'{x:02x}' for x in struct.pack('<4I', A, B, C, D))


# Хеш для txt файлу
def md4_file(path: str) -> str:
    with open(path, 'rb') as f:
        data = f.read()
    return md4(data)


if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("MD4:", md4_file(file_path))