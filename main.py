import tkinter as tk
import random

background = "#016B61"

#opening words file

with open("words.txt","r") as file:
    contents = file.read()
    words = contents.split()

#grab unique random words (no repeats).

random_words = random.sample(words,15)
display_words = " ".join(random_words) #join those words

# set up the screen

window = tk.Tk()
window.title("Typing Test")
window.config(padx=50,pady=50,bg=background)
canvas = tk.Canvas(width=500,height=500)   #set up the canvas
canvas.pack()

#functions
def on_focus_in(event):  #when user clicks entry box delete placeholder
    if entry_box.get() == "type the words here":
        entry_box.delete(0,tk.END)
        entry_box.config(fg="black")

def on_focus_out(event): #when user clicks out of entry box showcase the placeholder again
    if entry_box.get() == "":
        entry_box.insert(0,"type the words here")
        entry_box.config(fg="grey",justify="center")

#heading

canvas.create_text(250,40,text="TYPING SPEED TEST",font=("Times New Roman",30,"bold"),fill="#70B2B2")

#widgets

text_label = tk.Label(text="How fast are your fingers? Do the one-minute typing test to find out!"
                           " Press the space bar after each word. At the end, you'll get your typing speed in CPM and WPM."
                           ,
                      font=("Times New Roman",10),fg="black",wraplength=450,justify="center")
text_label_window = canvas.create_window(250,100,window=text_label)

words_label = tk.Label(text=f"{display_words}",font=("Times New Roman",20),fg="black",wraplength=450,bg="#E5E9C5")
words_label_window = canvas.create_window(250,220,window=words_label)

entry_box = tk.Entry(width=50)
entry_box.insert(0,"type the words here")
entry_box.config(fg="grey",justify="center")

entry_box.bind("<FocusIn>", on_focus_in)
entry_box.bind("<FocusOut>", on_focus_out)

entry_box_window = canvas.create_window(250,300,window=entry_box)










window.mainloop()