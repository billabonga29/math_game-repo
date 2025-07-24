'''
Math Game
Filename: mathgame 1.6.0
Date: 12/06/2025
Version: 1.6.0

Description: The purpose of this program is to create a simple math quiz with images.
'''

import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Quiz questions with images and answers
quiz_questions = [
    {"image": "fig1.png", "question": "What is the y-intercept?", "answer": "3"},
    {"image": "fig2.png", "question": "What is the slope?", "answer": "-2"},
    {"image": "fig3.png", "question": "What is the slope of the line?", "answer": "-4"},
    {"image": "fig4.png", "question": "What is the y-intercept?", "answer": "4"}
]

class ImageMathQuiz:
    def __init__(self, parent_window):
        self.score = 0
        self.question_number = 0

        self.window = tk.Toplevel(parent_window)
        self.window.title("Math Image Quiz")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        self.question_label = tk.Label(self.window, text="", font=("Courier", 16))
        self.question_label.pack(pady=10)

        self.image_label = tk.Label(self.window)
        self.image_label.pack(pady=10)

        self.entry = tk.Entry(self.window, font=("Courier", 14))
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Courier", 12))
        self.score_label.pack(pady=10)

        self.show_question()

    def input_validator(self, user_input):
        if user_input == "":
            self.create_error_window("NO BLANKS!")
            return False
        elif not (user_input.replace('-', '', 1).isdigit()):
            if any(c.isalpha() for c in user_input):
                self.create_error_window("NO LETTERS!")
            elif " " in user_input:
                self.create_error_window("NO WHITESPACE!")
            else:
                self.create_error_window("NO SYMBOLS!")
            return False
        elif len(user_input) > 6:
            self.create_error_window("CHARACTER LIMIT IS 6!")
            return False
        else:
            return True

    def create_error_window(self, error_message):
        error_win = tk.Toplevel(self.window)
        error_win.title("Error")
        error_win.geometry("300x150")
        error_label = tk.Label(error_win, text=error_message, fg="red", font=("Courier", 14))
        error_label.pack(pady=30)

    def show_question(self):
        if self.question_number < len(quiz_questions):
            current = quiz_questions[self.question_number]
            self.question_label.config(text=f"Q{self.question_number + 1}: {current['question']}")
            try:
                image = Image.open(current["image"])
                image = image.resize((400, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            except FileNotFoundError:
                self.image_label.config(text="Image not found", image='', compound='center')
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Quiz Complete", f"Your final score is {self.score}/{len(quiz_questions)}")
            self.window.destroy()

    def submit_answer(self):
        user_input = self.entry.get().strip()
        if not self.input_validator(user_input):
            return

        correct_answer = quiz_questions[self.question_number]["answer"]
        if user_input == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Good job!")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer was: {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")
        self.question_number += 1
        self.show_question()

# Main app window
root = tk.Tk()
root.title("Math For Kids")
root.geometry("300x200")
root.resizable(False, False)

def start_quiz():
    ImageMathQuiz(root)

start_img = tk.PhotoImage(file="start.png")
start_img = start_img.subsample(10)

start_button = tk.Button(root, image=start_img, command=start_quiz)
start_button.place(relx=0.3, rely=0.25, relwidth=0.4, relheight=0.25)
start_button.image = start_img

root.mainloop()
