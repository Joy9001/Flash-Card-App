from tkinter import *
from tkinter import messagebox
import pandas
import random

# Constants
GREEN = "#B1DDC6"
GREEN2 = "#91c2af"
WHITE = "#FFFFFF"
TIMER = 3

# Data Handling
try:
    data = pandas.read_csv("data/word_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
data_dict = data.to_dict(orient="records")
current_word = random.choice(data_dict)


# Button Functions
def timer():
    global TIMER, TIMER_ID
    if TIMER == 0:
        timer_label.config(text=str(TIMER))
        TIMER = 3
    else:
        timer_label.config(text=str(TIMER))
        TIMER -= 1
        TIMER_ID = window.after(1000, timer)


def flipping():
    global current_word
    english_word = current_word["English"]
    canvas.itemconfig(flash_card_image, image=back_card_image)
    lang.config(text="English", fg=WHITE, bg=GREEN2)
    word.config(text=english_word, fg=WHITE, bg=GREEN2)


def dont_know_this():
    global FLIP_TIMER, TIMER_ID, TIMER, current_word, data_dict
    window.after_cancel(FLIP_TIMER)
    window.after_cancel(TIMER_ID)

    if len(data_dict) != 0:
        TIMER = 3
        current_word = random.choice(data_dict)
        canvas.itemconfig(flash_card_image, image=front_card_image)
        lang.config(text="French", bg=WHITE, fg=GREEN2)
        word.config(text=current_word["French"], bg=WHITE, fg=GREEN2)

        timer_label.config(text=TIMER)
        timer()

        FLIP_TIMER = window.after(3000, flipping)
    else:
        lang.config(text="")
        word.config(text="")
        timer_label.config(text="0")
        messagebox.showinfo(title="All Done",
                            message="You have learnt all the french words. Congratulation!\nYou can exit now.")


def know_this():
    global data_dict, current_word
    dont_know_this()
    try:
        data_dict.remove(current_word)
    except ValueError:
        pass
    new_df = pandas.DataFrame(data_dict, columns=["French", "English"])
    new_df.to_csv("data/words_to_learn.csv")


# UI Interface
window = Tk()
window.config(padx=50, pady=50, bg=GREEN)
window.title("FLASHY")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=GREEN)
back_card_image = PhotoImage(file="images/card_back.png")
front_card_image = PhotoImage(file="images/card_front.png")
# canvas.create_image(400, 263, image=back_card_image)
flash_card_image = canvas.create_image(400, 263, image=front_card_image)
canvas.grid(row=0, column=0, columnspan=2)

# Labels
lang = Label(text="French", font=("Ariel", 40, "italic"), bg=WHITE)
lang.place(x=310, y=150)

word = Label(text=current_word["French"], font=("Ariel", 60, "bold"), bg=WHITE)
word.place(x=canvas.winfo_reqwidth() // 2, y=(canvas.winfo_reqheight() // 2) + 50, anchor="center")

FLIP_TIMER = window.after(3000, func=flipping)
# TIMER
timer_label = Label(text=TIMER, font=("Ariel", 60, "bold"), bg=GREEN, fg=WHITE)
timer_label.place(x=370, y=530)

TIMER_ID = window.after(0, func=timer)
# BUTTONS
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, bg=GREEN, highlightthickness=0, bd=0, command=know_this)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, bg=GREEN, highlightthickness=0, bd=0, command=dont_know_this)
wrong_button.grid(row=1, column=0)

window.mainloop()
