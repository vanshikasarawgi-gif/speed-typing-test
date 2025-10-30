import tkinter as tk
import random
import time

# ----- CONFIG -----
BACKGROUND = "#016B61"
sec = 60
timer_started = False
typed_index = 0
correct_words = 0
typed_words = []
start_time = None
word_items = []  # store canvas text items for coloring


# ----- LOAD WORDS -----
with open("words.txt", "r") as file:
    words = file.read().split()


# ----- FUNCTIONS -----
def update_display_words():
    """Generate and show new random words with proper wrapping."""
    global displayed_words, typed_index, word_items
    canvas_words.delete("word")  # clear previous batch
    displayed_words = random.sample(words, 15)
    typed_index = 0
    word_items = []

    # Canvas width — keep some padding
    canvas_width = 440
    x, y = 20, 30
    spacing = 10  # space between words

    for word in displayed_words:
        # Measure word width dynamically using font metrics
        temp = canvas_words.create_text(0, 0, text=word, font=("Times New Roman", 18))
        bbox = canvas_words.bbox(temp)
        word_width = bbox[2] - bbox[0] if bbox else 0
        canvas_words.delete(temp)

        # Wrap to next line if this word would overflow
        if x + word_width > canvas_width:
            x = 20
            y += 40  # move to next line

        text_item = canvas_words.create_text(
            x, y,
            text=word,
            font=("Times New Roman", 18),
            fill="black",
            anchor="w",
            tags="word"
        )
        word_items.append(text_item)
        x += word_width + spacing

    entry_box.delete(0, tk.END)

def count_time():
    """Countdown timer."""
    global sec
    if sec > 0:
        sec -= 1
        time_label.config(text=f"Time left: {sec}")
        window.after(1000, count_time)
    else:
        show_results()


def show_results():
    """Display typing speed and accuracy."""
    global correct_words, typed_words, start_time
    elapsed = time.time() - start_time if start_time else 60
    total_typed = len(typed_words)
    wpm = (total_typed / elapsed) * 60 if elapsed > 0 else 0
    accuracy = (correct_words / total_typed * 100) if total_typed > 0 else 0

    canvas_words.delete("word")
    canvas_words.create_text(
        250, 100,
        text=f"Time’s up!\nWPM: {wpm:.1f}\nAccuracy: {accuracy:.1f}%",
        font=("Times New Roman", 20, "bold"),
        fill="black"
    )
    entry_box.config(state="disabled")


def on_focus_in(event):
    """Start timer when user focuses for the first time."""
    global timer_started, start_time
    if entry_box.get() == "type the words here":
        entry_box.delete(0, tk.END)
        entry_box.config(fg="black")
    if not timer_started:
        timer_started = True
        start_time = time.time()
        count_time()


def on_focus_out(event):
    """Restore placeholder text when entry is empty."""
    if entry_box.get() == "":
        entry_box.insert(0, "type the words here")
        entry_box.config(fg="grey", justify="center")


def get_typed_words():
    """Handle each space press (one word at a time) and color it."""
    global typed_index, typed_words, correct_words

    typed_text = entry_box.get().strip()
    entry_box.delete(0, tk.END)

    if not typed_text:
        return  # ignore accidental space

    typed_words.append(typed_text)

    # check correctness + color word
    if typed_index < len(displayed_words):
        shown_word = displayed_words[typed_index]
        if typed_text == shown_word:
            correct_words += 1
            canvas_words.itemconfig(word_items[typed_index], fill="green")
        else:
            canvas_words.itemconfig(word_items[typed_index], fill="red")
        typed_index += 1

    # if finished current batch
    if typed_index >= len(displayed_words):
        window.after(500, update_display_words)  # slight pause before refreshing

def reset_test():
    global sec, timer_started, typed_index, correct_words, typed_words, start_time

    # Reset all variables
    sec = 60
    timer_started = False
    typed_index = 0
    correct_words = 0
    typed_words = []
    start_time = None

    # Reset UI
    time_label.config(text=f"Time left: {sec}")
    entry_box.config(state="normal", fg="grey", justify="center")
    entry_box.delete(0, tk.END)
    entry_box.insert(0, "type the words here")
    canvas_words.delete("word")

    # Show new words
    update_display_words()


# ----- GUI -----
window = tk.Tk()
window.title("Typing Test")
window.config(padx=50, pady=50, bg=BACKGROUND)

canvas = tk.Canvas(window, width=500, height=500, highlightthickness=0)
canvas.pack()

canvas.create_text(250, 40, text="TYPING SPEED TEST",
                   font=("Times New Roman", 30, "bold"),
                   fill="#70B2B2")

text_label = tk.Label(
    text=("How fast are your fingers? Do the one-minute typing test to find out! "
          "Press the space bar after each word. Correct words turn green, wrong turn red!"),
    font=("Times New Roman", 10),
    fg="black",
    wraplength=500,
    justify="center",
)
canvas.create_window(250, 100, window=text_label)

# canvas for displaying colorable words
canvas_words = tk.Canvas(window, width=460, height=160, bg="#E5E9C5", highlightthickness=0)
canvas.create_window(250, 230, window=canvas_words)

entry_box = tk.Entry(width=50)
entry_box.insert(0, "type the words here")
entry_box.config(fg="grey", justify="center")
entry_box.bind("<FocusIn>", on_focus_in)
entry_box.bind("<FocusOut>", on_focus_out)
entry_box.bind("<space>", lambda event: get_typed_words())
canvas.create_window(250, 350, window=entry_box)

update_display_words()

time_label = tk.Label(
    text=f"Time left: {sec}",
    font=("Times New Roman", 10),
    fg="black",
)
canvas.create_window(350, 140, window=time_label)

reset_btn = tk.Button(text="Reset",command=reset_test,highlightthickness=0)
canvas.create_window(250,400,window=reset_btn)

window.mainloop()
