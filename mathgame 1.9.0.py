'''Math Game
Filename: mathgameexample 1.9.0
Date: 19/06/2025
Version: 1.9.0

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
    def __init__(self, main_window, player_name):
        self.player_name = player_name
        self.score = 0
        self.question_number = 0
        self.questions = build_question_pool()

        self.window = tk.Toplevel(main_window)
        self.window.title("Question Page")
        self.window.geometry("650x550")
        self.window.resizable(False, False)

        self.question_background_img = Image.open("question_bg.png") 
        self.question_bg = ImageTk.PhotoImage(self.question_background_img)
        self.question_bg_label = tk.Label(self.window, image=self.question_bg)
        self.question_bg_label.place(x=0, y=0, relwidth=1, relheight=1) 

        self.question_label = tk.Label(self.window, text="", font=("Courier", 16))
        self.question_label.pack(pady=(20,10))

        self.image_label = tk.Label(self.window)
        self.image_label.pack(pady=10)

        self.entry = tk.Entry(self.window, font=("Courier", 14))
        self.entry.pack(pady=10)

        self.submit_img = tk.PhotoImage(file="submit.png")
        self.submit_img = self.submit_img.subsample(10)
        self.submit_button = tk.Button(self.window, image=self.submit_img, command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.score_label = tk.Label(self.window, text="Score: 0", font=("Courier", 12))
        self.score_label.pack(pady=10)

        self.show_question()
        self.window.lift()
        self.window.focus_force() 

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

            self.question_label.config(text=f"Q{self.question_number + 1}: {current['question']}")

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
            self.save_score()
            self.window.destroy()

    def save_score(self):
        try:
            with open("leaderboard.txt", "a") as file:
                file.write(f"{self.player_name}: {self.score}/{len(self.questions)}\n")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save score: {e}")

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
root.title("Maths Game")
root.geometry("844x648")
root.resizable(False, False)

background_img = Image.open("background.png") 
bg = ImageTk.PhotoImage(background_img)
bg_label = tk.Label(root, image=bg)
bg_label.pack()


def launch_quiz():
    root.withdraw()
    MixedMathQuiz(root)
def start_game():
    player_name = name_entry.get().strip()
    if not player_name:
        messagebox.showwarning("Input Error", "Please enter your name!")
        return
    root.withdraw()
    MixedMathQuiz(root, player_name)

name_label = tk.Label(root, text="Enter Your Name:", font=("Courier", 14), bg="white")
name_label.place(relx=0.35, rely=0.45)

name_entry = tk.Entry(root, font=("Courier", 14))
name_entry.place(relx=0.35, rely=0.50, relwidth=0.28)

start_img = tk.PhotoImage(file="start.png")
start_img = start_img.subsample(5)

start_button = tk.Button(root, image=start_img, command=start_game)
start_button.place(relx=0.35, rely=0.55, relwidth=0.28, relheight=0.21)
start_button.image = start_img

def view_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            scores = file.read()
    except FileNotFoundError:
        scores = "No scores yet."

    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("400x500")

    leaderboard_img = Image.open("scoreboard_bg.png") 
    leaderboard_bg = ImageTk.PhotoImage(leaderboard_img)
    leaderboard_bg_label = tk.Label(leaderboard_window, image=leaderboard_bg)
    leaderboard_bg_label.image = leaderboard_bg 
    leaderboard_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    scores_text = tk.Text(leaderboard_window, font=("Courier", 12), bg="white", borderwidth=0)
    scores_text.insert(tk.END, scores)
    scores_text.config(state="disabled")
    scores_text.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.75)

leaderboard_button = tk.Button(root, text="View Leaderboard", font=("Courier", 12), command=view_leaderboard)
leaderboard_button.place(relx=0.35, rely=0.80, relwidth=0.28)


root.mainloop()
