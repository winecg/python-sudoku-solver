import copy

from collections import deque
from flask import Flask, render_template, request
from typing import List

from sudoku_constraints9x9 import constraint9x9

app = Flask(__name__)

# Part 1
# CSP class that has a dictionary of variables and a ditionary of constraints
class CSP:
    def __init__(self, puzzle: List[List[int]], constraints: dict):
        self.variables = {}
        self.constraints = constraints
        self.size = len(puzzle)
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                label = f'C{i}{j}'
                value = puzzle[i - 1][j - 1]
                if value is not None:
                    self.variables[label] = [value]
                else:
                    self.variables[label] = list(range(1, self.size + 1))

# variables and constraints for a 4x4 puzzle
variables = {'C11': [1],
             'C12': [1, 2, 3, 4],
             'C13': [1, 2, 3, 4],
             'C14': [1, 2, 3, 4],
             'C21': [1, 2, 3, 4],
             'C22': [2],
             'C23': [1, 2, 3, 4],
             'C24': [1, 2, 3, 4],
             'C31': [1, 2, 3, 4],
             'C32': [1, 2, 3, 4],
             'C33': [3],
             'C34': [1, 2, 3, 4],
             'C41': [1, 2, 3, 4],
             'C42': [1, 2, 3, 4],
             'C43': [1, 2, 3, 4],
             'C44': [4]}

constraints4x4 = {('C11', 'C12'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C13'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C14'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C21'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C22'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C31'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C11', 'C41'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C13'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C14'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C21'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C22'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C32'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C12', 'C42'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C13', 'C14'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C13', 'C23'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C13', 'C24'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C13', 'C33'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C13', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C14', 'C23'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C14', 'C24'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C14', 'C34'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C14', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C21', 'C22'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C21', 'C23'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C21', 'C24'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C21', 'C31'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C21', 'C41'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C22', 'C23'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C22', 'C24'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C22', 'C32'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C22', 'C42'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C23', 'C24'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C23', 'C33'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C23', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C24', 'C34'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C24', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C31', 'C32'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C31', 'C33'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C31', 'C34'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C31', 'C41'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C31', 'C42'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C32', 'C33'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C32', 'C34'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C32', 'C41'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C32', 'C42'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C33', 'C34'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C33', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C33', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C34', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C34', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C41', 'C42'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C41', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C41', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C42', 'C43'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C42', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]],
                    ('C43', 'C44'): [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]]}

# Part 2
def revise(csp: CSP, var1: str, var2: str):
    # initializes variables for if the csp was revised, the domains of var1 and var2, and the constraints of the csp
    revised = False
    domain_var1 = csp.variables[var1][:]
    domain_var2 = csp.variables[var2][:]
    constraints = csp.constraints

    # finds constraints involving var1 and var2
    relevant_constraints = []

    # adds constraints to the list bidirectionally since constraints are only defined one way
    if (var1, var2) in constraints:
        relevant_constraints = constraints[(var1, var2)]
    elif (var2, var1) in constraints:
        relevant_constraints = constraints[(var2, var1)]
    else:
        return revised, csp

    # sets consistent to false and loops through the domain of var1
    for value1 in domain_var1[:]:
        consistent = False
        for value2 in domain_var2:
            # checks if [value1, value2] satisfies any constraint between var1 and var2
            if [value1, value2] in relevant_constraints:
                consistent = True
                break
        # if no compatible value in var2's domain is found for var1, remove value1 from var1's domain
        if not consistent:
            domain_var1.remove(value1)
            revised = True

    # edits the domain of var1 in the csp after the revision
    csp.variables[var1] = domain_var1
    return revised, csp

# Part 3
def ac3(csp: CSP):
    # creates a queue of all the arcs
    queue = deque()
    for (var1, var2) in csp.constraints:
        queue.append((var1, var2))
        queue.append((var2, var1))

    # while the queue is not empty, pop an arc and revise the csp
    while queue:
        (xi, xj) = queue.popleft()
        revised, csp = revise(csp, xi, xj)
        if revised:
            # if all values for a domain were removed, return false
            if len(csp.variables[xi]) == 0:
                return False, csp
            # if the csp was revised, push all neighbors of the current arc to the queue
            for xk in csp.variables:
                if xk != xi and ((xk, xi) in csp.constraints or (xi, xk) in csp.constraints):
                    queue.append((xk, xi))
    return True, csp

# Part 4
def minimum_remaining_values(csp: CSP):
    # creates a list of all the unassigned variables in the csp
    unassigned_variables = [var for var in csp.variables.keys() if len(csp.variables[var]) > 1]
    if not unassigned_variables:
        return None
    
    # initially sets the minimum to the first variable in the list and keeps track of its domain size
    min_var = unassigned_variables[0]
    min_domain_size = len(csp.variables[min_var])
    
    # loops through the unassigned variables to find the minimum
    for var in unassigned_variables:
        if len(csp.variables[var]) < min_domain_size:
            min_var = var
            min_domain_size = len(csp.variables[var])

    # returns the name of the variables with the minimum remaining values
    print("Minimum remaining values variable:", min_var)
    return min_var

# Part 5
def backtracking_search(csp: CSP):
    # creates lists for the assignment order and remaining domains
    assignment_order = []
    remaining_domains = []

    # calls the ac3 function to maintain arc consistency
    consistent, csp = ac3(csp)
    app.logger.info(consistent)
    
    # if the puzzle is not consistent, it does not have a solution
    if not consistent:
        return False, {}, [], []

    # makes a list of all squares with more than 1 value in their domain
    for var in csp.variables.keys():
        if len(csp.variables[var]) > 1:
            remaining_domains.append(var)

    # runs the backtracking algorithm
    return backtrack(csp, assignment_order, remaining_domains)

def backtrack(csp: CSP, assignment_order, remaining_domains):
    # if there are no more remaining domains, the puzzle is solved
    if len(remaining_domains) == 0:
        return True, csp.variables, assignment_order, remaining_domains
    
    # calls minimum_remaining_values and removes it from the list of remaining domains
    var = minimum_remaining_values(csp)
    remaining_domains.remove(var)

    # saves the original domain in case it needs to be reverted
    original_domain = csp.variables[var][:]
    app.logger.info(original_domain)

    app.logger.info(var)
    app.logger.info(remaining_domains)

    # test each value in the variable's domain
    for value in original_domain:
        assignment_order.append((var, value))
        csp.variables[var] = [value]

        app.logger.info(value)
        app.logger.info(assignment_order)

        # check if the csp is consistent after assigning the value
        csp_copy = copy.deepcopy(csp)
        consistent, _ = ac3(csp_copy)
        print(consistent)

        # if it is consistent, recursively call the backtrack function to assign more values
        if consistent:
            result, _, _, _ = backtrack(csp, assignment_order, remaining_domains)

            # if the puzzle is solved, return True
            if result:
                return True, csp.variables, assignment_order, remaining_domains
            
        # pop last assignment from assignment order and revert var to its original domain if it isn't consistent
        assignment_order.pop()
        csp.variables[var] = original_domain 

    remaining_domains.append(var)
    return False, {}, [], []

# Part 6
def parse_puzzle(query):
    # finds the size of each row based on the query
    size = int(len(query) ** 0.5)

    # goes through every character in the query and adds it to the puzzle list
    puzzle = []
    for row in range(size):
        row_list = []
        for col in range(size):
            cell = query[row * size + col]

            # if the cell is 0, meaning an empty cell, append None instead of 0, else just add the number
            if cell == '0':
                row_list.append(None)
            else:
                row_list.append(int(cell))
        puzzle.append(row_list)
    return puzzle, size

@app.route('/solve_sudoku') 
def solve_sudoku():
    # gets the puzzle query from the website URL
    query = request.args.get('puzzle', '')

    # converts the query to a list
    puzzle, size = parse_puzzle(query)
    app.logger.info(puzzle)

    # determines which constraints to use based on the size of the puzzle
    constraint_size = 9
    size = int(size) ** 0.5
    if size == 2:
        constraint_size = 4
    constraints = constraint9x9
    if constraint_size == 4:
        constraints = constraints4x4

    # creates a CSP and runs the backtracking search algorithm
    csp = CSP(puzzle, constraints)
    solved, solution, assignment_order, _ = backtracking_search(csp)

    app.logger.info(solved)
    app.logger.info(assignment_order)

    # if the puzzle was solved, render the website
    if solved:
        return render_template('index.html', puzzle=puzzle, size=size, solution=solution)
    else:
        return "puzzle unsolvable! bwa!"

if __name__ == '__main__':
    app.run(debug=True)