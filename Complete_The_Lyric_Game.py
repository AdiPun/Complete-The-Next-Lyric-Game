# --- Import section ---
from tkinter import *         # Base Tkinter features
import tkinter as tk       # Themed Tkinter widgets
import random
import json

current_index = 0
pause_length = 500

# --- Functionality (callback) ---
def tokenise_words_to_json(file_path="Lyrics.txt", words_per_chunk=7):
    """
    Reads text from a .txt file, removes newlines, splits into groups of N words,
    and writes a JSON file for later use.
    """
    # Read file
    with open(file_path, "r", encoding="utf-8") as text_file:
        text = text_file.read()

    # Remove newlines and extra spaces
    clean_text = " ".join(text.split())

    # Split into list of words
    words = clean_text.split()

    # Group into chunks of 5 words
    chunks = []
    for i in range(0, len(words), words_per_chunk):
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk)

    # Write to JSON
    with open("songs.json", "w", encoding="utf-8") as json_file:
        json.dump(chunks, json_file, indent=4, ensure_ascii=False)

    print("Tokenised lyrics to songs.json")

# Run once to generate chunks.json
tokenise_words_to_json()

# Load JSON song
with open("songs.json", "r") as f:
    lyrics = json.load(f)

def next_round():
    global current_index

    if current_index >= len(lyrics) - 1:
        status_label.config(text=f"You finished the song!")
        for btn in buttons:
            btn.config(state="disabled")
        return

    # Pick a wrong line
    wrong_line = random.choice(lyrics)
    while wrong_line == lyrics[current_index + 1]:
        wrong_line = random.choice(lyrics)

    # Randomise options
    options = [lyrics[current_index + 1], wrong_line]
    random.shuffle(options)

    # Set buttons
    for i, btn in enumerate(buttons):
        btn.config(text=options[i], command=lambda t=options[i]: handle_answer(t))

    # Update current line
    status_label.config(text=f"Current line:\n'{lyrics[current_index]}'")

def handle_answer(selected_text):
    global current_index
    correct_text = lyrics[current_index + 1]
    if selected_text == correct_text:
        current_index += 1
        status_label.config(text=f"Correct! Next line:\n'{correct_text}'")
        root.after(pause_length, next_round)
    else:
        status_label.config(text="Wrong! Try again.")

# --- Main window setup ---
root = Tk()                   # Create the main window
root.title("Lyric matching game")   # Set window title
root.geometry("400x250")      # Set fixed size (optional)

status_label = tk.Label(root, text="", font=("Segoe UI", 12), wraplength=350, justify="center")
status_label.pack(pady=20)

buttons = [
    tk.Button(root, text="", width=50, font=("Segoe UI", 10)),
    tk.Button(root, text="", width=50, font=("Segoe UI", 10)),
]
for btn in buttons:
    btn.pack(pady=5)

# --- Start game ---
next_round()

root.mainloop()
