import random
import numpy as np
import pandas as pd
from PuzzleReader import PuzzleReader
from SolutionChecker import SolutionChecker
from collections import Counter


''' Contributors: Alyse Mize
----------------------------------------------------------------------------------------------
LocalSearch() will use simulated annealing to find a solution to a puzzle. 
----------------------------------------------------------------------------------------------
'''

class LocalSearch:

    
    @staticmethod
    def assignRandomValues(puzzle):
        f = np.array(puzzle)
        for array in f:
            for i in range(0, len(array)):
                rand = random.randint(1, 9)
                if array[i] == " ":
                    array[i] = rand
        return f


    @staticmethod
    def countConflict(new_puzzle):
        f = np.array(new_puzzle)
        count = 0
        df = pd.DataFrame(data = new_puzzle)
        for array in f:
            count += len(array) - len(set(array))   #this returns the row conflicts
    
        df1 = df.apply(lambda y:sum(y.duplicated()))    #This returns the column conflicts

        count += df1.sum()
        if count == 0:
            check_solution(new_puzzle)
        return count


    @staticmethod
    def check_solution(new_puzzle):
        check = SolutionChecker
        printer = PuzzleReader
        if check.is_solved_sudoku(new_puzzle)is True:
            print("is solution")
            print(printer.print_puzzle(new_puzzle))
            return True
        return False

    

    @staticmethod
    def chooseConflicts(new_puzzle, original_puzzle):
        puzzles = PuzzleReader
        new = np.array(new_puzzle)
        ori = np.copy(original_puzzle)
        changed_puzzle = np.copy(new)
        grids = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        x = random.choice(grids)
        y = random.choice(grids)
        first_node = 0
        second_node = 0
        while first_node == 0:
            n = random.randint(x[0], x[2])              # random x integer from grid
            i = random.randint(y[0], y[2])              # random y integer from grid
            if ori[n: n + 1, i: i + 1] == " ":     # assert selection is not from original or changed
                first_node = new[n: n + 1, i: i + 1]
                
        while second_node == 0:
            k = random.randint(x[0], x[2])              # random x integer from grid
            t = random.randint(y[0], y[2])              # random y integer from grid
            if ori[k: k + 1, t: t + 1] == " ":     # assert selection is not from original or changed
                second_node = new[k: k + 1, t: t + 1]
                
        for array in changed_puzzle:
            for m in range(0, len(array)):
                if array[m] == changed_puzzle[k: k + 1, t: t + 1]:
                    array[m] = int(first_node)
        for array in changed_puzzle:
            for m in range(0, len(array)):
                if array[m] == changed_puzzle[n: n + 1, i: i + 1]:
                    array[m] = int(second_node)
        return changed_puzzle
        
    @staticmethod            
    def simulated_Anneal(original, temp):
        ls = LocalSearch
        original_puzzle = np.copy(original)
        solved = False

        while not solved:
            coolTemp = .99
            

            newPuzzle = ls.assignRandomValues(original_puzzle[5])
            print(puzzles.print_puzzle(newPuzzle))
            old_conflicts = ls.countConflict(newPuzzle)
            print("number of starting conflicts " + start_conflicts)

            switch = ls.chooseConflicts(new_puzzle, puzzle)
            new_conflicts = ls.countConflict(switch)
            if new_conflicts < old_conflicts:
                print(new_conflicts)
                old_conflicts = new_conflicts
            
def testing():
    puzzles = PuzzleReader
    puzzle = puzzles.read_puzzles("easy")
    print(puzzles.print_puzzle(puzzle[5]))
    original = puzzle[5]
    search = LocalSearch
    
    solved = search.simulated_Anneal(original, 100)
    print(puzzles.print_puzzle(solved))
    print(solved.get_decisions())


testing()
