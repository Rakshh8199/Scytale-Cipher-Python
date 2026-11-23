
import tkinter as tk
from tkinter import ttk, messagebox
from math import ceil


# ---------- SCYTALE CIPHER ALGORITHM ----------

def encrypt_scytale(text, key):
    if key < 1:
        raise ValueError("Key must be a positive integer.")

    # Create rows with 'key' columns
    rows = [text[i:i + key] for i in range(0, len(text), key)]

    # Read column by column
    ciphertext = ""
    for col in range(key):
        for row in rows:
            if col < len(row):
                ciphertext += row[col]

    return ciphertext


def decrypt_scytale(ciphertext, key):
    if key < 1:
        raise ValueError("Key must be a positive integer.")

    n = len(ciphertext)
    if n == 0:
        return ""

    row_count = ceil(n / key)
    remainder = n % key

    # Find the actual length of each column
    col_lengths = []
    for col in range(key):
        if remainder == 0 or col < remainder:
            col_lengths.append(row_count)
        else:
            col_lengths.append(row_count - 1)

    # Reconstruct columns from ciphertext
    columns = []
    position = 0

    for length in col_lengths:
        columns.append(ciphertext[position:position + length])
        position += length

    # Read row by row to recover plaintext
    plaintext = ""
    for row in range(row_count):
        for col in range(key):
            if row < len(columns[col]):
                plaintext += columns[col][row]

    return plaintext


def show_matrix(text, key):
    rows = [text[i:i + key] for i in range(0, len(text), key)]
    return "\n".join("  ".join(row) for row in rows)


# ---------- GRAPHICAL USER INTERFACE ----------

root = tk.Tk()
root.title("Scytale Cipher - CNS Project")
root.geometry("780x700")
root.configure(bg="#eef2f7")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Action.TButton",
    font=("Arial", 12, "bold"),
    padding=10
)

title = tk.Label(
    root,
    text="SCYTALE CIPHER",
    font=("Arial", 25, "bold"),
    bg="#eef2f7",
    fg="#17365d"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Encryption and Decryption Using Transposition Cipher",
    font=("Arial", 11),
    bg="#eef2f7"
)
subtitle.pack(pady=(0, 15))


# Input area
tk.Label(
    root, text="Enter Message:",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=30)

input_text = tk.Text(root, height=4, font=("Consolas", 12), wrap="word")
input_text.pack(fill="x", padx=30, pady=7)

key_frame = tk.Frame(root, bg="#eef2f7")
key_frame.pack(pady=10)

tk.Label(
    key_frame, text="Scytale Key (Columns):",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(side="left", padx=8)

key_entry = tk.Entry(key_frame, width=10, font=("Arial", 12))
key_entry.insert(0, "4")
key_entry.pack(side="left")


# Output area
tk.Label(
    root, text="Result:",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=30)

output_text = tk.Text(root, height=4, font=("Consolas", 12), wrap="word")
output_text.pack(fill="x", padx=30, pady=7)

tk.Label(
    root, text="Scytale Matrix Visualization:",
    font=("Arial", 12, "bold"),
    bg="#eef2f7"
).pack(anchor="w", padx=30, pady=(10, 0))

matrix_text = tk.Text(
    root, height=8,
    font=("Consolas", 12),
    bg="#e0eaf5",
    wrap="none"
)
matrix_text.pack(fill="both", expand=True, padx=30, pady=7)


def get_values():
    text = input_text.get("1.0", "end-1c")
    if not text:
        raise ValueError("Please enter a message.")

    try:
        key = int(key_entry.get())
    except ValueError:
        raise ValueError("Please enter a valid integer key.")

    if key < 1:
        raise ValueError("Key must be greater than zero.")

    return text, key


def display_result(result, matrix_source, key):
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", result)

    matrix_text.delete("1.0", tk.END)
    matrix_text.insert("1.0", show_matrix(matrix_source, key))


def encrypt_action():
    try:
        text, key = get_values()
        encrypted = encrypt_scytale(text, key)
        display_result(encrypted, text, key)
    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


def decrypt_action():
    try:
        text, key = get_values()
        decrypted = decrypt_scytale(text, key)
        display_result(decrypted, decrypted, key)
    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


def copy_action():
    result = output_text.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(result)
    root.update()
    messagebox.showinfo("Copied", "Result copied to clipboard!")


def clear_action():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    matrix_text.delete("1.0", tk.END)


button_frame = tk.Frame(root, bg="#eef2f7")
button_frame.pack(pady=15)

ttk.Button(
    button_frame, text="Encrypt",
    style="Action.TButton",
    command=encrypt_action
).grid(row=0, column=0, padx=5)

ttk.Button(
    button_frame, text="Decrypt",
    style="Action.TButton",
    command=decrypt_action
).grid(row=0, column=1, padx=5)

ttk.Button(
    button_frame, text="Copy Result",
    style="Action.TButton",
    command=copy_action
).grid(row=0, column=2, padx=5)

ttk.Button(
    button_frame, text="Clear",
    style="Action.TButton",
    command=clear_action
).grid(row=0, column=3, padx=5)

footer = tk.Label(
    root,
    text="Cryptography and Network Security | Scytale Cipher Project",
    font=("Arial", 10),
    bg="#eef2f7",
    fg="#666666"
)
footer.pack(pady=(0, 12))

root.mainloop()
