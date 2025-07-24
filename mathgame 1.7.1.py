'''
Math Game
Filename: mathgameexample 1.7.0
Date: 12/06/2025
Version: 1.7.0

Description: This quiz includes both random math questions and graph image questions.
'''

import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


image_questions = [
    {"type": "image", "image": "fig1.png", "question": "What is the y-intercept?", "answer": "3"},
    {"type": "image", "image": "fig2.png", "question": "What is the slope?", "answer": "-2"},
    {"type": "image", "image": "fig3.png", "question": "What is the slope of the line?", "answer": "-4"},
    {"type": "image", "image": "fig4.png", "question": "What is the y-intercept?", "answer": "4"}
]

def generate_math_question():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    return {
        "type": "math",
        "question": f"What is {num1} + {num2}?",
        "answer": str(num1 + num2)
    }

def build_question_pool():
    math_questions = [generate_math_question() for _ in range(4)]
    combined = image_questions + math_questions
    random.shuffle(combined)
    return combined

class MixedMathQuiz:
    def __init__(self, parent_window):
        self.score = 0
        self.question_number = 0
        self.questions = build_question_pool()

        self.window = tk.Toplevel(parent_window)
        self.window.title("Mixed Math Quiz")
        self.window.geometry("650x550")
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
        if self.question_number < len(self.questions):
            current = self.questions[self.question_number]
            self.entry.delete(0, tk.END)

            # Show question text
            self.question_label.config(text=f"Q{self.question_number + 1}: {current['question']}")

            # Handle image display
            if current["type"] == "image":
                try:
                    img = Image.open(current["image"])
                    img = img.resize((400, 300), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.image_label.config(image=photo, text="")
                    self.image_label.image = photo
                except FileNotFoundError:
                    self.image_label.config(text="Image not found", image='', compound='center')
            else:
                self.image_label.config(image='', text="")

        else:
            messagebox.showinfo("Quiz Complete", f"Final Score: {self.score}/{len(self.questions)}")
            self.window.destroy()

    def submit_answer(self):
        user_input = self.entry.get().strip()
        if not self.input_validator(user_input):
            return

        correct_answer = self.questions[self.question_number]["answer"]
        if user_input == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Good job!")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer was: {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")
        self.question_number += 1
        self.show_question()


root = tk.Tk()
root.title("Math For Kids")
root.geometry("300x200")
root.resizable(False, False)

def launch_quiz():
    root.withdraw()
    MixedMathQuiz(root)

start_img = tk.PhotoImage(file="start.png")
start_img = start_img.subsample(10)

start_button = tk.Button(root, image=start_img, command=launch_quiz)
start_button.place(relx=0.3, rely=0.25, relwidth=0.4, relheight=0.25)
start_button.image = start_img

root.mainloop()
