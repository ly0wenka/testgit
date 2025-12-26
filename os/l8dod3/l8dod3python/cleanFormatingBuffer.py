import pyperclip

# Get current clipboard content
text = pyperclip.paste()

# Put it back as plain text (removes formatting)
pyperclip.copy(text)

print("Clipboard formatting cleared, plain text preserved!")
