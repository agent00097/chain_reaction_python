import pygame
from tkinter import *

# Define some colors
LIGHT_RED = (249, 200, 200)
LIGHT_GREEN = (200, 249, 226)
LIGHT_RED_2 = (243, 95, 129)
LIGHT_GREEN_2 = (101, 255, 78)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (88, 214, 141)
RED = (231, 76, 60)
DARK_GREEN = (12, 75, 3)
DARK_RED = (124, 13, 43)
ORANGE = (255,174,66)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

#Getting Font
player_turn = 0
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

def deleteTheAtom(row, column):
    if (row, column) in playerOneAtoms:
        playerOneAtoms.remove(tuple([row, column]))
    if (row, column) in playerTwoAtoms:
        playerTwoAtoms.remove(tuple([row, column]))


def checkForRowAndColumn(row, column, player_turn):
    if (row == 0 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 8 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 0 and column == 8):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (row == 8 and column == 8):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 0 and column >=1 and column <=7):
        #We now check for three
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 9 and column >=1 and column <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (column == 9 and row >=1 and row <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (column == 0 and row >=1 and row <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    else:
        checkForTheFour(row, column, player_turn)

done = False

def checkForWin():
    if(len(playerOneAtoms) == 0):
        #Player 2 has won, end the game
        print("Player 2 won")
        done = True
    elif(len(playerTwoAtoms) == 0):
        #Player 1 has won, end the game
        print("Player 1 won")
        done = True
    else:
        #Game is still going on, continue
        return  


def checkForTheFour(row, column, player_turn):
    if(grid[row][column] == 4):
        grid[row][column] = 0
        grid[row+1][column] += 1
        deleteTheAtom(row+1, column)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row+1, column]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row+1, column]))
        checkForRowAndColumn(row+1, column, player_turn)
        grid[row][column+1] += 1
        deleteTheAtom(row, column+1)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row, column+1]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row, column+1]))
        checkForRowAndColumn(row, column+1, player_turn)
        grid[row-1][column] += 1
        deleteTheAtom(row-1, column)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row-1, column]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row-1, column]))  
        checkForTheFour(row-1, column, player_turn)
        grid[row][column-1] += 1
        deleteTheAtom(row, column-1)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row, column-1]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row, column-1]))
        checkForRowAndColumn(row, column-1, player_turn)
# Set title of screen
pygame.display.set_caption("Game Window:")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

font=pygame.font.SysFont('arial', 40)
text=font.render('@', True, (0, 0, 0)) 

turn = 0

for row in range(10):
        for column in range(10):
            color = WHITE
            # if grid[row][column] == 1:
            #     if (turn % 2):
            #         color = LIGHT_RED
            #     else:
            #         color = LIGHT_GREEN
            # if grid[row][column] == 2:
            #     if (turn % 2):
            #         color = LIGHT_RED_2
            #     else:
            #         color = LIGHT_GREEN_2
            # if grid[row][column] == 3:
            #     if (turn % 2):
            #         color = RED
            #     else:
            #         color = GREEN
            # if grid[row][column] == 4:
            #     if (turn % 2):
            #         color = DARK_RED
            #     else:
            #         color = DARK_GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

# -------- Main Program Loop -----------
while not done:
    if len(playerOneAtoms) == 0 and turn > 2:
        Tk().wm_withdraw() #to hide the main window
        messagebox.showinfo('Player Two Won','Player Two Won')
        screen.quit()
    if len(playerTwoAtoms) == 0 and turn > 2:
        Tk().wm_withdraw() #to hide the main window
        messagebox.showinfo('Player One Won','Player One Won')
        screen.quit()
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            
            if turn % 2:
                #This is to add the atom in the player's data structure
                #Before adding and bursting bubble we need to make sure that this cell is not occupied by the other player
                if (row, column) in playerOneAtoms:
                    print("You can't click there")
                else:
                    if (row, column) in playerTwoAtoms:
                        print("It is already in the block")
                        player_turn = 2     
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, player_turn)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        print("PlayerOneAtoms are: ", playerOneAtoms)
                        print("PlayerTwoAtoms are: ", playerTwoAtoms)
                    else:
                        playerTwoAtoms.append(tuple([row, column]))
                        player_turn = 2     
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, player_turn)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        print("PlayerOneAtoms are: ", playerOneAtoms)
                        print("PlayerTwoAtoms are: ", playerTwoAtoms)

            else:
                if (row, column) in playerTwoAtoms:
                    print("You can't click there")
                else:
                    if (row, column) in playerOneAtoms:
                        print("It is already in the list")
                        player_turn = 1
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, player_turn)
                        print("Click ", pos, "Grid coordinates: ", row, column) 
                        print("PlayerOneAtoms are: ", playerOneAtoms)
                        print("PlayerTwoAtoms are: ", playerTwoAtoms)
                    else:
                        playerOneAtoms.append(tuple([row, column]))
                        player_turn = 1
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, player_turn)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        print("PlayerOneAtoms are: ", playerOneAtoms)
                        print("PlayerTwoAtoms are: ", playerTwoAtoms)
                    

 
    # Set the screen background
    if turn % 2:
        screen.fill(RED)
    else:
        screen.fill(GREEN)
 
    # Draw the grid
    
    for row in range(10):
        for column in range(10):
            color = WHITE
            # if grid[row][column] == 1:
            #     if (turn % 2):
            #         color = LIGHT_RED
            #     else:
            #         color = LIGHT_GREEN
            # if grid[row][column] == 2:
            #     if (turn % 2):
            #         color = LIGHT_RED_2
            #     else:
            #         color = LIGHT_GREEN_2
            # if grid[row][column] == 3:
            #     if (turn % 2):
            #         color = RED
            #     else:
            #         color = GREEN
            # if grid[row][column] == 4:
            #     if (turn % 2):
            #         color = DARK_RED
            #     else:
            #         color = DARK_GREEN
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
            if (row, column) in playerOneAtoms:
                if grid[row][column] == 1:
                    color = LIGHT_GREEN
                elif grid[row][column] == 2:
                    color = LIGHT_GREEN_2
                elif grid[row][column] == 3:
                    color = GREEN
                else:
                    color = DARK_GREEN
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    #This is to update the screen according to player two
    for row in range(10):
        for column in range(10):
            #Color of the player one is red
            if (row, column) in playerTwoAtoms:
                if grid[row][column] == 1:
                    color = LIGHT_RED
                elif grid[row][column] == 2:
                    color = LIGHT_RED_2
                elif grid[row][column] == 3:
                    color = RED
                else:
                    color = DARK_RED
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()