from PuzzleReader import PuzzleReader
from SolutionChecker import SolutionChecker
from BackTracking import BackTracking
from BackTrackForwardChecking import BackTrackForwardChecking
from BackTrackingArcConsistency import BackTrackingArcConsistency

''' Contributors: Derek Logan
----------------------------------------------------------------------------------------------
SudokuSolver() class has one main purpose. 
    1) 'Main' file for program. Classes will be instantiated and run. No unique functions or 
        data. Code is arranged in a comprehensive manner. 
----------------------------------------------------------------------------------------------
'''

def main():
    puzzles = PuzzleReader 
    back = BackTracking
    backF = BackTrackForwardChecking
    backA = BackTrackingArcConsistency
    easy = puzzles.read_puzzles("easy")
    medium = puzzles.read_puzzles("medium")
    hard = puzzles.read_puzzles("hard")
    evil = puzzles.read_puzzles("evil")
    # print(easy[4]) # delete eventually, only allows to see what puzzles look like in matrix

    check = SolutionChecker


    #back.matrixSelection(medium)
    #backF.matrixSelection(easy)
    #backF.obtainDomain(easy[0])
    #back.matrixSelection(easy)
    #backF.matrixSelection(easy)

    backA.matrixSelection(easy)
    



main()