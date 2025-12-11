import socket
import os

SOCKET_PATH = "/tmp/ipc_socket"

# Видаляємо старий сокет
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
    server.bind(SOCKET_PATH)
    server.listen()
    print("Сервер очікує клієнта...")

    conn, _ = server.accept()
    with conn:
        print("Клієнт підключений")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Отримано: {data.decode()}")
            conn.sendall(f"Відповідь: {data.decode()}".encode())
