import pygame
import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# Initialize Pygame
pygame.init()

# Game constants 
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Racing Game")

# Car settings 
CAR_WIDTH, CAR_HEIGHT = 120, 90
PLAYER_CAR = pygame.image.load("car_player.png")
PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (CAR_WIDTH, CAR_HEIGHT))
AI_CAR = pygame.image.load("car_ai.png")
AI_CAR = pygame.transform.scale(AI_CAR, (CAR_WIDTH, CAR_HEIGHT))

TRACK_IMG = pygame.image.load("track.png")

QUESTIONS_TO_WIN = 10
MOVE_DISTANCE = WIDTH // QUESTIONS_TO_WIN
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts 
pygame.font.init()
FONT = pygame.font.SysFont("Courier", 18)
INPUT_FONT = pygame.font.SysFont("Courier", 16)

# Input box 
input_box = pygame.Rect(50, HEIGHT - 70, 200, 35)

input_text = ""
active = False

def generate_addition_question():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    return {"question": f"What is {num1} + {num2}?", "answer": str(num1 + num2), "params": None}


def generate_area_question():
    shape = random.choice(["square", "rectangle", "triangle", "circle"])
    if shape == "square":
        side = random.randint(2, 10)
        question = f"What is the area of a square with side {side}?"
        answer = side * side
        shape_data = ("square", (side,))
    elif shape == "rectangle":
        l = random.randint(3, 12)
        w = random.randint(2, 10)
        question = f"What is the area of a rectangle with length {l} and width {w}?"
        answer = l * w
        shape_data = ("rectangle", (l, w))
    elif shape == "triangle":
        base = random.randint(4, 10)
        height_val = random.randint(3, 8)
        question = f"What is the area of a triangle with base {base} and height {height_val}?"
        answer = 0.5 * base * height_val
        shape_data = ("triangle", (base, height_val))
    elif shape == "circle":
        radius = random.randint(2, 8)
        question = f"What is the area of a circle with radius {radius}? (π ≈ 3.14)"
        answer = round(3.14 * radius * radius, 2)
        shape_data = ("circle", (radius,))
    return {
        "question": question,
        "answer": round(answer, 2),
        "shape_data": shape_data
        }

def generate_calculus_question():
    q_type = random.choice(["derivative", "integral"])
    x = random.randint(1, 5)
    if q_type == "derivative":
        return {
            "question": f"What is the derivative of {x}x^2?",
            "answer": str(2 * x) + "x"
        }
    else:
        return {
            "question": f"What is the integral of {x}x?",
            "answer": f"{x/2}x^2 + C"
        }

def get_random_question(difficulty):
    if difficulty == "Easy":
        return generate_addition_question()
    elif difficulty == "Medium":
        return generate_area_question()
    elif difficulty == "Hard":
        return generate_calculus_question()

def build_question_pool(difficulty):
    questions = []
    if difficulty == "Medium":
        questions = [generate_area_question() for _ in range(QUESTIONS_TO_WIN * 2)]
    elif difficulty == "Hard":
        questions = [generate_calculus_question() for _ in range(QUESTIONS_TO_WIN * 2)]
    else:
        questions = [generate_addition_question() for _ in range(QUESTIONS_TO_WIN * 2)]
    random.shuffle(questions)
    return questions


def save_to_leaderboard(name, time_taken):
    with open("leaderboard.txt", "a") as file:
        file.write(f"{name}: {time_taken:.2f} seconds\n")


def run_game(player_name, difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Math Race Challenge")
    clock = pygame.time.Clock()

    player_x = 0
    ai_x = 0
    player_score = 0

    questions = build_question_pool(difficulty)

    ai_speed = {"Easy": 40, "Medium": 25, "Hard": 10}[difficulty]  

    current_question = questions.pop()
    input_text = ""

    waiting = True
    while waiting:
        screen.fill(WHITE)
        screen.blit(TRACK_IMG, (0, 0))
        title = FONT.render("Press SPACE to Start the Race!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))
        
        instruction = FONT.render(f"Solve {QUESTIONS_TO_WIN} questions to win!", True, BLACK)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


    start_time = time.time()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        screen.blit(TRACK_IMG, (0, 0))

        ai_x += ai_speed * dt

        pygame.draw.line(screen, BLACK, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 5)

        target_x = (player_score * MOVE_DISTANCE)
        if player_x < target_x:
            player_x += min(5, target_x - player_x)

        screen.blit(PLAYER_CAR, (player_x, HEIGHT // 6))
        screen.blit(AI_CAR, (ai_x, HEIGHT // 2))

        player_label = FONT.render(f"{player_name} Position: {player_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        ai_label = FONT.render(f"AI Position: {int(ai_x) // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        screen.blit(player_label, (20, 20))
        screen.blit(ai_label, (20, 50))

        question_surface = FONT.render(current_question['question'], True, BLACK)
        screen.blit(question_surface, (20, HEIGHT - 210))

        pygame.draw.rect(screen, WHITE, (20, HEIGHT - 160, 200, 35))
        pygame.draw.rect(screen, BLACK, (20, HEIGHT - 160, 200, 35), 2)
        input_surface = INPUT_FONT.render(input_text, True, BLACK)
        screen.blit(input_surface, (30, HEIGHT - 155))

        box_width, box_height = 200, 160
        box_x = WIDTH - box_width - 20
        box_y = HEIGHT - box_height - 20
        shape_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, WHITE, shape_box_rect)
        pygame.draw.rect(screen, BLACK, shape_box_rect, 3)


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

            shape_center_x = box_x + box_width // 2
            shape_center_y = box_y + box_height // 2 + 5  

            max_shape_size = 100

            if p["shape"] == "square":
                side_pixels = max_shape_size
                top_left = (shape_center_x - side_pixels // 2, shape_center_y - side_pixels // 2)
                pygame.draw.rect(screen, BLACK, (*top_left, side_pixels, side_pixels), 2)
                label = FONT.render(f"{p['side']} cm", True, BLACK)
                screen.blit(label, (top_left[0] + side_pixels // 2 - label.get_width() // 2, top_left[1] + side_pixels + 5))

            elif p["shape"] == "rectangle":
                w_ratio = p["width"]
                h_ratio = p["height"]
                max_dim = max(w_ratio, h_ratio)
                width_px = int((w_ratio / max_dim) * max_shape_size)
                height_px = int((h_ratio / max_dim) * max_shape_size)
                top_left = (shape_center_x - width_px // 2, shape_center_y - height_px // 2)
                pygame.draw.rect(screen, BLACK, (*top_left, width_px, height_px), 2)
                screen.blit(FONT.render(f"{p['width']} cm", True, BLACK), (top_left[0] + width_px // 2 - 20, top_left[1] + height_px + 5))
                screen.blit(FONT.render(f"{p['height']} cm", True, BLACK), (top_left[0] - 45, top_left[1] + height_px // 2 - 10))

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

            elif p["shape"] == "circle":
                max_cm = 15  
                radius_px = max(20, int((p["radius"] / max_cm) * max_shape_size))
                center = (shape_center_x, shape_center_y)
                pygame.draw.circle(screen, BLACK, center, radius_px, 2)

                pygame.draw.line(screen, BLACK, center, (center[0] + radius_px, center[1]), 2)
                screen.blit(FONT.render(f"{p['radius']} cm", True, BLACK), (center[0] + radius_px + 5, center[1] - 15))

        pygame.display.flip()

        if player_x >= WIDTH - CAR_WIDTH:
            total_time = time.time() - start_time
            messagebox.showinfo("You Win!", f"You beat the AI in {total_time:.2f} seconds!")
            save_to_leaderboard(player_name, total_time)
            running = False
            break
        elif ai_x >= WIDTH - CAR_WIDTH:
            messagebox.showinfo("You Lose", "The AI won this time. Try again!")
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    user_answer = input_text.strip().replace(" ", "").lower()
                    correct_answer = current_question['answer'].strip().replace(" ", "").lower()
                    if user_answer == correct_answer:
                        player_score += 1
                    input_text = ""
                    if questions:
                        current_question = questions.pop()
                elif event.unicode.isprintable():
                    if len(input_text) < 10:
                        input_text += event.unicode

def start_game():
    def on_difficulty_select(selected_difficulty):
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return
        root.destroy()
        run_game(name, selected_difficulty)

    root = tk.Tk()
    root.title("Math Racing Game Setup")
    root.geometry("400x300")

    tk.Label(root, text="Enter your name:", font=("Courier", 14)).pack(pady=10)
    name_entry = tk.Entry(root, font=("Courier", 14))
    name_entry.pack(pady=10)

    tk.Label(root, text="Select Difficulty:", font=("Courier", 14)).pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Easy", width=10, font=("Courier", 12), command=lambda: on_difficulty_select("Easy")).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Medium", width=10, font=("Courier", 12), command=lambda: on_difficulty_select("Medium")).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Hard", width=10, font=("Courier", 12), command=lambda: on_difficulty_select("Hard")).grid(row=0, column=2, padx=5)

    root.mainloop()


start_game()
pygame.quit()
