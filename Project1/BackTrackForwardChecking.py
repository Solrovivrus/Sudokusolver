from PuzzleReader import PuzzleReader
from SolutionChecker import SolutionChecker
import numpy as np


''' Contributors: Derek Logan
----------------------------------------------------------------------------------------------
BackTrackForwardChecking class has one main purpose. This class uses backtracking combined with
forward checking to solve puzzles. solve() gets the domain of possible choices through 
obtainDomain() and only chooses possible cell values through the given domain which is populated
each iteration. 

decisionCount gets a +1 everytime a choice is considered, a choice is placed on the board, and 
when backtracking occurs (for empty domain or otherwise)
----------------------------------------------------------------------------------------------
'''

class BackTrackForwardChecking:
    decisionCount = 0 
    numBacks = 0

    # --------------------------------------------------------------------------------------------
    
    # The nextCell function iterates through a passed game board and updates the current location 
    # of the player. If cell found, return location. If not, return False
    @staticmethod
    def nextCell(mtrx, location):
        for i in range(len(mtrx)):
            for j in range(len(mtrx[0])):
                if mtrx[i,j] == ' ':
                    location = [i,j]
                    return(location)
        return(False)

    
    # matrixSelection moves through passed Sudoku difficulty sending each file one at a time
    @staticmethod
    def matrixSelection(difficulty):
        backtrackF = BackTrackForwardChecking
        # iterate through and send to solve()
        for mtrx in difficulty:
            currentMatrix = backtrackF.solve(mtrx)


    # solve() takes a matrix from matrixSelection and solves it by recursively backtracking if encountering an obstacle 
    @staticmethod
    def solve(mtrx):
        backtrackF = BackTrackForwardChecking
        puzzle = PuzzleReader
        check = SolutionChecker

        # creates domain for unpopulated cell in board
        domain = backtrackF.obtainDomain(mtrx)
        # check through domains to see if an empty list was populated which indicates an empty domain
        # if found, backtrack!
        for i in range(len(domain)):
            for j in range(len(domain[0])):
                if domain[i,j] == 0:
                    continue
                # if length exists, continue through
                elif len(domain[i,j]):
                    continue
                # if cell is list and empty, backtrack for empty domain
                else:
                    backtrackF.decisionCount +=1
                    print("Backtracking... FROM NO LENGTH") # will remove before turn-in
                    return False

        #currentLocation starts at first cell, then finds next empty cell
        currentLocation = [0,0]
        currentLocation = backtrackF.nextCell(mtrx, currentLocation)

        # if currentLocation is checked and contains False because nextCell couldn't find anything, game complete
        if not currentLocation:
            print("No cells left", "Number of decisions made: " + str(backtrackF.decisionCount), "Number of backtracks: " + str(backtrackF.numBacks), sep = "\n")
            return True
        # iterate through all possible values while checking through SolutionChecker
        for i in domain[currentLocation[0], currentLocation[1]]:
            backtrackF.decisionCount +=1
            # if current location and value is valid across row, column, and box.. place the value in cell
            if check.is_valid_cell(i, currentLocation[0], currentLocation[1], mtrx):
                mtrx[currentLocation[0],currentLocation[1]] = i
                # +1 decisionCount when placing a number
                backtrackF.decisionCount += 1
                print(puzzle.print_puzzle(mtrx)) # printing each placement (will be deleted for final turn-in)
                # return true if solve works
                if backtrackF.solve(mtrx):
                    return True
            
                # resetting spot to blank if encountering an error
                mtrx[currentLocation[0], currentLocation[1]] = ' '

        # +1 decisionCount when backtracking
        # +1 numBacks when backtracking
        # returns false if need arises to backtrack
        backtrackF.decisionCount +=1
        backtrackF.numBacks += 1
        print("Backtracking...") # will delete before turn-in
        return False


    # obtainDomain() takes the gameboard and creates a complete domain of empty cells on the gameboard
    @staticmethod
    def obtainDomain(mtrx):
        check = SolutionChecker
        # creating domain matrix for gameboard. Any cell with a number in its place will have a domain of 0
        domain = np.full_like(mtrx,0)
        # finds empty cells in gameboard, places empty list in same cell in domain matrix
        for i in range(len(domain)):
            for j in range(len(domain[0])):
                if mtrx[i,j] == ' ':  
                    domainList = []
                    domain[i,j] = domainList
                    # checks range 1-9 for possible values and populates domainList
                    for num in range(1,10):
                        if check.is_valid_cell(num, i, j, mtrx):
                            domain[i,j].append(num)
                        else:
                            continue
                else:
                    continue

        return(domain)
        


