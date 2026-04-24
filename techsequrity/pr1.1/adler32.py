def adler32(data: bytes) -> str:
    MOD_ADLER = 65521

    a = 1
    b = 0

    for byte in data:
        a = (a + byte) % MOD_ADLER
        b = (b + a) % MOD_ADLER

    # об'єднання у 32-біт
    result = (b << 16) | a

    return f"{result:08x}"


def adler32_file(path: str) -> str:
    with open(path, 'rb') as f:
        return adler32(f.read())


# --- тест ---
if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("Adler32:", adler32_file(file_path))