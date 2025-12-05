import os
import time

fifo = 'myfifo'

# Створення FIFO, якщо не існує
if not os.path.exists(fifo):
    os.mkfifo(fifo)

os.chmod(fifo, 0o666)  # rw-rw-rw-
# Запис даних у канал
with open(fifo, 'w') as f:
    for i in range(5):
        msg = f"Повідомлення {i}\n"
        print(f"Запис: {msg.strip()}")
        f.write(msg)
        f.flush()
        time.sleep(1)
