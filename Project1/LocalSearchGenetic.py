from PuzzleReader import PuzzleReader
from SolutionChecker import SolutionChecker
import random as random
import numpy as np
from copy import deepcopy

''' Contributors: Max Kuttner
----------------------------------------------------------------------------------------------
LocalSearchGenetic()
    This class uses a genetic local search algorithm with tournament seleciton and a 
        fitness_function(). It solves a sudoku board by crossing over data from two parent 
        boards and randomly mutating cells from a handful of the child boards. It creates new
        boards until there are no conflicts and a solution is found. 
----------------------------------------------------------------------------------------------
'''


class LocalSearchGenetic:

    def __init__(self, decisions, original, board, fitness, conflicts):
        self.decisions = decisions
        self.original = original
        self.board = board
        self.fitness = fitness
        self.conflicts = conflicts

    # -------------------------------------------------------------------------------------------
    # Hill_climbing() will choose non-original cells at random and loop through possible values
    #   1 - 9. It will do this to the board until it cannot find a value for the current cell.
    #   At which point it will return the board.
    @staticmethod
    def hill_climbing(board, original):
        check = SolutionChecker
        backtracking = False
        while not backtracking:
            y = random.randint(0, 8)
            x = random.randint(0, 8)
            if original[y:y+1, x:x+1] == " ":
                for n in range(0, 9):
                    if check.is_valid_cell(n+1, y, x, board):
                        board[y:y + 1, x:x + 1] = n+1
                        break
                    elif n == 8:
                        backtracking = True
                        for row in board:
                            for cell in range(0, len(row)):
                                if row[cell] == " ":
                                    row[cell] = random.randint(1, 9)
        return board

    # -------------------------------------------------------------------------------------------
    # Loops through every row, column and box within the board, counting the total conflicts or
    #   repeated numbers. Then it returns the conflicts for the given board.
    @staticmethod
    def conflict_counter(board):
        conflicts = 0
        for row in board:                       # conflicts in each row
            temp = row
            conflicts += 9 - len(set(temp))
        for column in range(0, 9):              # conflicts in each column
            temp = []
            for cell in board[:, column:column + 1]:
                temp = np.concatenate((temp, cell), axis=0)
            conflicts += 9 - len(set(temp))
        x = [0, 3, 6, 9]
        for n in range(0, 3):
            for i in range(0, 3):
                temp = []
                for cell in board[x[n]: x[n+1], x[i]: x[i+1]]:  # iterates each cell in box, for each box on the board
                    temp = np.concatenate((temp, cell), axis=0)
                conflicts += 9 - len(set(temp))
        return conflicts

    # -------------------------------------------------------------------------------------------
    # Iterates through population and updates the number of conflicts on each board.
    @staticmethod
    def update_conflicts(population):
        for board in population:
            board.set_conflicts(LocalSearchGenetic.conflict_counter(board.get_board()))

    # -------------------------------------------------------------------------------------------
    # Boolean function that returns true if a solution is found within the population
    @staticmethod
    def solution_found(population):
        for board in population:
            if board.get_conflicts() == 0:
                return True
        return False

    # -------------------------------------------------------------------------------------------
    # Returns the solution board that has 0 conflicts.
    @staticmethod
    def solution(population):
        for board in population:
            if board.get_conflicts() == 0:
                return board

    # -------------------------------------------------------------------------------------------
    # First method used to initialize the population. It will create a list with number of boards
    #   in size, run a hill-climb on each one, then check their conflicts. Then it will create an
    #   instance of the LocalSearchGenetic class for each. This function returns a list of boards.
    @staticmethod
    def initialize_population(size, original):
        init = LocalSearchGenetic
        population = []
        for i in range(0, size):
            temp = np.ndarray.copy(original)
            chromosome = init.hill_climbing(temp, original)
            conflicts = init.conflict_counter(chromosome)
            individual = LocalSearchGenetic(0, original, chromosome, 0,  conflicts)
            population.append(individual)
        return population

    # -------------------------------------------------------------------------------------------
    # Fitness_function() assigns a float to each board based on its number of conflicts, or distance
    #   from the solution. It does this by first taking f(x) / Sum(f(x)) in the first three for loops.
    #   Then it sorts the population by fitness with the lambda function. Next takes that fitness value and
    #   places it into the equation P(1-P)^i and that value is multiplied by 100. This equation is used to
    #   "weight" better solutions more heavily.
    @staticmethod
    def fitness_function(population):
        fitness_total = 0
        adj_total = 0
        for board in population:
            fitness_total += board.get_conflicts()
            board.set_fitness(1 / (board.get_conflicts()))
        for board in population:
            adj_total += fitness_total * board.get_fitness()
            board.set_fitness(fitness_total * board.get_fitness())
        for board in population:
            temp = (board.get_fitness() / adj_total) * 100
            board.set_fitness(round(temp, 2))
        population.sort(key=lambda x: LocalSearchGenetic.get_fitness(x), reverse=True)  # sort population by fitness
        i = 0
        for board in population:
            p = board.get_fitness()
            board.set_fitness((p * ((1 - p) ** i)) * 100)           # give better solutions higher probability or weight
            i += 1
        return population

    # -------------------------------------------------------------------------------------------
    # Tournament_selection() returns the winners or selected chromosomes from the old_population
    #   of boards. It does this by doing a weighted selection from list of each board's fitness value
    #   Then it will check each board's fitness value with the list of selections, adding the matching boards
    #   to a list called winners, that will be returned at the end.
    @staticmethod
    def tournament_selection(old_population):
        winners = []
        weight = []
        for board in old_population:
            weight.append(board.get_fitness())
        choices = random.choices(weight, weights=weight, k=len(old_population))     # weighted selection
        for choice in choices:
            for board in old_population:
                if board.get_fitness() == choice:
                    winners.append(board)
                    break
        return winners

    # -------------------------------------------------------------------------------------------
    # The cross_over() method operated on the parent or old_population, creating children from it.
    #   it takes two random boards from parents, chooses a random spot, checks if it was a number
    #   from the original board, and swaps it with the second board.
    @staticmethod
    def cross_over(number_crossovers, original_puzzle, parents):
        children = []
        while len(parents) != 0:
            n = random.randint(0, len(parents)-1)   # random board integer index from parents list
            p1 = deepcopy(parents[n])               # copies selected board from parents list
            parents.remove(parents[n])              # removes selected board from parents list
            n = random.randint(0, len(parents)-1)   # repeat for board 2
            p2 = deepcopy(parents[n])
            parents.remove(parents[n])
            crossed_and_original = deepcopy(original_puzzle)
            changed = 0
            while number_crossovers != changed:
                y = random.randint(0, 8)
                x = random.randint(0, 8)
                if crossed_and_original[y:y + 1, x:x + 1] == " ":       # swap board 1 cell with board 2 cell
                    temp = int(p2.get_board()[y:y + 1, x:x + 1])
                    p2.get_board()[y:y + 1, x:x + 1] = int(p1.get_board()[y:y + 1, x:x + 1])
                    p1.get_board()[y:y + 1, x:x + 1] = temp
                    crossed_and_original[y:y + 1, x:x + 1] = p1.get_board()[y:y + 1, x:x + 1]
                    changed += 1
            p1.set_decisions(number_crossovers)
            p2.set_decisions(number_crossovers)
            children.append(p1)
            children.append(p2)
        return children

    # -------------------------------------------------------------------------------------------
    # Takes each board in new generation and will randomly change a user defined number_mutations.
    #   It does this by choosing a random "grid" or box on the board and changing a random non-
    #   original value.
    @staticmethod
    def mutate(mutation_rate, number_mutations, original_puzzle, children):
        for c in children:
            if random.randint(1, mutation_rate) == 1:
                num_changed = 0
                changed_cell = deepcopy(original_puzzle)
                while num_changed != number_mutations:
                    grids = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
                    x = random.choice(grids)
                    y = random.choice(grids)
                    n = random.randint(x[0], x[2])              # random x integer from grid
                    i = random.randint(y[0], y[2])              # random y integer from grid
                    if changed_cell[n: n + 1, i: i + 1] == " ":     # assert selection is not from original or changed
                        temp = random.randint(1, 9)
                        if temp == c.get_board()[n: n + 1, i: i + 1]:
                            continue
                        c.get_board()[n: n + 1, i: i + 1] = temp
                        changed_cell[n: n + 1, i: i + 1] = temp
                        num_changed += 1
                c.set_decisions(number_mutations)

    # -------------------------------------------------------------------------------------------
    # This is where the aforementioned functions are combined with a simple while loop, and a
    #   an if statement to check if a solution has been found. The algorithm will initialize a
    #   user defined number of boards in population (outside the loop). Then in each iteration
    #   of the while loop it 1. checks if solution is found 2. if not found then run these functions
    #   fitness_function(), tournament_selection(), crossover(), mutate(), and update_conflicts().
    @staticmethod
    def genetic_search(population_size, original_puzzle):
        lsg = LocalSearchGenetic
        population = lsg.initialize_population(population_size, original_puzzle)
        old_conflicts = 100
        solved = False
        while not solved:
            conflicts = population[random.randint(0, len(population) - 1)].get_conflicts()
            if conflicts < old_conflicts:
                print(conflicts)
                old_conflicts = conflicts
            if lsg.solution_found(population):
                return lsg.solution(population)
            old_population = lsg.fitness_function(population)
            parents = lsg.tournament_selection(old_population)
            children = lsg.cross_over(5, original_puzzle, parents)
            lsg.mutate(2, 1, original_puzzle, children)
            population = children
            lsg.update_conflicts(population)

    # -------------------------------------------------------------------------------------------
    # The remaining class functions below serve as the setter and getter functions for all of the
    #   class instances.
    def get_decisions(self):
        return self.decisions

    def get_original(self):
        return self.original

    def get_board(self):
        return self.board

    def get_fitness(self):
        return self.fitness

    def get_conflicts(self):
        return self.conflicts

    def set_decisions(self, decisions):
        self.decisions += decisions

    def set_original(self, original):
        self.original = original

    def set_board(self, board):
        self.board = board

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_conflicts(self, conflicts):
        self.conflicts = conflicts


def testing():
    puzzles = PuzzleReader
    easy = puzzles.read_puzzles("easy")
    original = easy[0]

    test = LocalSearchGenetic
    solved = test.genetic_search(8, original)
    print(PuzzleReader.print_puzzle(solved.get_board()))
    print(solved.get_decisions())


testing()
