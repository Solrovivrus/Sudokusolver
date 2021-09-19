from PuzzleReader import PuzzleReader
from SolutionChecker import SolutionChecker
import numpy as np
import pandas as pd

''' Contributors: Derek Logan
----------------------------------------------------------------------------------------------
BackTracking class has one main purpose.
    1) Implement solve() and nextCell() function to build candidate solutions to solving the 
    given sudoku puzzles with a backtracking algorithm. 
----------------------------------------------------------------------------------------------
'''
class BackTracking:

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
        backtrack = BackTracking

        # iterate through and send to solve()
        for mtrx in difficulty:
            currentMatrix = backtrack.solve(mtrx)



    # solve() takes a matrix from matrixSelection and solves it by recursively backtracking if encountering an obstacle 
    @staticmethod
    def solve(mtrx):
        backtrack = BackTracking
        puzzle = PuzzleReader
        check = SolutionChecker

        #currentLocation starts at first cell, then finds next empty cell
        currentLocation = [0,0]
        currentLocation = backtrack.nextCell(mtrx, currentLocation)

        # if currentLocation is checked and contains False because nextCell couldn't find anything, game complete
        if not currentLocation:
            print("No cells left", "Number of decisions made: " + str(backtrack.decisionCount), "Number of backtracks: " + str(backtrack.numBacks), sep = "\n")
            return True

        # iterate through all possible values while checking through SolutionChecker
        for i in range(1,10):
            # if current location and value is valid across row, column, and box.. place the value in cell
            if check.is_valid_cell(i, currentLocation[0], currentLocation[1], mtrx):
                mtrx[currentLocation[0],currentLocation[1]] = i
                # +1 decisionCount when placing a number
                backtrack.decisionCount += 1
                # printing each placement (will be deleted for final turn-in)
                print(puzzle.print_puzzle(mtrx))
                # return true if solve works
                if backtrack.solve(mtrx):
                    return True
                
                # resetting spot to blank if encountering an error
                mtrx[currentLocation[0], currentLocation[1]] = ' '

        # +1 decisionCount when backtracking
        # +1 numBacks when backtracking
        # returns false if need arises to backtrack
        backtrack.decisionCount +=1
        backtrack.numBacks += 1
        print("Backtracking...")
        return False

            


    




