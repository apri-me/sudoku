import json
import numpy as np
from sudoku import solve_sudoku


class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        problem_data = json.loads(problem)
        sudoku = np.array(problem_data['sudoku'])
        solved = solve_sudoku(sudoku)
        output = {
            "sudoku": solved
        }
        return json.dumps(output)
