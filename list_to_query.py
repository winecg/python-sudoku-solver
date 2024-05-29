def list_to_query(list):
    query = ''
    for row in list:
        for cell in row:
            if cell == None:
                query += '0'
            else:
                query += str(cell)
    print(query)

def main():
    puzzle1 = [[7, None, None, 4, None, None, None, 8, 6],
               [None, 5, 1, None, 8, None, 4, None, None],
               [None, 4, None, 3, None, 7, None, 9, None],
               [3, None, 9, None, None, 6, 1, None, None],
               [None, None, None, None, 2, None, None, None, None],
               [None, None, 4, 9, None, None, 7, None, 8],
               [None, 8, None, 1, None, 2, None, 6, None],
               [None, None, 6, None, 5, None, 9, 1, None],
               [2, 1, None, None, None, 3, None, None, 5]]
    puzzle2 = [[1, None, None, 2, None, 3, 8, None, None],
               [None, 8, 2, None, 6, None, 1, None, None],
               [7, None, None, None, None, 1, 6, 4, None],
               [3, None, None, None, 9, 5, None, 2, None],
               [None, 7, None, None, None, None, None, 1, None],
               [None, 9, None, 3, 1, None, None, None, 6],
               [None, 5, 3, 6, None, None, None, None, 1],
               [None, None, 7, None, 2, None, 3, 9, None],
               [None, None, 4, 1, None, 9, None, None, 5]]
    puzzle3 = [[1, None, None, 8, 4, None, None, 5, None],
               [5, None, None, 9, None, None, 8, None, 3],
               [7, None, None, None, 6, None, 1, None, None],
               [None, 1, None, 5, None, 2, None, 3, None],
               [None, 7, 5, None, None, None, 2, 6, None],
               [None, 3, None, 6, None, 9, None, 4, None],
               [None, None, 7, None, 5, None, None, None, 6],
               [4, None, 1, None, None, 6, None, None, 7],
               [None, 6, None, None, 9, 4, None, None, 2]]
    puzzle4 = [[None, None, None, None, 9, None, None, 7, 5],
               [None, None, 1, 2, None, None, None, None, None],
               [None, 7, None, None, None, None, 1, 8, None],
               [3, None, None, 6, None, None, 9, None, None],
               [1, None, None, None, 5, None, None, None, 4],
               [None, None, 6, None, None, 2, None, None, 3],
               [None, 3, 2, None, None, None, None, 4, None],
               [None, None, None, None, None, 6, 5, None, None],
               [7, 9, None, None, 1, None, None, None, None]]
    puzzle5 = [[None, None, None, None, None, 6, None, 8, None],
               [3, None, None, None, None, 2, 7, None, None],
               [7, None, 5, 1, None, None, 6, None, None],
               [None, None, 9, 4, None, None, None, None, None],
               [None, 8, None, None, 9, None, None, 2, None],
               [None, None, None, None, None, 8, 3, None, None],
               [None, None, 4, None, None, 7, 8, None, 5],
               [None, None, 2, 8, None, None, None, None, 6],
               [None, 5, None, 9, None, None, None, None, None]]
    list_to_query(puzzle1)

main()