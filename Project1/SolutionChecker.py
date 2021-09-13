from PuzzleReader import PuzzleReader

''' Contributors: Max Kuttner
----------------------------------------------------------------------------------------------
SolutionChecker() class has two main purposes. 
    1) For any given cell on a sudoku board, decide whether or not an integer n can be placed 
        there without any conflicts. 
    2) Take a completed puzzle called solution (in matrix form), and iterate through the entire
        board to see if the solution has any conflicts to tell if the solution is correct.
----------------------------------------------------------------------------------------------
'''


class SolutionChecker:

    # -------------------------------------------------------------------------------------------
    # The in_row() function checks if integer n is in the matrix at array integer column
    @staticmethod
    def in_row(n, row, matrix):
        for cell in matrix[row]:
            if cell == n:           # if cell equals the checked integer n, then n is in the row
                return True
        return False

    # -------------------------------------------------------------------------------------------
    # The in_column() function checks if integer n is in the matrix at array integer column
    @staticmethod
    def in_column(n, column, matrix):
        for cell in matrix[:, column:column+1]:
            if cell == n:           # if cell equals the checked integer n, then n is in the column
                return True
        return False

    # --------------------------------------------------------------------------------------------
    # The in_box() function checks if integer n is in the sub-matrix at matrix [y1:y1, x1:x2]. It locates
    #   the values for x and y by checking which "grid" they lie in.
    @staticmethod
    def in_box(n, row, column, matrix):

        # Initialize x and y values and grids
        y1 = 0
        y2 = 0
        x1 = 0
        x2 = 0
        grid1, grid2, grid3 = [0, 1, 2], [3, 4, 5], [6, 7, 8]

        # Three if statements for finding row "grid" then three more for column "grid"
        if grid1.count(row) == 1:
            y1, y2 = 0, 3
        if grid2.count(row) == 1:
            y1, y2 = 3, 6
        if grid3.count(row) == 1:
            y1, y2 = 6, 9

        if grid1.count(column) == 1:
            x1, x2 = 0, 3
        if grid2.count(column) == 1:
            x1, x2 = 3, 6
        if grid3.count(column) == 1:
            x1, x2 = 6, 9

        # Once the correct sub-matrix slices have been found, loop to check if n is already in box
        for i in matrix[y1:y2, x1:x2]:
            if n in i:
                return True
        return False

    # --------------------------------------------------------------------------------------------
    # The is_valid_cell() method simply combines the three proceeding methods in_row(), in_column(),
    #   and in_box() to check if n passes those functions, if and only if n is not found in any of
    #   those functions will is_valid_cell() return True.
    @staticmethod
    def is_valid_cell(n, row, column, matrix):
        check = SolutionChecker
        if check.in_row(n, row, matrix):
            return False
        if check.in_column(n, column, matrix):
            return False
        if check.in_box(n, row, column, matrix):
            return False
        return True

    # --------------------------------------------------------------------------------------------
    # The in_box function checks if integer n is in the sub-matrix at matrix [y1:y1, x1:x2]. It locates
    #   the values for x and y by checking which "grid" they lie in.
    @staticmethod
    def is_solved_sudoku(solution):
        test = SolutionChecker
        row_number = 0
        for row in solution:
            for cell in range(0, len(row)):
                temp = row[cell]        # assign current cell value to temporary variable
                row[cell] = 0           # replace current cell value with 0 for checking validity
                if test.is_valid_cell(temp, row_number, cell, solution) is False:   # if false -> not solution
                    print("Not a solution")
                    return False
                row[cell] = temp        # check is passed, value is correct, return temp value to cell
            row_number += 1
        print("Solution found")
        return True                     # if entire board has been iterated, then current matrix is solution


def testing():
    puzzles = PuzzleReader
    easy = puzzles.read_puzzles("easy")

    check = SolutionChecker

    # Print easy boards and format

    # Test solution checker:
    print("test1: real solution")
    check.is_solved_sudoku(easy[4])
    print(puzzles.print_puzzle(easy[4]))

    print("\n\n")

    print("test2: not a real solution")
    check.is_solved_sudoku(easy[5])
    print(puzzles.print_puzzle(easy[5]))


testing()
