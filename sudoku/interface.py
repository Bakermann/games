# import pygame library
import pygame
from grid_generator import Sudoku

# initialise the pygame font
pygame.font.init()

# Total window
screen = pygame.display.set_mode((500, 650))

# Title and Icon
pygame.display.set_caption("SUDOKU")

x = 0
y = 0
dif = 500 / 9
val = 0
# Default Sudoku Board.

sdk = Sudoku()
grid = sdk.sudoku()
gr = [row[:] for row in grid]  # initial grid

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)


def get_cord(pos):
    global x
    x = pos[0] // dif
    global y
    y = pos[1] // dif


# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines

    for i in range(9):
        for j in range(9):
            if gr[i][j] != 0:

                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 13, j * dif + 3))
            elif gr[i][j] == 0 and grid[i][j] != 0:
                pygame.draw.rect(screen, (255, 255, 255), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 13, j * dif + 3))

    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 2
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)


# Fill value entered in cell
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# Display instruction for the game
def instruction():
    text1 = font2.render("Press D to reset / S to change grid", 1, (0, 0, 0))
    text2 = font2.render("Press Q to verify / F to solve", 1, (0, 0, 0))
    text3 = font2.render("1-a 2-z 3-e 4-r 5-t 6-y 7-u 8-i 9-o", 1, (0, 0, 0))
    screen.blit(text1, (20, 510))
    screen.blit(text2, (20, 530))
    screen.blit(text3, (20, 550))


# Display options when solved
def result():
    text1 = font1.render("FINISHED!", 1, (255, 0, 0))
    text2 = font2.render("Press S for a new grid", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))
    screen.blit(text2, (165, 575))


def run_game():
    global val, gr, sdk, grid, x, y
    run = True
    flag1 = 0
    flag2 = 0
    rs = 0
    # The loop thats keep the window running
    while run:

        # White color background
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
            # Get the mouse position to insert number
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                get_cord(pos)
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    y -= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    y += 1
                    flag1 = 1
                if event.key == pygame.K_a:
                    val = 1
                if event.key == pygame.K_z:
                    val = 2
                if event.key == pygame.K_e:
                    val = 3
                if event.key == pygame.K_r:
                    val = 4
                if event.key == pygame.K_t:
                    val = 5
                if event.key == pygame.K_y:
                    val = 6
                if event.key == pygame.K_u:
                    val = 7
                if event.key == pygame.K_i:
                    val = 8
                if event.key == pygame.K_o:
                    val = 9
                if event.key == pygame.K_q:  # verify
                    flag2 = 1
                if event.key == pygame.K_f:  # solve
                    grid = sdk.resolver(grid, sdk.n_missing(grid))
                # If R pressed clear the sudoku board
                if event.key == pygame.K_s:
                    rs = 0
                    flag2 = 0
                    grid = sdk.sudoku()
                    gr = [row[:] for row in grid]
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    rs = 0
                    flag2 = 0
                    grid = gr
        if flag2 == 1:
            if sdk.verif(gr, grid) == 1:
                rs = 1
            flag2 = 0
        if val != 0:
            draw_val(val)
            if gr[int(x)][int(y)] == 0 and grid[int(x)][int(y)] != val:
                grid[int(x)][int(y)] = val
                flag1 = 0
            elif gr[int(x)][int(y)] == 0 and grid[int(x)][int(y)] == val:
                grid[int(x)][int(y)] = 0
            flag1 = 0
            val = 0

        if rs == 1:
            result()
        draw()
        if flag1 == 1:
            draw_box()
        instruction()

        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()

if __name__ == "__main__":
    run_game()
