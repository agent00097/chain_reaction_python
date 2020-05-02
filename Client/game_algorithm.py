playerOneAtoms = []
playerTwoAtoms = []

grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell
 

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

    if (row == 9 and column == 0):
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

    if (row == 0 and column == 9):
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


    if (row == 9 and column == 9):
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

    if (row == 0 and column >=1 and column <=8):
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

    if (row == 9 and column >=1 and column <=8):
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

    if (column == 9 and row >=1 and row <=8):
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


    if (column == 0 and row >=1 and row <=8):
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

def checkForWin():
    if(len(playerOneAtoms) == 0):
        #Player 2 has won, end the game
        #print("Player 2 won")
        return 2
        
    elif(len(playerTwoAtoms) == 0):
        #Player 1 has won, end the game
        #print("Player 1 won")
        return 1
    else:
        #Game is still going on, continue
        return 0