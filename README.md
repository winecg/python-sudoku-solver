# Python Sudoku Solver

## Requirements
- Python
- Flask

## Setting Up the Environment
1. **Installation**
- Make sure you have Python already installed
- Install Flask using `pip install flask`

2. **Generating a Puzzle**
- Run `list_to_query.py` to generate a query to use as the puzzle
- There are 5 example puzzles already there for you to convert
- Feel free to make your own in that file

3. **Running the Application**
- Execute the `sudoku_solver.py` script
- In your web browser, go to `https://127.0.0.1:5000/solve_sudoku?puzzle={query}`, replace {query} with the query you generated from `list_to_query.py`
- Once the website loads, you'll see the solution in red if the AC3 algorithm alone was able to solve the puzzle, or you'll be able to walk through each assignment in blue using the Next Step button if it used backtracking
