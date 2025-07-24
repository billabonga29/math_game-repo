'''Maths Racing Game
Author: Bill Xie
Date: 24/07/2025
Purpose: The purpose of this program is to create a fun interactive math game to help students better develop and reinforce their math skills.
'''
import pygame
import tkinter as tk
from tkinter import messagebox
import random
import time
import os
from PIL import Image, ImageTk

# Initialize Pygame
pygame.init()

# Game Constants 
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Racing Game")

# Game Settings
QUESTIONS_TO_WIN = 10
MOVE_DISTANCE = WIDTH // QUESTIONS_TO_WIN
FPS = 60

# Car Settings (Loads and resizes the images)
# Car Size
CAR_WIDTH, CAR_HEIGHT = 120, 90
# Players Car
PLAYER_CAR = pygame.image.load("Images/car_player.png")
PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (CAR_WIDTH, CAR_HEIGHT))
# AI Car
AI_CAR = pygame.image.load("Images/car_ai.png")
AI_CAR = pygame.transform.scale(AI_CAR, (CAR_WIDTH, CAR_HEIGHT))

# Loads Track Image
TRACK_IMG = pygame.image.load("Images/track_2.png")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts 
pygame.font.init()
FONT = pygame.font.SysFont("Calibri", 18)
INPUT_FONT = pygame.font.SysFont("Calibri", 16)

# Input box 
input_box = pygame.Rect(50, HEIGHT - 70, 200, 35)
input_text = ""
active = False

# Generates a random addition question for easy difficulty.
def generate_addition_question():
    # Generates random numbers
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    # Returns the question and answer
    return {"question": f"What is {num1} + {num2}?",
            "answer": str(num1 + num2),
            "params": None}

# Generates random area questions for medium difficulty.
def generate_area_question():
    # Picks a random shape out of the options.
    shape = random.choice(["square", "rectangle", "triangle", "circle"])
    #Square
    if shape == "square":
        # Generates random lengths for the sides of the shape.
        side = random.randint(2, 10)
        question = f"What is the area of a square with side {side}?"
        # Calculates the area (side x side)
        answer = side * side
        # Saves shape data to be used for drawing.
        shape_data = ("square", (side,))

    # Rectangle
    elif shape == "rectangle":
        # Generates random length and width values.
        l = random.randint(3, 12)
        w = random.randint(2, 10)
        question = f"What is the area of a rectangle with length {l} and width {w}?"
        # Calculates Area (length × width)
        answer = l * w
        # Saves data of shape for drawing.
        shape_data = ("rectangle", (l, w))

    # Triangle
    elif shape == "triangle":
        # Generates random base and height values.
        base = random.randint(4, 10)
        height_val = random.randint(3, 8)
        question = f"What is the area of a triangle with base {base} and height {height_val}?"
        # Calculates Area (0.5 × base × height)
        answer = 0.5 * base * height_val
        # Saves shape data to be used for drawing.
        shape_data = ("triangle", (base, height_val))

    # Circle
    elif shape == "circle":
        # Generates random radius length.
        radius = random.randint(2, 8)
        question = f"What is the area of a circle with radius {radius}? (π ≈ 3.14)"
        # Calculates area (πr²)
        answer = round(3.14 * radius * radius, 2)
        # Saves shape data for drawing.
        shape_data = ("circle", (radius,))

    # Returns final question string, answer (rounded) and the data of the shape.
    return {
        "question": question,
        "answer": round(answer, 2),
        "shape_data": shape_data
        }

# This function generates calculus question used for the hard difficulty.
def generate_calculus_question():
    # Picks between differentiation and integration question types.
    qtype = random.choice(["derivative_poly", "integral_poly"])

    # Differentiation (in form f(x) = ax^n)
    if qtype == "derivative_poly":
        # Generates random coefficent and exponents.
        a = random.randint(1, 5)
        n = random.randint(1, 5)
        question = f"What is the derivative of {a}x^{n}?"
        
        # Calculates new coefficent and exponent.
        new_coeff = a * n
        new_power = n - 1

        # Formats answer based on the power.
        if new_power == 1:
            answer = f"{new_coeff}x"
        elif new_power == 0:
            answer = f"{new_coeff}"
        else:
            answer = f"{new_coeff}x^{new_power}"

        # Returns the question and answer.
        return question, answer

    # Integration (in form: ∫ ax^n dx)
    elif qtype == "integral_poly":
        # Generates random coefficent and power values.
        a = random.randint(1, 5)
        n = random.randint(0, 4)
        # Calculates new power.
        new_power = n + 1

        # Formats fraction if necessary.
        if a % new_power == 0:
            coeff = a // new_power
            coeff_str = f"{coeff}"
        else:
            coeff_str = f"{a}/{new_power}"
        # Formats answer string.
        if new_power == 1:
            answer = f"{coeff_str}x + C"
        else:
            answer = f"{coeff_str}x^{new_power} + C"
        question = f"What is the integral of {a}x^{n}?"
        # Returns question and answer.
        return question, answer

    return "No question", "N/A"

# Picks a generator for the difficulty chosen for the math game.
def get_random_question(difficulty):
    # Calls easy question generator.
    if difficulty == "Easy":
        return generate_addition_question()
    # Calls medium question generator.
    elif difficulty == "Medium":
        return generate_area_question()
    # Calls hard question generator.
    elif difficulty == "Hard":
        return generate_calculus_question()

# Builds a question pool
def build_question_pool(difficulty):
    questions = []
    if difficulty == "Medium":
        questions = [generate_area_question() for _ in range(QUESTIONS_TO_WIN * 2)]
    elif difficulty == "Hard":
        # Converts tuple into dictionary to prevent error.
        questions = [{"question": q, "answer": a} for q, a in [generate_calculus_question() for _ in range(QUESTIONS_TO_WIN * 2)]]
    else:
        questions = [generate_addition_question() for _ in range(QUESTIONS_TO_WIN * 2)]
    # Shuffles the order of the questions.
    random.shuffle(questions)
    return questions

# Saves the scores to a text file.
def save_to_leaderboard(name, time_taken):
    # Opens text file and adds data into it.
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name}: {time_taken:.2f} seconds\n")

# This function runs the game.
def run_game(player_name, difficulty):
    # Creates window.
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Math Race Challenge")

    # Creates clock for the game.
    clock = pygame.time.Clock()
    
    # Constants
    feedback_message = ""
    feedback_color = BLACK
    feedback_timer = 0

    # Sets starting positions and score of player and AI.
    player_x = 0
    ai_x = 0
    player_score = 0

    # Calls questions from the question pool.
    questions = build_question_pool(difficulty)

    # Sets speed of AI based on the difficulty selected.
    ai_speed = {"Easy": 40, "Medium": 25, "Hard": 15}[difficulty]  

    # Picks question to be displayed and removes it from the list so it's not reused.
    current_question = questions.pop()

    # Makes textbox empty to start.
    input_text = ""

    # Waits for player to press start before the game begins.
    waiting = True
    while waiting:
        screen.fill(WHITE)
        screen.blit(TRACK_IMG, (0, 0))
        # Gives user message for startin the game.
        title = FONT.render("Press SPACE to Start the Race!", True, BLACK, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))

        # Instructions for user.
        instruction = FONT.render(f"Solve {QUESTIONS_TO_WIN} questions to win!", True, BLACK, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 40))

        # Begins game if user presses space button.
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


    # Starts Stopwatch.
    start_time = time.time()

    running = True
    while running:
        # Limit game to fixed frame rate.
        dt = clock.tick(FPS) / 1000
        # Draws Race Track.
        screen.blit(TRACK_IMG, (0, 0))

        # Moves AI
        ai_x += ai_speed * dt

        # Draws finish line
        pygame.draw.line(screen, BLACK, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 5)

        # Makes the players car drive to its next position in a mini animation.
        target_x = (player_score * MOVE_DISTANCE)
        if player_x < target_x:
            player_x += min(5, target_x - player_x)
    
        # Draws cars
        screen.blit(PLAYER_CAR, (player_x, HEIGHT // 5))
        screen.blit(AI_CAR, (ai_x, HEIGHT // 2.5))

        # Draws labels
        player_label = FONT.render(f"{player_name} Position: {player_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        ai_label = FONT.render(f"AI Position: {int(ai_x) // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        screen.blit(player_label, (20, 20))
        screen.blit(ai_label, (20, 50))

        # Draws question
        question_surface = FONT.render(current_question['question'], True, BLACK)
        screen.blit(question_surface, (20, HEIGHT - 270))

        # Draws input box background and border
        input_rect = pygame.Rect(20, HEIGHT - 220, 300, 35)
        pygame.draw.rect(screen, WHITE, input_rect)            
        pygame.draw.rect(screen, BLACK, input_rect, 2)         

        input_surface = INPUT_FONT.render(input_text, True, BLACK)
        text_rect = input_surface.get_rect()
        text_pos = (input_rect.x + 10, input_rect.y + (input_rect.height - text_rect.height) // 2)
        screen.blit(input_surface, text_pos)

        # Draws box to hold the shapes.
        box_width, box_height = 230, 180
        box_x = WIDTH - box_width - 60
        box_y = HEIGHT - box_height - 10
        shape_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, WHITE, shape_box_rect)
        pygame.draw.rect(screen, BLACK, shape_box_rect, 3)

        # Draws shapes in shape box for medium difficulty.
        if difficulty == "Medium" and current_question.get("shape_data"):
            shape_type, dimensions = current_question["shape_data"]
            p = {}
            if shape_type == "square":
                p = {"shape": "square", "side": dimensions[0]}
            elif shape_type == "rectangle":
                p = {"shape": "rectangle", "width": dimensions[0], "height": dimensions[1]}
            elif shape_type == "triangle":
                p = {"shape": "triangle", "base": dimensions[0], "height": dimensions[1]}
            elif shape_type == "circle":
                p = {"shape": "circle", "radius": dimensions[0]}

            # Picks x and y values for shape centre to fit in box.
            shape_center_x = box_x + box_width // 2
            shape_center_y = box_y + box_height // 2 + 5  

            # Maxiumum size for shapes inside box
            max_shape_size = 100

            # Draws square.
            if p["shape"] == "square":
                side_pixels = max_shape_size
                top_left = (shape_center_x - side_pixels // 2, shape_center_y - side_pixels // 2)
                pygame.draw.rect(screen, BLACK, (*top_left, side_pixels, side_pixels), 2)
                label = FONT.render(f"{p['side']} cm", True, BLACK)
                screen.blit(label, (top_left[0] + side_pixels // 2 - label.get_width() // 2, top_left[1] + side_pixels + 5))

            # Draws rectangle
            elif p["shape"] == "rectangle":
                # This maintains the ratio for width and height but keeps it within the maximum shape size.
                w_ratio = p["width"]
                h_ratio = p["height"]
                max_dim = max(w_ratio, h_ratio)
                width_px = int((w_ratio / max_dim) * max_shape_size)
                height_px = int((h_ratio / max_dim) * max_shape_size)
                top_left = (shape_center_x - width_px // 2, shape_center_y - height_px // 2)
                pygame.draw.rect(screen, BLACK, (*top_left, width_px, height_px), 2)
                screen.blit(FONT.render(f"{p['width']} cm", True, BLACK), (top_left[0] + width_px // 2 - 20, top_left[1] + height_px + 5))
                screen.blit(FONT.render(f"{p['height']} cm", True, BLACK), (top_left[0] - 45, top_left[1] + height_px // 2 - 10))

            # Draws Triangle
            elif p["shape"] == "triangle":
                b_ratio = p["base"]
                h_ratio = p["height"]
                max_dim = max(b_ratio, h_ratio)
                base_px = int((b_ratio / max_dim) * max_shape_size)
                height_px = int((h_ratio / max_dim) * max_shape_size)
                x1, y1 = shape_center_x - base_px // 2, shape_center_y + height_px // 2
                x2, y2 = shape_center_x + base_px // 2, shape_center_y + height_px // 2
                x3, y3 = shape_center_x, shape_center_y - height_px // 2
                pygame.draw.polygon(screen, BLACK, [(x1, y1), (x2, y2), (x3, y3)], 2)
                screen.blit(FONT.render(f"{p['base']} cm", True, BLACK), ((x1 + x2) // 2 - 20, y1 + 5))
                screen.blit(FONT.render(f"{p['height']} cm", True, BLACK), (x2 + 10, (y3 + y1) // 2 - 10))

            # Draws Circle
            elif p["shape"] == "circle":
                max_cm = 15  
                # Scales radius proportionally to fit within max shape size but big enough to be visible. 
                radius_px = max(20, int((p["radius"] / max_cm) * max_shape_size))
                center = (shape_center_x, shape_center_y)
                pygame.draw.circle(screen, BLACK, center, radius_px, 2)
                # Draws radius line
                pygame.draw.line(screen, BLACK, center, (center[0] + radius_px, center[1]), 2)
                screen.blit(FONT.render(f"{p['radius']} cm", True, BLACK), (center[0] + radius_px + 5, center[1] - 15))

        # Shows feedback message if it's active
        if feedback_message and time.time() < feedback_timer:
            msg_surface = FONT.render(feedback_message, True, feedback_color)
            screen.blit(msg_surface, (20, HEIGHT - 120))

        pygame.display.flip()

        # Checks win conditions
        if player_x >= WIDTH - CAR_WIDTH:
            total_time = time.time() - start_time
            messagebox.showinfo("You Win!", f"You beat AI in {total_time:.2f} seconds!")
            save_to_leaderboard(player_name, total_time)
            running = False
            break
        elif ai_x >= WIDTH - CAR_WIDTH:
            messagebox.showinfo("You Lose", "The AI won this time. Try again!")
            running = False
            break

        # Handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    user_answer_raw = input_text.strip()
                    correct_answer_raw = current_question['answer']
                    try:
                        user_answer_num = float(user_answer_raw)
                        correct_answer_num = float(correct_answer_raw)
                        # Adds tolerance for decimals.
                        is_correct = abs(user_answer_num - correct_answer_num) < 0.01
                    except:
                        user_answer = user_answer_raw.replace(" ", "").lower()
                        correct_answer = str(correct_answer_raw).replace(" ", "").lower()
                        is_correct = user_answer == correct_answer

                    # Gives correct/incorrect messages.
                    if is_correct:
                        player_score += 1
                        feedback_message = "Correct!"
                        feedback_color = (0, 0, 0) 
                    else:
                        feedback_message = "Incorrect!"
                        feedback_color = (0, 0, 0)

                    feedback_timer = time.time() + 1.5  

                    # Checks if player has reached the winning score.
                    if player_score >= QUESTIONS_TO_WIN:
                        total_time = time.time() - start_time
                        messagebox.showinfo("You Win!", f"You beat the AI in {total_time:.2f} seconds!")
                        save_to_leaderboard(player_name, total_time)
                        running = False
                        break

                    # Gets next question and replenishes question pool if empty.
                    if not questions:
                        questions = build_question_pool(difficulty)

                    current_question = questions.pop()
                    input_text = ""
                else:
                    if event.unicode.isprintable() and len(input_text) < 10:
                        # Sets characters allowed to be entered.
                        allowed_chars = "0123456789.+-*/xXcC^ "  
                        if event.unicode in allowed_chars and len(input_text) < 10:
                            input_text += event.unicode


# Button to display the leaderboard.
def show_leaderboard():
    if not os.path.exists("leaderboard.txt"):
        messagebox.showinfo("Leaderboard", "No leaderboard data found.")
        return

    with open("leaderboard.txt", "r") as file:
        data = file.read()

    # Creates window
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("350x400")

    # Adds Labels
    tk.Label(leaderboard_window, text="🏁 Leaderboard 🏁", font=("Calibri", 16, "bold")).pack(pady=10)

    # Adds textbox to display entries for leaderboard.
    text_box = tk.Text(leaderboard_window, font=("Calibri", 12), wrap="none", bg="white", width=40, height=20)
    text_box.insert(tk.END, data)
    text_box.config(state=tk.DISABLED)
    text_box.pack(padx=10, pady=10)

# Starts the game.
def start_game():
    # Retrieves data for name and selected difficulty.
    def on_difficulty_select(selected_difficulty):
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        root.destroy()
        run_game(name, selected_difficulty)

    # Window Settings
    root = tk.Tk()
    root.title("Math Racing Game Setup")
    root.geometry("400x450")

    # Loads and resizes logo image
    if os.path.exists("Images/logo.png"):
        logo_raw = Image.open("Images/logo.png")
        resized_logo = logo_raw.resize((300, 100), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(resized_logo)
        logo_label = tk.Label(root, image=logo_img)
        logo_label.image = logo_img
        logo_label.pack(pady=10)
    else:
        print("logo.png not found.")

    # Name input
    tk.Label(root, text="Enter your name:", font=("Calibri", 14)).pack(pady=10)
    name_entry = tk.Entry(root, font=("Calibri", 14))
    name_entry.pack(pady=10)

    # Difficulty options
    tk.Label(root, text="Select Difficulty:", font=("Calibri", 14)).pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Easy", width=10, font=("Calibri", 12), command=lambda: on_difficulty_select("Easy")).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Medium", width=10, font=("Calibri", 12), command=lambda: on_difficulty_select("Medium")).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Hard", width=10, font=("Calibri", 12), command=lambda: on_difficulty_select("Hard")).grid(row=0, column=2, padx=5)

    # Leaderboard button
    tk.Button(root, text="Leaderboard", font=("Calibri", 12), command=show_leaderboard).pack(pady=10)

    root.mainloop()


start_game()
pygame.quit()
