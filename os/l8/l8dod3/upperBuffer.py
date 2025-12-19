import pyperclip

# Get the current clipboard content
text = pyperclip.paste()

# Convert to uppercase
upper_text = text.upper()

# Put the uppercase text back to the clipboard
pyperclip.copy(upper_text)

print("Clipboard content converted to uppercase!")
