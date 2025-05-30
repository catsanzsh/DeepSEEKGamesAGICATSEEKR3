import pygame
from pygame.locals import *
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake properties
snake_block_size = 20
snake_speed = 15  # This controls the speed, higher is faster

# Clock for controlling FPS
clock = pygame.time.Clock()

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block_size, snake_block_size])

def message(msg, color):
    font = pygame.font.SysFont(None, 30)
    text = font.render(msg, True, color)
    screen.blit(text, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    game_over = False
    game_close = False

    # Initial snake position and movement direction
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    # Make sure the snake starts at a grid position
    x1 = round(x1 / snake_block_size) * snake_block_size
    y1 = round(y1 / snake_block_size) * snake_block_size

    x1_change = 0
    y1_change = 0

    # Snake body (list of coordinates)
    snake_list = []
    length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, WIDTH - snake_block_size) / snake_block_size) * snake_block_size
    foody = round(random.randrange(0, HEIGHT - snake_block_size) / snake_block_size) * snake_block_size

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block_size:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block_size:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block_size:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block_size:
                    y1_change = snake_block_size
                    x1_change = 0

        # Check if snake hits the boundary
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        
        screen.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block_size, snake_block_size])
        
        # Update snake body
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        
        # Remove extra segments if snake hasn't eaten food
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake hits itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Draw the snake
        draw_snake(snake_list)
        
        # Display score
        font = pygame.font.SysFont(None, 25)
        score_text = font.render(f"Score: {length_of_snake - 1}", True, WHITE)
        screen.blit(score_text, [0, 0])
        
        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            # Generate new food position
            foodx = round(random.randrange(0, WIDTH - snake_block_size) / snake_block_size) * snake_block_size
            foody = round(random.randrange(0, HEIGHT - snake_block_size) / snake_block_size) * snake_block_size
            # Increase snake length
            length_of_snake += 1

        # Control game speed (FPS)
        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    game_loop()
