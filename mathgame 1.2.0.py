'''Math Game
Filename: mathgameexample 1.1.0
Date 14/05/2025
Version: 1.1.0
- Validity Checking
    - Special Characteres
    - Blanks
    - Boundaries
    - Alphabet
Description: The purpose of this program is to create a simple math quiz.
'''

import random
from tkinter import *

num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
def input_validator(user_input):
    # Blanks
    if user_input == "":
        create_error_window()
        warning = Label(app, text="NO BLANKS!", fg="RED", font=("Courier", 16))
        warning.place(relx=0.25, rely=0.16)
    # Alphabet, Whitespace and Symbols
    elif user_input.isdigit() == False:
        if user_input.isalnum() == True:
            warning = Label(app, text="NO LETTERS!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
        elif " " in user_input:
            warning = Label(app, text="NO WHITESPACE!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
        else:
            warning = Label(app, text="NO SYMBOLS!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
    # Boundaries (user input is more than)
    elif len(user_input) > 6:
        warning = Label(app, text="CHARACTER LIMIT IS 6", fg="RED", font=("Courier", 16))
        warning.place(relx=0.25, rely=0.16)
    else:
        return True
    return False

def submt(user_entry):
    user_input = user_entry.get()

    validity = input_validator(user_input)
    if validity == True:
        if user_input == str(resultPLUS()):
            correct = Label(app, text="Correct!", fg="green", font=("Courier", 16))
            correct.place(relx=0.3, rely=0.2)
        else:
            wrong = Label(app, text="Wrong!!!", fg="red", font=("Courier", 16))
            wrong.place(relx=0.3, rely=0.2)
    print("Checks Done!")
    
def try_again():
    try_again.num1update = random.choice(num)
    try_again.num2update = random.choice(num)
    newQ = Label(
        app, text=f"{try_again.num1update}+{try_again.num2update}", font=("Courier", 16)
    )
    newQ.place(relx=0.16, rely=0.1, relwidth=0.7, relheight=0.23)


def resultPLUS():
    try_again
    return try_again.num1update + try_again.num2update


app = Tk()
app.title("Math For Kids")
# canvas = Canvas(app, width=240, height=300)
# canvas.pack()
app.geometry("300x400")
app.resizable(True, True)

# Start Button
start = Button(app, text="Begin Adventure", font= ("Times New Roman","10"), bg="blue", fg="white", command=try_again)
start.place(relx=0.30, rely=0.1, relheight= 0.1, relwidth = 0.4)

# Entry textbox
solving = Entry(app, font = ("Comic Sans MS", 12))
solving.place(relx=0.30, rely=0.3, relwidth=0.40, relheight=0.23)

# Submit Button
submit = Button(app, text="Submit", command=lambda: submt(solving))
submit.place(relx=0.32, rely=0.64, relwidth=0.34, relheight=0.15)

# Try Again
try_again = Button(app, text="Try Again", command=try_again)
try_again.place(relx=0.39, rely=0.85)
app.mainloop()
