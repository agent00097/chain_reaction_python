import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (88, 214, 141)
RED = (231, 76, 60)
ORANGE = (255,174,66)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

#Getting Font

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

playerColor = [RED, GREEN]

noOfPlayers = 2
noOfBlocks = 100

players = []
for i in range(noOfPlayers):
    players.append(playerColor[i])

playerOneAtoms = []
playerTwoAtoms = []

def checkForRowAndColumn(row, column):
    if (row == 0 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            checkForRowAndColumn(row+1, column)
            grid[row][column+1] += 1
            checkForRowAndColumn(row, column+1)

    if (row == 9 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            checkForRowAndColumn(row-1, column)
            grid[row][column+1] += 1
            checkForRowAndColumn(row, column+1)

    if (row == 0 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            checkForRowAndColumn(row+1, column)
            grid[row][column-1] += 1
            checkForRowAndColumn(row, column-1)


    if (row == 9 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            checkForRowAndColumn(row-1, column)
            grid[row][column-1] += 1
            checkForRowAndColumn(row, column-1)

    if (row == 0 and column >=1 and column <=8):
        #We now check for three
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row+1][column] += 1
            checkForRowAndColumn(row+1, column)
            grid[row][column+1] += 1
            checkForRowAndColumn(row, column+1)
            grid[row][column-1] += 1
            checkForRowAndColumn(row, column-1)

    if (row == 9 and column >=1 and column <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            checkForRowAndColumn(row-1, column)
            grid[row][column+1] += 1
            checkForRowAndColumn(row, column+1)
            grid[row][column-1] += 1
            checkForRowAndColumn(row, column-1)

    if (column == 9 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            checkForRowAndColumn(row-1, column)
            grid[row+1][column] += 1
            checkForRowAndColumn(row+1, column)
            grid[row][column-1] += 1
            checkForRowAndColumn(row, column-1)


    if (column == 0 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            checkForRowAndColumn(row-1, column)
            grid[row+1][column] += 1
            checkForRowAndColumn(row+1, column)
            grid[row][column+1] += 1
            checkForRowAndColumn(row, column+1)

    else:
        checkForTheFour(row, column)

def checkForWin():
    if(len(playerOneAtoms) == 0):
        #Player 2 has won, end the game
        print("Player 2 won")
    elif(len(playerTwoAtoms) == 0):
        #Player 1 has won, end the game
        print("Player 1 won")
    else:
        #Game is still going on, continue
        return  

def checkIfRCexists(row ,column, list):
    for cell in list:

def checkForTheFour(row, column):
    if(grid[row][column] == 4):
        grid[row][column] = 0
        grid[row+1][column] += 1
        checkForRowAndColumn(row+1, column)
        grid[row][column+1] += 1
        checkForRowAndColumn(row, column+1)
        grid[row-1][column] += 1  
        checkForTheFour(row-1, column)
        grid[row][column-1] += 1
        checkForRowAndColumn(row, column-1)
# Set title of screen
pygame.display.set_caption("Game Window:")
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

font=pygame.font.SysFont('arial', 40)
text=font.render('@', True, (0, 0, 0)) 

turn = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            turn = turn + 1
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            grid[row][column] += 1
            if turn % 2:
                playerOneAtoms.append(tuple([row, column]))
            else:
                playerTwoAtoms.append(tuple([row, column]))
            checkForRowAndColumn(row, column)
            print("Click ", pos, "Grid coordinates: ", row, column)
            print("PlayerOneAtoms are: ", len(playerOneAtoms))
            print("PlayerTwoAtoms are: ", len(playerTwoAtoms))
            if turn > 2:
                checkForWin()
 
    # Set the screen background
    if turn % 2:
        screen.fill(RED)
    else:
        screen.fill(GREEN)
 
    # Draw the grid
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = YELLOW
            if grid[row][column] == 2:
                color = GREEN
            if grid[row][column] == 3:
                color = ORANGE
            if grid[row][column] == 4:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    #This is to update the screen according to player one
    for row in range(10):
        for column in range(10):
            #Color of the player one is green
            color = GREEN
            checkIfRCexists(row, column, playerOneAtoms)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()