'''Math Game
Filename: mathgamee 1.5.1
Date 14/05/2025
Version: 1.4.1
- 
Description: The purpose of this program is to create a simple math quiz.
'''

import random
from tkinter import *
from tkinter import PhotoImage

num = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def create_error_window(error_message):
    error_window = Toplevel(app)
    error_window.title("Error Window")
    error_window.geometry("300x200")
    error_window.resizable(False, False)
    error_window_warning = Label(error_window, text = error_message, fg="RED",font=("Courier", 16))

    error_window_warning.config(text=error_message)
    error_window_warning.place(relx=0.3, rely=0.1)

    
def input_validator(user_input):
    # Blanks
    if user_input == "":
        create_error_window("NO BLANKS!")
                            
        warning = Label(app, text="NO BLANKS!", fg="RED", font=("Courier", 16))
        warning.place(relx=0.25, rely=0.16)
    # Alphabet, Whitespace and Symbols
    elif user_input.isdigit() == False:
        if user_input.isalnum() == True:
            create_error_window("NO LETTERS!")
            warning = Label(app, text="NO LETTERS!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
        elif " " in user_input:
            create_error_window("NO WHITESPACE!")
            warning = Label(app, text="NO WHITESPACE!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
        else:
            create_error_window("NO SYMBOLS!")
            warning = Label(app, text="NO SYMBOLS!", fg="RED", font=("Courier", 16))
            warning.place(relx=0.25, rely=0.16)
    # Boundaries (user input is more than)
    elif len(user_input) > 6:
        create_error_window("CHARACTER LIMIT IS 6!")
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
app.geometry("300x400")
app.resizable(True, True)

start_img = PhotoImage(file="start.png") 
start_img = start_img.subsample(10) 
# Start Button
start = Button(app, image = start_img, font= ("Times New Roman","10"), command=try_again)
start.place(relx=0.30, rely=0.1, relheight= 0.17, relwidth = 0.4)
start.image = start_img  

# Entry textbox
solving = Entry(app, font = ("Comic Sans MS", 12))
solving.place(relx=0.30, rely=0.3, relwidth=0.40, relheight=0.23)

# Submit Button
submit_img = PhotoImage(file="submit.png") 
submit_img = submit_img.subsample(10) 
submit = Button(app, image=submit_img, command=lambda: submt(solving))
submit.place(relx=0.32, rely=0.64, relwidth=0.34, relheight=0.14)
start.image = submit_img  

# Try Again
try_again = Button(app, text="Try Again", command=try_again)
try_again.place(relx=0.39, rely=0.85)
app.mainloop()
