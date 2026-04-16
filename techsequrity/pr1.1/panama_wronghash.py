import struct

def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def panama(message: bytes) -> str:
    state = [0] * 17
    buffer = [[0] * 8 for _ in range(32)]
    ptr = 0

    # padding
    message += b'\x80'
    while len(message) % 32 != 0:
        message += b'\x00'

    def step(block=None):
        nonlocal state, buffer, ptr

        # --- buffer update ---
        for i in range(8):
            buffer[(ptr - 1) % 32][i] ^= buffer[(ptr - 25) % 32][i]
            buffer[(ptr - 1) % 32][i] ^= buffer[(ptr - 4) % 32][i]
            if block:
                buffer[(ptr - 1) % 32][i] ^= block[i]
            buffer[(ptr - 1) % 32][i] &= 0xFFFFFFFF

        ptr = (ptr - 1) % 32

        # --- gamma ---
        gamma = [0] * 17
        for i in range(17):
            gamma[i] = state[i] ^ (
                state[(i + 1) % 17] |
                ((~state[(i + 2) % 17]) & 0xFFFFFFFF)
            )
            gamma[i] &= 0xFFFFFFFF

        # --- pi ---
        pi = [0] * 17
        for i in range(17):
            pi[i] = left_rotate(gamma[(7 * i) % 17], (i * (i + 1) // 2) % 32)

        # --- theta ---
        theta = [0] * 17
        for i in range(17):
            theta[i] = (
                pi[i] ^
                pi[(i + 1) % 17] ^
                pi[(i + 4) % 17]
            ) & 0xFFFFFFFF

        theta[0] ^= 1

        # 🔥 правильне змішування buffer
        for i in range(8):
            theta[i + 1] ^= buffer[(ptr + i) % 32][i]
            theta[i + 1] &= 0xFFFFFFFF

        state = theta

    # --- push phase ---
    for i in range(0, len(message), 32):
        block = list(struct.unpack('<8I', message[i:i+32]))
        step(block)

    # --- pull phase ---
    for _ in range(33):  # 🔥 ключова різниця
        step()

    return ''.join(f'{x:08x}' for x in state[:8])


def panama_file(path: str) -> str:
    with open(path, 'rb') as f:
        return panama(f.read())


if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("PANAMA:", panama_file(file_path))