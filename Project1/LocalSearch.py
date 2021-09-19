import random
import numpy as np
import pandas as pd
from PuzzleReader import PuzzleReader
from collections import Counter


''' Contributors: Alyse Mize
----------------------------------------------------------------------------------------------
LocalSearch() will use simulated annealing to find a solution to a puzzle. 
----------------------------------------------------------------------------------------------
'''

class LocalSearch:

'''
The assignRandomValues() method will take the data from puzzle reader which should put everything
into its own array.  It will then make everything into a numpy array and check to see if
there are any blank spots which it will then fill with a random number of 1-9.
'''
    @staticmethod
    def assignRandomValues(puzzle):
        f = np.array(puzzle)
        for array in f:
            for i in range(0, len(array)):
                    rand = random.randint(1, 9)     #checks the element if its " " if yes it gets replaced
                    if array[i] == " ":             
                        array[i] = rand
        return f

'''
countConflict() takes the sudoku puzzle and puts it into a data frame.  It then counts
each row for conflicts and adds that to the column conflicts which is returned with count.
'''
    @staticmethod
    def countConflict(puzzle):
        f = np.array(puzzle)
        count = 0
        df = pd.DataFrame(data = puzzle)
        for array in f:
            count += len(array) - len(set(array))   #this returns the row conflicts
            #print("amount of conflicts in array " + str(array) + str(count))
        df1 = df.apply(lambda y:sum(y.duplicated()))    #This returns the column conflicts
        #print(df1)
        count += df1.sum() 
        return count

'''
This is just to help with testing the code, once the code is finished we should cut it
and only use sudoku solver.
'''
def testing():
    puzzles = PuzzleReader
    puzzle = puzzles.read_puzzles("easy")

    search = LocalSearch

    print(puzzles.print_puzzle(puzzle[5]))

    newPuzzle = search.assignRandomValues(puzzle[5])
    print(puzzles.print_puzzle(newPuzzle))
    count = search.countConflict(newPuzzle)
    print("number of conflicts" + count)

testing()
