import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageGrab
from threading import Thread
import keyboard
import time
import tkinter as tk
from tkinter import messagebox
import win32gui


# -------------------------------
# GUI
# -------------------------------
def create_gui():
    root = tk.Tk()
    root.title("Mini Hash Tool")
    root.geometry("400x200")

    text = tk.Text(root, height=5)
    text.pack(fill="both", expand=True, padx=10, pady=10)

    def copy_hash():
        content = text.get("1.0", "end").strip()
        pyperclip.copy(content)
        messagebox.showinfo("Copied", "Copied to clipboard!")

    btn = tk.Button(root, text="Copy", command=copy_hash)
    btn.pack(pady=5)

    root.mainloop()


# -------------------------------
# Clipboard monitor
# -------------------------------
def monitor_clipboard():
    last = ""

    while True:
        try:
            data = pyperclip.paste()
            if data != last:
                last = data
                print("Clipboard:", data)
        except:
            pass
        time.sleep(1)


# -------------------------------
# Screenshot (Ctrl+Shift+S)
# -------------------------------
def screenshot():
    time.sleep(0.3)
    img = ImageGrab.grab()
    img.save("screenshot.png")
    print("Screenshot saved!")


# -------------------------------
# Tray icon
# -------------------------------
def create_tray():
    def on_exit(icon, item):
        icon.stop()

    def on_show(icon, item):
        Thread(target=create_gui).start()

    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 54, 54), fill="white")

    menu = pystray.Menu(
        pystray.MenuItem("Show GUI", on_show),
        pystray.MenuItem("Exit", on_exit)
    )

    icon = pystray.Icon("HashTool", image, "Hash Tool", menu)
    icon.run()


# -------------------------------
# Hotkeys
# -------------------------------
def register_hotkeys():
    keyboard.add_hotkey("ctrl+shift+s", screenshot)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    # запуск clipboard monitor
    Thread(target=monitor_clipboard, daemon=True).start()

    # гарячі клавіші
    register_hotkeys()

    # tray
    create_tray()