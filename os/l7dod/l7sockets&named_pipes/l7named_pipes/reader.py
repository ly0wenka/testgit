import os

fifo = '/tmp/myfifo'

# Читання даних з каналу
with open(fifo, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        print(f"Прочитано: {line.strip()}")
