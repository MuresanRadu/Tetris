import pygame
import random
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of each Tetris block
block_size = 20

# Set the width and height of the playing field
field_width = 10
field_height = 20

# Set the width and height of the window
window_width = block_size * field_width
window_height = block_size * field_height

# Set the frame rate
frame_rate = 60

# Initialize Pygame
pygame.init()

# Set the window title
pygame.display.set_caption("Tetris")

# Set the window size
screen = pygame.display.set_mode([window_width, window_height])

# Set the frame rate clock
clock = pygame.time.Clock()

# Define the shapes of the Tetris blocks
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 2, 2],
     [2, 2, 0]],
    
    [[3, 3, 0],
     [0, 3, 3]],
    
    [[4, 0, 0],
     [4, 4, 4]],
    
    [[0, 0, 5],
     [5, 5, 5]],
    
    [[6, 6, 6, 6]],
    
    [[7, 7],
     [7, 7]]
]

# Define the colors of the Tetris blocks
tetris_colors = [
    (0,   0,   0  ), # black
    (255, 0,   0  ), # red
    (0,   255, 0  ), # green
    (0,   0,   255), # blue
    (255, 120, 0  ), # orange
    (255, 255, 0  ), # yellow
    (180, 0,   255)  # purple
]

def create_field():
    # Create an empty field
    field = []
    for i in range(field_height):
        field.append([0] * field_width)
    return field

def add_block(block, field, x_pos=3, y_pos=0):
    # Add a block to the field
    for y in range(len(block)):
        for x in range(len(block[y])):
            if block[y][x] != 0:
                field[y_pos + y][x_pos + x] = block[y][x]
    return field

def remove_row(field, row):
    # Remove a row from the field and shift the rows above it down
    del field[row]
    field.insert(0, [0] * field_width)
    return field

def check_collision(block, field, x_pos=3, y_pos=0):
    # Check if the block collides with anything on the field
    for y in range(len(block)):
        for x in range(len(block[y])):
            if block[y][x] != 0:
                if int(y_pos) + y >= field_height or x_pos + x < 0 or x_pos + x >= field_width:
                    return True
                if field[int(y_pos) + y][x_pos + x] != 0:
                    return True
    return False

# Set the fall speed of the blocks in pixels per second
fall_speed = 500

def check_rows(field):
    # Check if any rows are complete and remove them
    rows_removed = 0
    y = field_height - 1
    while y >= 0:
        row_complete = True
        for x in range(field_width):
            if field[y][x] == 0:
                row_complete = False
                break
        if row_complete:
            rows_removed += 1
            field = remove_row(field, y)
        else:
            y -= 1
    return field, rows_removed

# Create an empty field
field = create_field()
y_pos = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the field
    field, rows_removed = check_rows(field)

    # Select a random block and add it to the field
    block = random.choice(tetris_shapes)
    if check_collision(block, field):
        break
    field = add_block(block, field)

    # Update the block position
    elapsed_time = clock.tick(frame_rate)
    y_pos += elapsed_time / 1000.0 * fall_speed
    if check_collision(block, field, y_pos=y_pos):
        y_pos -= elapsed_time / 1000.0 * fall_speed

    # Check if the game is over
    if y_pos < 0:
        break

    # Draw the field
    screen.fill(BLACK)
    for y in range(field_height):
        for x in range(field_width):
            if field[y][x] != 0:
                color = tetris_colors[field[y][x] - 1]
                pygame.draw.rect(screen, color, [x * block_size, y * block_size, block_size, block_size])

    # Update the display
    pygame.display.flip()