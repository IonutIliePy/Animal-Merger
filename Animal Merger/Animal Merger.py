import pygame
import random
import asyncio
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE - 2.3
TILE_PADDING = 10  # Add padding between tiles
NEW_TILE_SIZE = TILE_SIZE - TILE_PADDING
BLUE = (157, 228, 252)
PINK = (242, 24, 239)
BLACK = (0, 0, 0)
FPS = 60

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Merger")

# Load images
start_background = pygame.transform.scale(pygame.image.load("Data/start_background.png"), (WIDTH, HEIGHT))
game_background = pygame.transform.scale(pygame.image.load("Data/game_background.png"), (WIDTH, HEIGHT))
game_over_background = pygame.transform.scale(pygame.image.load("Data/game_over_background.png"), (WIDTH, HEIGHT))

# Load number images individually
image_2 = pygame.image.load("Data/2.png")
image_4 = pygame.image.load("Data/4.png")
image_8 = pygame.image.load("Data/8.png")
image_16 = pygame.image.load("Data/16.png")
image_32 = pygame.image.load("Data/32.png")
image_64 = pygame.image.load("Data/64.png")
image_128 = pygame.image.load("Data/128.png")
image_256 = pygame.image.load("Data/256.png")
image_512 = pygame.image.load("Data/512.png")
image_1024 = pygame.image.load("Data/1024.png")
image_2048 = pygame.image.load("Data/2048.png")

# Initialize the mixer
pygame.mixer.init()


# Load sound effect
key_press_sound = pygame.mixer.Sound("Data/key_press_sound.ogg")
# Load music
pygame.mixer.music.load("Data/background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music in an infinite loop

# Load sound effects
key_press_sound = pygame.mixer.Sound("Data/key_press_sound.ogg")
win_sound = pygame.mixer.Sound("Data/win_sound.ogg")
lose_sound = pygame.mixer.Sound("Data/lose_sound.ogg")


# Function to play sound on key press
def play_key_press_sound():
    key_press_sound.play()

# Function to play sound when the player wins
def play_win_sound():
    win_sound.play()

# Function to play sound when the player loses
def play_lose_sound():
    lose_sound.play()

# Function to reset the game state
def reset_game():
    global highest_number, game_grid
    highest_number = 0
    game_grid = init_grid()
    add_tile(game_grid)
    add_tile(game_grid)


# Function to initialize the game grid
def init_grid():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Function to add a new tile (2 or 4) to the grid at a random empty position
def add_tile(grid):
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = random.choice([2, 4])

# Function to draw the grid and tiles
def draw_grid(grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            tile_value = grid[x][y]
            tile_x = y * TILE_SIZE + TILE_PADDING
            tile_y = x * TILE_SIZE + TILE_PADDING

            pygame.draw.rect(screen, BLUE, (tile_x, tile_y, NEW_TILE_SIZE, NEW_TILE_SIZE))

            if tile_value != 0:
                image = get_image_for_number(tile_value)
                image = pygame.transform.scale(image, (NEW_TILE_SIZE, NEW_TILE_SIZE))
                screen.blit(image, (tile_x, tile_y))

# Function to get the image for a specific number
def get_image_for_number(number):
    if number == 2:
        return image_2
    elif number == 4:
        return image_4
    elif number == 8:
        return image_8
    elif number == 16:
        return image_16
    elif number == 32:
        return image_32
    elif number == 64:
        return image_64
    elif number == 128:
        return image_128
    elif number == 256:
        return image_256
    elif number == 512:
        return image_512
    elif number == 1024:
        return image_1024
    elif number == 2048:
        return image_2048
    else:
        # Default to an empty image for other numbers
        return pygame.Surface((TILE_SIZE, TILE_SIZE))

# Function to check if there are any valid moves left
def is_game_over(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if grid[i][j] == 0 or grid[i][j] == grid[i][j + 1]:
                return False
    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE - 1):
            if grid[i][j] == 0 or grid[i][j] == grid[i + 1][j]:
                return False
    return True

# Function to check for a win condition (2048 tile)
def has_won(grid):
    for row in grid:
        if 2048 in row:
            return True
    return False

# Function to move tiles in a row or column
def move_tiles(line):
    new_line = [value for value in line if value != 0]
    while len(new_line) < GRID_SIZE:
        new_line.append(0)
    for i in range(GRID_SIZE - 1):
        if new_line[i] == new_line[i + 1] and new_line[i] != 0:
            new_line[i] *= 2
            new_line[i + 1] = 0
    new_line = [value for value in new_line if value != 0]
    while len(new_line) < GRID_SIZE:
        new_line.append(0)
    return new_line

# Function to move tiles in the entire grid
def move(direction, grid):
    if direction == "UP":
        grid = [list(x) for x in zip(*grid)]
        for i in range(GRID_SIZE):
            grid[i] = move_tiles(grid[i])
        grid = [list(x) for x in zip(*grid)]
    elif direction == "DOWN":
        grid = [list(x) for x in zip(*grid)]
        for i in range(GRID_SIZE):
            grid[i] = move_tiles(grid[i][::-1])[::-1]
        grid = [list(x) for x in zip(*grid)]
    elif direction == "LEFT":
        for i in range(GRID_SIZE):
            grid[i] = move_tiles(grid[i])
    elif direction == "RIGHT":
        for i in range(GRID_SIZE):
            grid[i] = move_tiles(grid[i][::-1])[::-1]
    return grid

# Function to display start screen
def show_start_screen():
    screen.blit(start_background, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        pygame.time.Clock().tick(FPS)

# Function to display game over screen
def show_game_over_screen(highest_number):
    screen.blit(game_over_background, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Biggest Animal: {highest_number}", True, PINK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100))
    screen.blit(text, text_rect)

    # Display the image corresponding to the highest number
    image = get_image_for_number(highest_number)
    image = pygame.transform.scale(image, (NEW_TILE_SIZE * 2, NEW_TILE_SIZE * 2))
    image_rect = image.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
    screen.blit(image, image_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
        pygame.time.Clock().tick(FPS)

# Show the start screen
show_start_screen()






# Main game loop
running = True
highest_number = 0
game_grid = init_grid()
add_tile(game_grid)
add_tile(game_grid)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            play_key_press_sound()  # Play sound on key press

            if event.key == pygame.K_UP:
                new_grid = move("UP", game_grid)
            elif event.key == pygame.K_DOWN:
                new_grid = move("DOWN", game_grid)
            elif event.key == pygame.K_LEFT:
                new_grid = move("LEFT", game_grid)
            elif event.key == pygame.K_RIGHT:
                new_grid = move("RIGHT", game_grid)
            elif event.key == pygame.K_r:  # Press 'R' to restart
                reset_game()
                continue  # Skip the rest of the event handling for this iteration

            if new_grid != game_grid or True:
                game_grid = new_grid
                add_tile(game_grid)
                if has_won(game_grid):
                    print("You won!")
                    play_win_sound()
                    reset_game()
                elif is_game_over(game_grid):
                    print("Game Over!")
                    play_lose_sound()
                    if highest_number < max(map(max, game_grid)):
                        highest_number = max(map(max, game_grid))
                    show_game_over_screen(highest_number)
                    reset_game()

    # Fill the background
    screen.blit(game_background, (0, 0))

    # Draw the grid and tiles
    draw_grid(game_grid)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
