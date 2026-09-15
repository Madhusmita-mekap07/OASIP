import string
import secrets
import tkinter as tk
from tkinter import messagebox
import pyperclip

def generate_password():
    length = int(slider_length.get())
    
    use_upper = var_upper.get()
    use_lower = var_lower.get()
    use_digits = var_digits.get()
    use_symbols = var_symbols.get()
    
    # At least 2 types must be selected rule
    selected_types = sum([use_upper, use_lower, use_digits, use_symbols])
    if selected_types < 2:
        messagebox.showerror("Error", "Please select at least 2 character types!")
        return

    char_pool = ""
    guaranteed_chars = []

    if use_upper:
        char_pool += string.ascii_uppercase
        guaranteed_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        char_pool += string.ascii_lowercase
        guaranteed_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        char_pool += string.digits
        guaranteed_chars.append(secrets.choice(string.digits))
    if use_symbols:
        char_pool += string.punctuation
        guaranteed_chars.append(secrets.choice(string.punctuation))

    # Exclude ambiguous characters option
    if var_exclude.get():
        for char in "0O1lI":
            char_pool = char_pool.replace(char, "")

    # Generate remaining characters securely using secrets module
    remaining_length = length - len(guaranteed_chars)
    password_list = guaranteed_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
    
    # Shuffle for randomness
    secrets.SystemRandom().shuffle(password_list)
    password = "".join(password_list)

    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    # Strength evaluation
    evaluate_strength(password, selected_types)

def evaluate_strength(password, types_count):
    length = len(password)
    if length >= 12 and types_count >= 3:
        lbl_strength.config(text="Strength: Strong 💪", fg="#10b981")
    elif length >= 8 and types_count >= 2:
        lbl_strength.config(text="Strength: Medium 🟡", fg="#f59e0b")
    else:
        lbl_strength.config(text="Strength: Weak 🔴", fg="#ef4444")

def copy_to_clipboard():
    pwd = entry_password.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password generated yet!")

# GUI Layout
root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("400x420")
root.resizable(False, False)

tk.Label(root, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Slider for Length
frame_length = tk.Frame(root)
frame_length.pack(pady=5)
tk.Label(frame_length, text="Length:").pack(side=tk.LEFT)
slider_length = tk.Scale(frame_length, from_=8, to=32, orient=tk.HORIZONTAL)
slider_length.set(12)
slider_length.pack(side=tk.LEFT)

# Checkboxes
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)
var_exclude = tk.BooleanVar(value=False)

frame_opts = tk.Frame(root)
frame_opts.pack(pady=10)

tk.Checkbutton(frame_opts, text="Uppercase (A-Z)", variable=var_upper).grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame_opts, text="Lowercase (a-z)", variable=var_lower).grid(row=0, column=1, sticky="w")
tk.Checkbutton(frame_opts, text="Digits (0-9)", variable=var_digits).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_opts, text="Symbols (!@#)", variable=var_symbols).grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame_opts, text="Exclude Ambiguous (0,O,1,l)", variable=var_exclude).grid(row=2, column=0, columnspan=2, sticky="w")

btn_gen = tk.Button(root, text="Generate Password", command=generate_password, bg="#10b981", fg="white", font=("Arial", 10, "bold"))
btn_gen.pack(pady=10)

entry_password = tk.Entry(root, font=("Arial", 12), width=25, justify="center")
entry_password.pack(pady=5)

lbl_strength = tk.Label(root, text="Strength: --", font=("Arial", 10, "bold"))
lbl_strength.pack(pady=5)

btn_copy = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#0284c7", fg="white")
btn_copy.pack(pady=5)

root.mainloop()