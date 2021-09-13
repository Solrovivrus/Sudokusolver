import os
import numpy as np
import pandas as pd


''' Contributors: Max Kuttner
----------------------------------------------------------------------------------------------
PuzzleReader() job is to first read in puzzles from excel files in its first method and then
    to format a puzzle when given a matrix as a parameter. 
----------------------------------------------------------------------------------------------
'''


class PuzzleReader:

    # --------------------------------------------------------------------------------------------
    # The read_puzzles() method reads sudoku boards from excel files (.csv) and places its values
    #   into a matrix. Takes all files from desired puzzle difficulty level (easy, medium, hard, or evil)
    #   and places returns them in an array. Example: if user wanted all easy puzzles they would
    #   call using read_puzzles("easy"). NOTE: FOLDER PATH WILL BE DIFFERENT FOR EACH USER
    @staticmethod
    def read_puzzles(difficulty):
        folder_path = os.path.join("C:\\Users\Max\PycharmProjects\Project1\puzzles", difficulty)

        puzzles = []
        for file in os.listdir(folder_path):
            data = pd.read_csv(os.path.join(folder_path, file), header=None)
            f = np.array(data)
            for array in f:
                for i in range(0, len(array)):
                    if array[i] != '?':             # if value in cell is not '?', convert to int
                        array[i] = int(array[i])
                        continue
                    array[i] = " "                  # value for empty cells
            puzzles.append(f)
        return puzzles

    # --------------------------------------------------------------------------------------------
    # The print_puzzle() method simply takes the values from puzzle matrix and neatly formats to output
    @staticmethod
    def print_puzzle(puzzle):
        string = "\n"
        for n in range(0, len(puzzle)):
            for i in range(0, len(puzzle)):
                if i == 3 or i == 6:
                    string += " |  " + str(puzzle[n][i]) + " "
                    continue
                elif i == 8:
                    string += " " + str(puzzle[n][i]) + "\n"
                    continue
                else:
                    string += " " + str(puzzle[n][i]) + " "
            if n == 2 or n == 5:
                string += " — — — — — — — — — — — —\n"
        return string
