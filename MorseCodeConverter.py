import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Style, ttk
import winsound
import time

# Morse Code Dictionary
morse_code_dict = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
                   'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
                   'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
                   'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
                   '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
                   '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
                   ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
                   '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
                   }

# Reverse Morse Code Dictionary
reverse_morse_code_dict = {v: k for k, v in morse_code_dict.items()}

# Function to show the 'text to morse code' translation screen
def show_text_to_morse():
    home_frame.pack_forget()
    translation_frame.pack()
    translation_label.config(text="Input Text:")
    translation_button.config(text="Translate to Morse Code")
    translation_button.config(command=text_to_morse_code)

def show_morse_code_to_text():
    home_frame.pack_forget()
    translation_frame.pack()
    translation_label.config(text="Input Morse Code:")
    translation_button.config(text="Translate to Text")
    translation_button.config(command=morse_code_to_text)

# Function to show the home screen
def show_home_screen():
    translation_frame.pack_forget()
    home_frame.pack()
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")

# Function to translate text to morse code
def text_to_morse_code():
    text = input_text.get("1.0", "end").strip().upper()
    if not text:
        messagebox.showwarning("Empty Input", "Please enter some text.")
        return

    try:
        morse_code = " ".join(morse_code_dict[char] if char in morse_code_dict else char for char in text)
        output_text.delete("1.0", "end")
        output_text.insert("1.0", morse_code)
    except KeyError as e:
        messagebox.showerror("Invalid Character", f"Character '{e.args[0]}' cannot be translated to Morse code.")

# Function to translate Morse Code to Text
def morse_code_to_text():
    morse_code = input_text.get("1.0", "end").strip().split(" ")
    if not morse_code:
        messagebox.showwarning("Empty Input", "Please enter some Morse code.")
        return

    text = ""
    for code in morse_code:
        if code in reverse_morse_code_dict:
            text += reverse_morse_code_dict[code]
        else:
            text += code
    output_text.delete("1.0", "end")
    output_text.insert("1.0", text)

# Function to clear the input and output fields and show the home screen
def clear_text():
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")
    show_home_screen()

# Save translation to file
def save_translation():
    text = output_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Empty Output", "There is no translated text to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text)
        messagebox.showinfo("Saved", "Translation saved successfully.")

# Load translation from file
def load_translation():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        input_text.delete("1.0", "end")
        input_text.insert("1.0", content)

# Add custom character to Morse code dictionary
def add_custom_character():
    def save_custom_character():
        char = char_entry.get().strip().upper()
        code = code_entry.get().strip()
        if char and code:
            morse_code_dict[char] = code
            reverse_morse_code_dict[code] = char
            messagebox.showinfo("Success", "Custom character added.")
            custom_char_window.destroy()
        else:
            messagebox.showwarning("Invalid Input", "Please enter both character and code.")

    custom_char_window = tk.Toplevel(window)
    custom_char_window.title("Add Custom Character")

    ttk.Label(custom_char_window, text="Character:").pack(pady=5)
    char_entry = ttk.Entry(custom_char_window)
    char_entry.pack(pady=5)

    ttk.Label(custom_char_window, text="Morse Code:").pack(pady=5)
    code_entry = ttk.Entry(custom_char_window)
    code_entry.pack(pady=5)

    ttk.Button(custom_char_window, text="Save", command=save_custom_character).pack(pady=10)

# Play Morse code as audio
def play_morse_code(morse_code):
    for symbol in morse_code:
        if symbol == ".":
            winsound.Beep(1000, 200)  # Frequency: 1000 Hz, Duration: 200 ms
        elif symbol == "-":
            winsound.Beep(1000, 600)  # Frequency: 1000 Hz, Duration: 600 ms
        elif symbol == " ":
            time.sleep(0.2)  # Space between characters
        elif symbol == "/":
            time.sleep(0.6)  # Space between words

# Create the main window
window = tk.Tk()
style = Style(theme="superhero")
window = style.master
window.title("Enhanced Morse Code Translator")
window.geometry("600x600")

# Create home screen
home_frame = ttk.Frame(window, padding="20")
home_frame.pack()

home_label = ttk.Label(home_frame, text="Select Translation Type:",
                       font=('Arial', 20, 'bold'))
home_label.pack(pady=10)

# Text -> Morse Code button
text_to_morse_code_btn = ttk.Button(home_frame, text="Text to Morse Code",
                                    command=show_text_to_morse, style="success.TButton")
text_to_morse_code_btn.pack(pady=5)

# Morse Code -> text button
morse_code_to_text_btn = ttk.Button(home_frame, text="Morse Code to Text",
                                    command=show_morse_code_to_text, style="info.TButton")
morse_code_to_text_btn.pack(pady=5)

# Save translation button
save_btn = ttk.Button(home_frame, text="Save Translation", command=save_translation, style="primary.TButton")
save_btn.pack(pady=5)

# Load translation button
load_btn = ttk.Button(home_frame, text="Load Translation", command=load_translation, style="warning.TButton")
load_btn.pack(pady=5)

# Add custom character button
add_custom_btn = ttk.Button(home_frame, text="Add Custom Character", command=add_custom_character, style="danger.TButton")
add_custom_btn.pack(pady=5)

# Create translation screen
translation_frame = ttk.Frame(window, padding="20")

# Create label for input text
translation_label = ttk.Label(translation_frame, text="Input Text:",
                              font=('Arial', 20, 'bold'))
translation_label.pack(pady=10)

# Create input text field
input_text = tk.Text(translation_frame, height=5, font=('Arial', 12))
input_text.pack()

# Create label for output text
output_text_label = ttk.Label(translation_frame, text="Output Text:",
                              font=('Arial', 20, 'bold'))
output_text_label.pack(pady=10)

# Create output text field
output_text = tk.Text(translation_frame, height=5, font=('Arial', 12))
output_text.pack()

# Create translation button
translation_button = ttk.Button(translation_frame, text="Translate", command=None, style="success.TButton")
translation_button.pack(pady=15)

# Create back button to return to home screen
back_button = ttk.Button(translation_frame, text="Back", command=show_home_screen, style="danger.TButton")
back_button.pack(pady=5)

# Create play button to play Morse code audio
play_button = ttk.Button(translation_frame, text="Play Morse Code", command=lambda: play_morse_code(output_text.get("1.0", "end").strip()), style="info.TButton")
play_button.pack(pady=5)

# Hide translation screen initially
translation_frame.pack_forget()

window.mainloop()
