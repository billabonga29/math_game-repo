import pygame
import tkinter as tk
from tkinter import messagebox
import random
import time
import os

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
FPS = 60

# Car settings
CAR_WIDTH, CAR_HEIGHT = 80, 100
PLAYER_CAR = pygame.image.load("car_player.png")
PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (CAR_WIDTH, CAR_HEIGHT))
AI_CAR = pygame.image.load("car_ai.png")
AI_CAR = pygame.transform.scale(AI_CAR, (CAR_WIDTH, CAR_HEIGHT))

TRACK_IMG = pygame.image.load("track.png")
TRACK_IMG = pygame.transform.scale(TRACK_IMG, (WIDTH, HEIGHT))

QUESTIONS_TO_WIN = 6
MOVE_DISTANCE = WIDTH // QUESTIONS_TO_WIN

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Courier", 24)
INPUT_FONT = pygame.font.SysFont("Courier", 20)


def generate_math_question():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    return {"question": f"What is {num1} + {num2}?", "answer": str(num1 + num2)}


def build_question_pool():
    return [generate_math_question() for _ in range(QUESTIONS_TO_WIN * 2)]


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
    questions = build_question_pool()
    random.shuffle(questions)

    ai_speed = {"Easy": 60, "Medium": 100, "Hard": 160}[difficulty]  # Speed in pixels per second
    start_time = time.time()

    current_question = questions.pop()
    input_text = ""

    waiting = True
    while waiting:
        screen.fill(WHITE)
        screen.blit(TRACK_IMG, (0, 0))
        title = FONT.render("Press SPACE to Start the Race!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2))
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

        screen.blit(PLAYER_CAR, (player_x, HEIGHT // 4))
        screen.blit(AI_CAR, (ai_x, HEIGHT // 2))

        player_label = FONT.render(f"{player_name} Position: {player_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        ai_label = FONT.render(f"AI Position: {ai_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        screen.blit(player_label, (20, 20))
        screen.blit(ai_label, (20, 50))

        question_surface = FONT.render(current_question['question'], True, BLACK)
        screen.blit(question_surface, (20, HEIGHT - 100))

        pygame.draw.rect(screen, WHITE, (20, HEIGHT - 60, 300, 40))
        pygame.draw.rect(screen, BLACK, (20, HEIGHT - 60, 300, 40), 2)
        input_surface = INPUT_FONT.render(input_text, True, BLACK)
        screen.blit(input_surface, (30, HEIGHT - 55))

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
                    if input_text.strip() == current_question['answer']:
                        player_x += MOVE_DISTANCE
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
