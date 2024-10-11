import re
import tkinter as tk
from tkinter import messagebox

def is_Chinese(word):
    """Check if a string contains any Chinese characters."""
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def is_al_num(word):
    """Check if a word is alphanumeric, excluding certain symbols."""
    word = word.replace("_", "").replace(" ", "").replace("()", "").encode('UTF-8')
    return word.isalnum()

def beautifyText(text, pattern, isloop):
    """Format text based on patterns, ensuring correct spacing."""
    res = re.compile(pattern)
    segments = res.split(text)
    result = ""

    for index, segment in enumerate(segments):
        if "\n" == segment:
            result += segment
            continue

        if is_Chinese(segment):
            result += segment
        elif is_al_num(segment):
            # Adjust spaces around alphanumeric segments
            if isloop and index == 0:
                result += (segment.strip() + " ")
            else:
                result += (" " + segment.strip() + " ")
        else:
            # Handle punctuation and symbols to ensure spacing
            if isloop:
                result += beautifyText(segment, r"([。，？！,!：\-]+)", False)
            else:
                result += add_spacing(segment)
    return result

def add_spacing(segment):
    """Add a single space around specific characters."""
    # Define characters that should have spaces around them
    symbols_with_spaces = [":", "-", "：", "—", "–"]

    # Use regex to find these symbols and add spaces around them
    for symbol in symbols_with_spaces:
        segment = re.sub(f" *{re.escape(symbol)} *", f" {symbol} ", segment)
    
    # Remove extra spaces created by the replacements
    segment = re.sub(r'\s+', ' ', segment).strip()
    
    return segment

def process_beautify():
    """Process the input text and display beautified text."""
    input_text = text_widget.get("1.0", tk.END).strip()
    if input_text:
        beautified_text = beautifyText(input_text, r"([\u4e00-\u9fff])", True)
        display_result(beautified_text)

def process_replace():
    """Replace specific patterns and display the replaced text."""
    input_text = text_widget.get("1.0", tk.END).strip()
    if input_text:
        pattern = r'(\[|\])'
        replaced_text = re.sub(pattern, '', input_text)
        display_result(replaced_text)

def display_result(result_text):
    """Display the processed text in the result text widget."""
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete("1.0", tk.END)
    result_text_widget.insert(tk.END, result_text)
    result_text_widget.config(state=tk.DISABLED)

def copy_to_clipboard():
    """Copy the processed text to the clipboard."""
    result_text = result_text_widget.get("1.0", tk.END).strip()
    if result_text:
        root.clipboard_clear()
        root.clipboard_append(result_text)
        messagebox.showinfo("Copied", "Processed text copied to clipboard!")


# Create the main window
root = tk.Tk()
root.title("Text Processor")

# Create a Text widget for multi-line input
text_widget = tk.Text(root, height=15, width=80)
text_widget.pack(pady=10)

# Create a Text widget to display the result
result_text_widget = tk.Text(root, height=15, width=80, state=tk.DISABLED)
result_text_widget.pack(pady=10)

# Create buttons
btn_beautify = tk.Button(root, text="Beautify Text", command=process_beautify)
btn_replace = tk.Button(root, text="Replace Text", command=process_replace)
btn_copy = tk.Button(root, text="Copy", command=copy_to_clipboard)

# Pack buttons
btn_beautify.pack(side=tk.LEFT, padx=5, pady=5)
btn_replace.pack(side=tk.LEFT, padx=5, pady=5)
btn_copy.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()

