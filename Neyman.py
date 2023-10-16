import pygame
import sys
import random
from bitstring import BitArray


def get_empty_state(width, height):
    """Create an empty state grid with the specified width and height."""
    return [[0 for y in range(height)] for x in range(width)]


def get_next_state(state, rules):
    """Calculate the next state based on the current state and given rules."""
    next_state = get_empty_state(len(state), len(state[0]))
    for i in range(len(state)):
        for j in range(len(state[i])):
            neighborhood = ''
            for ii in range(i-1, i+2):
                for jj in range(j-1, j+2):
                    if abs(ii - i) + abs(jj - j) == 2:
                        continue
                    if ii < 0 or ii >= len(state) or jj < 0 or jj >= len(state[i]):
                        neighborhood += '0'
                    else:
                        neighborhood += str(state[ii][jj])
            next_state[i][j] = rules[neighborhood]
    return next_state


def draw_game_state(state):
    """Draw the current state of the game on the screen."""
    screen.fill(black)
    for i in range(len(state)):
        for j in range(len(state[i])):
            color = white if state[i][j] == 1 else black
            pygame.draw.rect(screen, color, (j*cell_size+cell_margin, i*cell_size +
                             cell_margin, cell_size-cell_margin*2, cell_size-cell_margin*2))
    pygame.display.flip()


# Get user input for window width and height
width, height = 0, 0
while width <= 0 or height <= 0:
    width_str = input("Enter the width of the game window: ")
    height_str = input("Enter the height of the game window: ")
    try:
        width = int(width_str)
        height = int(height_str)
    except ValueError:
        print("Invalid input. Please enter valid width and height values.")

# Set window size and cell parameters

cell_size = 15
window_size = (width*15, height*15)
cell_margin = 1

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

# Create the initial state grid
state = get_empty_state(
    window_size[1] // cell_size, window_size[0] // cell_size)

# Ask the user for the initial setup
user_choice = input(
    "Do you want a random setup (R) or one cell in the middle (M)? (R/M): ")
if user_choice.lower() == "r":
    Chance1 = float(input("Set a chance of white cell from 0 to 1: "))
    Chance0 = 1 - Chance1
    for j in range(len(state)):
        state[j] = random.choices(
            [0, 1], weights=[Chance0, Chance1], k=len(state[j]))
elif user_choice.lower() == "m":
    state[len(state) // 2][len(state[0]) // 2] = 1

# Ask the user for the rule number
rule_number = input("Write the rule number: ")
binary_rule = BitArray(int=rule_number, length=32)
rules = {}
for i in range(32):
    rules[bin(i)[2:].zfill(5)] = int(binary_rule[31 - i])

# Initialize the Pygame library
pygame.init()

# Create the game window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cellular Automata")

# Define a variable for pausing the game
paused = True
stateCopy = state
font = pygame.font.Font(None, 36)


def update_rule_text():
    """Update the text displaying the rule number."""
    return font.render(f"Rule Number: {rule_number}", True, white)


rule_text = update_rule_text()
menu_rect = pygame.Rect(10, 10, 300, 50)
show_menu = False
input_text = ""

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                stateCopy = state
            elif event.key == pygame.K_n:
                stateCopy = get_next_state(stateCopy, rules)
                draw_game_state(stateCopy)
                paused = True
            elif event.key == pygame.K_m:
                show_menu = not show_menu
            elif event.key == pygame.K_RETURN:
                rule_number = int(input_text)
                binary_rule = bin(rule_number)[2:].zfill(32)
                rules = {bin(i)[2:].zfill(5): int(binary_rule[31 - i])
                         for i in range(32)}
                show_menu = False
            elif show_menu:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if not paused:
        stateCopy = get_next_state(stateCopy, rules)
        draw_game_state(stateCopy)

    if show_menu:
        pygame.draw.rect(screen, black, menu_rect)
        pygame.draw.rect(screen, white, menu_rect, 2)
        screen.blit(font.render(
            f"Rule Number: {input_text}", True, white), (15, 15))

    pygame.display.flip()
    pygame.time.delay(50)
