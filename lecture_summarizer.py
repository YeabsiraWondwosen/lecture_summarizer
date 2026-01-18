import re
import nltk
import tkinter as tk
from tkinter import scrolledtext, messagebox
from nltk.corpus import stopwords
from collections import defaultdict

# Download stopwords safely
nltk.download('stopwords', quiet=True)

# ---------------- TOKENIZATION ----------------
def tokenize_words(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def tokenize_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

# ---------------- SUMMARIZATION ----------------
def summarize_long_text(text, ratio):
    stop_words = set(stopwords.words("english"))

    words = tokenize_words(text)
    if len(words) < 50:
        return "Text is too short to summarize."

    freq = defaultdict(int)
    for w in words:
        if w not in stop_words:
            freq[w] += 1

    max_freq = max(freq.values())
    for w in freq:
        freq[w] /= max_freq  # normalize

    sentences = tokenize_sentences(text)
    scores = defaultdict(float)

    for s in sentences:
        wc = len(tokenize_words(s))
        if 5 <= wc <= 40:
            for w in tokenize_words(s):
                if w in freq:
                    scores[s] += freq[w]

    if not scores:
        return "Unable to generate summary."

    summary_len = max(3, int(len(sentences) * ratio))
    summary = sorted(scores, key=scores.get, reverse=True)[:summary_len]

    return " ".join(summary)

# ---------------- BUTTON ACTION ----------------
def generate_summary():
    lecture_text = input_text.get("1.0", tk.END).strip()
    ratio = length_scale.get() / 100

    if not lecture_text:
        messagebox.showwarning("Warning", "Please enter lecture text.")
        return

    summary = summarize_long_text(lecture_text, ratio)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, summary)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Automatic Lecture Summarization System")
root.geometry("900x650")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="Automatic Lecture Summarization System",
    font=("Arial", 18, "bold")
).pack(pady=10)

# Input Label
tk.Label(root, text="Lecture Text (Input):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

# Input Text Area
input_text = scrolledtext.ScrolledText(root, width=105, height=12)
input_text.pack(padx=10, pady=5)

# Summary Length
tk.Label(root, text="Summary Length (%)", font=("Arial", 11)).pack(pady=5)
length_scale = tk.Scale(root, from_=10, to=50, orient=tk.HORIZONTAL)
length_scale.set(25)
length_scale.pack()

# Button
tk.Button(
    root,
    text="Generate Summary",
    font=("Arial", 12, "bold"),
    bg="#2E8B57",
    fg="white",
    command=generate_summary
).pack(pady=10)

# Output Label
tk.Label(root, text="Summary Output:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

# Output Text Area
output_text = scrolledtext.ScrolledText(root, width=105, height=10)
output_text.pack(padx=10, pady=5)

root.mainloop()
