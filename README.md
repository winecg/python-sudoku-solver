# Python Sudoku Solver

## Requirements
- Python
- Flask

## Setting Up the Environment
1. **Installation**
- Make sure you have Python already installed
- Install Flask using the pip command `pip install Flask`

2. **Generating a Puzzle**
- Run `list_to_query.py` to output a query to use as the puzzle
- There are 5 example puzzles already there for you to convert
- You can also generate your own puzzles using the five provided as an example

3. **Running the Application**
- Execute the `sudoku_solver.py` script
- In your web browser, go to `https://127.0.0.1:5000/solve_sudoku?puzzle={query}`, replacing {query} with the query you generated from `list_to_query.py`
- Once the website loads, you'll see the puzzle's solution in red
