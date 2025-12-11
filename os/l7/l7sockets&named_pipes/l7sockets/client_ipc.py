import socket

SOCKET_PATH = "/tmp/ipc_socket"

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect(SOCKET_PATH)
    for msg in ["Привіт", "IPC тест", "Поки"]:
        print(f"Відправка: {msg}")
        client.sendall(msg.encode())
        data = client.recv(1024)
        print(f"Відповідь сервера: {data.decode()}")
