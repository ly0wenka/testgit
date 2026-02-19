import struct
import math

# Допоміжні функції
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# Основна реалізація MD5
def md5(message: bytes) -> str:
    # Ініціалізаційні значення
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Таблиця констант
    K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

    # Зсуви
    s = [
        7, 12, 17, 22] * 4 + \
        [5, 9, 14, 20] * 4 + \
        [4, 11, 16, 23] * 4 + \
        [6, 10, 15, 21] * 4

    # Паддінг
    original_len_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += struct.pack('<Q', original_len_bits)

    # Обробка блоків по 512 біт
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        M = list(struct.unpack('<16I', chunk))

        a, b, c, d = A, B, C, D

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(f, s[i])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Формуємо hex-рядок
    return ''.join(f'{x:02x}' for x in struct.pack('<4I', A, B, C, D))


# Хеш для txt файлу
def md5_file(path: str) -> str:
    with open(path, 'rb') as f:
        data = f.read()
    return md5(data)


if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("MD5:", md5_file(file_path))
