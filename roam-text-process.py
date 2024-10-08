import re
import tkinter as tk
from tkinter import messagebox

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def is_al_num(word):
    word = word.replace("_", "").replace(" ", "").replace("()", "").encode('UTF-8')
    if word.isalpha():
        return True
    if word.isdigit():
        return True
    if word.isalnum():
        return True
    return False

def beautifyText(text, pattern, isloop):
    res = re.compile(pattern)
    p1 = res.split(text)
    result = ""
    for index in range(len(p1)):
        str = p1[index]
        if "\n" == str:
            result += str
            continue

        if is_Chinese(str):
            result += str
        elif is_al_num(str):
            if isloop and index == 0:
                result += (str.strip() + " ")
            else:
                result += (" " + str.strip() + " ")
        else:
            if isloop:
                result += beautifyText(str, r"([。，？！,!]+)", False)
            else:
                result += str
    return result

def process_beautify():
    input_text = text_widget.get("1.0", tk.END).strip()
    if input_text:
        beautified_text = beautifyText(input_text, r"([\u4e00-\u9fff])", True)
        display_result(beautified_text)

def process_replace():
    input_text = text_widget.get("1.0", tk.END).strip()
    if input_text:
        pattern = r'(\[|\])'
        replaced_text = re.sub(pattern, '', input_text)
        display_result(replaced_text)

def display_result(result_text):
    result_text_widget.config(state=tk.NORMAL)
    result_text_widget.delete("1.0", tk.END)
    result_text_widget.insert(tk.END, result_text)
    result_text_widget.config(state=tk.DISABLED)

def copy_to_clipboard():
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

