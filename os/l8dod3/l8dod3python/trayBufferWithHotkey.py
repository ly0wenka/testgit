import pyperclip
import pystray
from PIL import Image, ImageDraw
from threading import Thread
import keyboard  # For hotkeys

# --- Clipboard Functions ---
def clean_formatting():
    """Remove all formatting, keep plain text"""
    try:
        text = pyperclip.paste()
        pyperclip.copy(text)
        print("Clipboard formatting cleared!")
    except Exception as e:
        print(f"Error: {e}")

def clear_clipboard():
    """Empty the clipboard"""
    try:
        pyperclip.copy("")
        print("Clipboard cleared!")
    except Exception as e:
        print(f"Error: {e}")

def uppercase_clipboard():
    """Convert clipboard text to uppercase"""
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

# --- Create a simple icon ---
def create_icon():
    width = 64
    height = 64
    image = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="black")
    draw.text((10, 20), "CB", fill="white")
    return image

# --- Tray Menu ---
def on_quit(icon, item):
    icon.stop()
    keyboard.unhook_all_hotkeys()  # Remove hotkeys on quit

icon = pystray.Icon(
    "clipboard_manager",
    create_icon(),
    "Clipboard Utility",
    menu=pystray.Menu(
        pystray.MenuItem("Clean Formatting", clean_formatting),
        pystray.MenuItem("Clear Clipboard", lambda icon, item: clear_clipboard()),
        pystray.MenuItem("Uppercase Clipboard", lambda icon, item: uppercase_clipboard()),
        pystray.MenuItem("Lowercase Clipboard", lambda icon, item: lowercase_clipboard()),
        pystray.MenuItem("Quit", on_quit)
    )
)

# --- Hotkeys ---
def setup_hotkeys():
    # Example hotkeys (Windows):
    keyboard.add_hotkey("ctrl+shift+c", clean_formatting)
    keyboard.add_hotkey("ctrl+shift+x", clear_clipboard)
    keyboard.add_hotkey("ctrl+shift+u", uppercase_clipboard)
    keyboard.add_hotkey("ctrl+shift+l", lowercase_clipboard)

# --- Run tray ---
def run_tray():
    setup_hotkeys()
    icon.run()

Thread(target=run_tray).start()
