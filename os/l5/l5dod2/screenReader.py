import pyperclip
import pystray
from PIL import Image, ImageDraw, ImageGrab
from threading import Thread
import keyboard
import time

# --- Clipboard Functions ---
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

# --- GIF Screen Recording ---
screenshot_frames = []

def capture_screen():
    """Take a screenshot and append to frames"""
    global screenshot_frames
    screenshot = ImageGrab.grab()
    screenshot_frames.append(screenshot)
    print("Screenshot captured!")

def save_gif():
    """Save captured frames as GIF"""
    if screenshot_frames:
        filename = f"screenshots_{int(time.time())}.gif"
        screenshot_frames[0].save(
            filename,
            save_all=True,
            append_images=screenshot_frames[1:],
            duration=5000,
            loop=0
        )
        print(f"GIF saved as {filename}")
        screenshot_frames.clear()
    else:
        print("No screenshots to save!")

# --- Create Tray Icon ---
def create_icon():
    width = 64
    height = 64
    image = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="red")
    draw.text((10, 20), "CB", fill="white")
    return image

def on_quit(icon, item):
    icon.stop()
    keyboard.unhook_all_hotkeys()

icon = pystray.Icon(
    "clipboard_manager",
    create_icon(),
    "Clipboard & Screen Recorder",
    menu=pystray.Menu(
        pystray.MenuItem("Clean Formatting", clean_formatting),
        pystray.MenuItem("Clear Clipboard", lambda icon, item: clear_clipboard()),
        pystray.MenuItem("Uppercase Clipboard", lambda icon, item: uppercase_clipboard()),
        pystray.MenuItem("Lowercase Clipboard", lambda icon, item: lowercase_clipboard()),
        pystray.MenuItem("Capture Screen", lambda icon, item: capture_screen()),
        pystray.MenuItem("Save GIF", lambda icon, item: save_gif()),
        pystray.MenuItem("Quit", on_quit)
    )
)

# --- Hotkeys ---
def setup_hotkeys():
    keyboard.add_hotkey("ctrl+shift+c", clean_formatting)
    keyboard.add_hotkey("ctrl+shift+x", clear_clipboard)
    keyboard.add_hotkey("ctrl+shift+u", uppercase_clipboard)
    keyboard.add_hotkey("ctrl+shift+l", lowercase_clipboard)
    keyboard.add_hotkey("ctrl+shift+s", capture_screen)  # capture screen
    keyboard.add_hotkey("ctrl+shift+g", save_gif)        # save GIF

# --- Run Tray ---
def run_tray():
    setup_hotkeys()
    icon.run()

Thread(target=run_tray).start()
