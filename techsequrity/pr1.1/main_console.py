import os

# імпорти твоїх алгоритмів
from adler32 import adler32_file
from crc32 import crc32_file
from md4 import md4_file
from md5 import md5_file
from sha1 import sha1_file
from sha256 import sha256_file
from sha384 import sha384_file
from sha512 import sha512_file

# ці поки "wronghash", але підключимо
from panama_wronghash import panama_file
from ripemd160_wronghash import ripemd160_file
from tiger_wronghash import tiger_file


def print_menu():
    print("\n=== HASH CALCULATOR ===")
    print("1. MD4")
    print("2. MD5")
    print("3. SHA1")
    print("4. SHA256")
    print("5. SHA384")
    print("6. SHA512")
    print("7. RIPEMD160")
    print("8. PANAMA")
    print("9. TIGER")
    print("10. ADLER32")
    print("11. CRC32")
    print("12. ALL")
    print("0. Exit")


def main():
    file_path = input("Enter file path: ").strip()

    if not os.path.exists(file_path):
        print("File not found!")
        return

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        try:
            if choice == "1":
                print("MD4:", md4_file(file_path))

            elif choice == "2":
                print("MD5:", md5_file(file_path))

            elif choice == "3":
                print("SHA1:", sha1_file(file_path))

            elif choice == "4":
                print("SHA256:", sha256_file(file_path))

            elif choice == "5":
                print("SHA384:", sha384_file(file_path))

            elif choice == "6":
                print("SHA512:", sha512_file(file_path))

            elif choice == "7":
                print("RIPEMD160:", ripemd160_file(file_path))

            elif choice == "8":
                print("PANAMA:", panama_file(file_path))

            elif choice == "9":
                print("TIGER:", tiger_file(file_path))

            elif choice == "10":
                print("ADLER32:", adler32_file(file_path))

            elif choice == "11":
                print("CRC32:", crc32_file(file_path))

            elif choice == "12":
                print("\n--- ALL HASHES ---")
                print("MD4:", md4_file(file_path))
                print("MD5:", md5_file(file_path))
                print("SHA1:", sha1_file(file_path))
                print("SHA256:", sha256_file(file_path))
                print("SHA384:", sha384_file(file_path))
                print("SHA512:", sha512_file(file_path))
                print("RIPEMD160:", ripemd160_file(file_path))
                print("PANAMA:", panama_file(file_path))
                print("TIGER:", tiger_file(file_path))
                print("ADLER32:", adler32_file(file_path))
                print("CRC32:", crc32_file(file_path))

            elif choice == "0":
                print("Exit.")
                break

            else:
                print("Invalid choice!")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()