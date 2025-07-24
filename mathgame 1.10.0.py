import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import os

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
FPS = 60

# Car settings
CAR_WIDTH, CAR_HEIGHT = 120, 100
PLAYER_CAR = pygame.image.load("car_player.png")
PLAYER_CAR = pygame.transform.scale(PLAYER_CAR, (CAR_WIDTH, CAR_HEIGHT))
AI_CAR = pygame.image.load("car_ai.png")
AI_CAR = pygame.transform.scale(AI_CAR, (CAR_WIDTH, CAR_HEIGHT))

FINISH_LINE = 100
QUESTIONS_TO_WIN = 6
MOVE_DISTANCE = WIDTH // QUESTIONS_TO_WIN

# Fonts
font = pygame.font.SysFont("Courier", 24)

# Question pool
image_questions = [
    {"question": "What is the y-intercept?", "answer": "3"},
    {"question": "What is the slope?", "answer": "-2"},
    {"question": "What is the slope of the line?", "answer": "-4"},
    {"question": "What is the y-intercept?", "answer": "4"}
]

def generate_math_question():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    return {"question": f"What is {num1} + {num2}?", "answer": str(num1 + num2)}

def build_question_pool():
    return image_questions + [generate_math_question() for _ in range(6)]

def get_player_input(question):
    root = tk.Tk()
    root.withdraw()
    answer = simpledialog.askstring("Answer the Question", question)
    root.destroy()
    return answer

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

    ai_speed = {"Easy": 0.4, "Medium": 0.6, "Hard": 1.0}[difficulty]
    start_time = time.time()

    running = True
    while running:
        screen.fill(WHITE)

        pygame.draw.line(screen, BLACK, (WIDTH - 10, 0), (WIDTH - 10, HEIGHT), 5)

        screen.blit(PLAYER_CAR, (player_x, HEIGHT // 4))
        screen.blit(AI_CAR, (ai_x, HEIGHT // 2))

        player_label = font.render(f"{player_name} Position: {player_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        ai_label = font.render(f"AI Position: {ai_x // MOVE_DISTANCE}/{QUESTIONS_TO_WIN}", True, BLACK)
        screen.blit(player_label, (20, 20))
        screen.blit(ai_label, (20, 50))

        pygame.display.flip()
        clock.tick(FPS)

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

        if player_score < QUESTIONS_TO_WIN:
            current = questions.pop()
            user_ans = get_player_input(current['question'])
            if user_ans and user_ans.strip() == current['answer']:
                player_x += MOVE_DISTANCE
                player_score += 1

        ai_x += ai_speed * MOVE_DISTANCE / 2

def start_game():
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Player Name", "Enter your name:")
    difficulty = simpledialog.askstring("Difficulty", "Choose difficulty: Easy, Medium, Hard")
    if not name or difficulty not in ["Easy", "Medium", "Hard"]:
        messagebox.showwarning("Input Error", "Please enter a valid name and difficulty.")
        return
    run_game(name, difficulty)

start_game()
pygame.quit()
