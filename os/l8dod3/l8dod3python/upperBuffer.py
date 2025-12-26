import pyperclip

# 1. Get the current clipboard content
# 2. Put the uppercase text back to the clipboard
text = pyperclip.paste()
pyperclip.copy(text.upper())

print("Clipboard content converted to uppercase!")
