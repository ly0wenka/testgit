def crc32(data: bytes) -> str:
    poly = 0xEDB88320  # стандартний поліном CRC32 (реверсований)
    crc = 0xFFFFFFFF

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1

    crc ^= 0xFFFFFFFF

    return f"{crc:08x}"


def crc32_file(path: str) -> str:
    with open(path, 'rb') as f:
        return crc32(f.read())


# --- тест ---
if __name__ == "__main__":
    file_path = r"C:\Users\L\Desktop\Hash.txt"
    print("CRC32:", crc32_file(file_path))