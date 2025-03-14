import random


def display(grid) -> None:
    """
    Print each grid's row

    :param grid: grid to consider
    :return:
    """
    for i in range(9):
        print(grid[i])
    print("\n")


class Sudoku:

    def __init__(self):

        self.base_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.index_grid = [list(range(1, 10)), list(range(10, 19)), list(range(19, 28)), list(range(28, 37)),
                           list(range(37, 46)),
                           list(range(46, 55)), list(range(55, 64)), list(range(64, 73)),
                           list(range(73, 82))]  # matrice des positions

        # number of tries before filling grid
        self.tries = 0

    def euclidian_division(self, numerator: int, denominator: int) -> list:
        """
        Result of the Euclidean division of a by b in the form [q, mod].

        :param numerator: number to divide
        :param denominator: divider used for the division
        :return:
        """
        q = numerator // denominator
        modulo = numerator - q * denominator
        output = [q, modulo]

        return output

    def value_in_bloc(self, bloc_number: int) -> list:
        """
        value of each cell whiting the ith bloc.

        :param bloc_number: bloc index (between 1 and 9)
        :return:
        """
        bloc = []
        q, mod = self.euclidian_division(bloc_number, 3)
        index_grid = self.index_grid[q * 3:q * 3 + 3]
        for i in range(3):
            bloc.append(index_grid[i][mod * 3:mod * 3 + 3])

        return [x for y in bloc for x in y]

    def bloc_index(self, row: int, column: int) -> int:
        """
        Bloc index based on cell row and col value.

        :param row: row index value
        :param column: column index value
        :return:
        """
        a = self.index_grid[row][column]

        for i in range(0, 9):
            if a in self.value_in_bloc(i):
                return i
        # return 0

    def available_bloc_value(self, grid: list, bloc_index: int):
        """
        Available value for a given bloc.

        :param grid: grid to consider
        :param bloc_index: index of bloc
        :return:
        """
        bloc = []
        sol = self.euclidian_division(bloc_index, 3)
        q = sol[0]
        mod = sol[1]
        t = grid[q * 3:q * 3 + 3]

        for i in range(3):
            bloc.append(t[i][mod * 3:mod * 3 + 3])

        val_in_bloc = set([x for y in bloc for x in y if x != 0])
        val_in_bloc = list(val_in_bloc)
        available_value = list(range(1, 10))

        for i in range(len(val_in_bloc)):
            b = val_in_bloc[i]
            del available_value[available_value.index(b)]

        return available_value

    def available_row_value(self, grid: list, row_index: int) -> list:
        """
        Available value for a cell based on a given row.

        :param grid: game grid
        :param row_index: row to consider
        :return:
        """
        val_in_row = []

        for i in range(9):
            if grid[row_index][i] != 0:
                val_in_row.append(grid[row_index][i])

        available_value = list(range(1, 10))

        for val in val_in_row:
            del available_value[available_value.index(val)]

        return available_value

    def available_col_value(self, grid: list, column_index: int) -> list:
        """
        Available value for a cell based on a given column.

        :param grid: game grid
        :param column_index: column to consider
        :return:
        """
        val_in_col = []

        for i in range(9):
            if grid[i][column_index] != 0:
                val_in_col.append(grid[i][column_index])

        l = list(range(1, 10))

        for val in val_in_col:
            del l[l.index(val)]

        return l

    def available_value(self, grid, row_index, column_index):
        """
        Available value for a cell.

        :param grid: game grid
        :param row_index: row to consider
        :param column_index: col to consider
        :return:
        """
        num = self.bloc_index(row_index, column_index)
        l1 = set(self.available_row_value(grid, row_index))
        l2 = set(self.available_col_value(grid, column_index))
        l3 = set(self.available_bloc_value(grid, num))
        l = list(l1 & l2 & l3)

        return l

    def fill(self) -> int:
        """
        Generate a sudoku grid.

        :return: 1 if the grid is created else 0
        """

        self.tries = self.tries + 1
        for i in range(9):
            for j in range(9):

                # avoid max recursion error
                if self.tries == 995:
                    return 0

                elif len(self.available_value(self.base_grid, i, j)) == 0:

                    self.base_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    return self.fill()


                else:
                    # randomly fill the grid
                    rdm = random.choice(self.available_value(self.base_grid, i, j))
                    self.base_grid[i][j] = rdm
                    if (i == 8) and (j == 8):
                        return 1
        return 0

    def n_missing(self, grid: list):
        """
        Number of cell to fill.

        :param grid: game grid
        :return:
        """
        zero = 0
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    zero = zero + 1

        return zero

    def is_solvable(self, grid: list, n_empty: int) -> list | int:
        """
        Try to solve grid to check if it is solvable.

        :param grid:
        :param n_empty:
        :return: grid if is solvable else 0
        """
        acc = 0
        grid_copy = [row[:] for row in grid]
        empty_coordinates = []

        for k in range(n_empty):
            for i in range(9):
                for j in range(9):
                    if grid_copy[i][j] == 0:
                        empty_coordinates.append([i, j])

                        value = self.available_value(grid_copy, i, j)

                        if len(value) == 1:
                            grid_copy[i][j] = value[0]
                            acc = acc + 1
        # if solvable empty filled cells
        if acc == n_empty:
            for k in range(n_empty):
                i = empty_coordinates[k][0]
                j = empty_coordinates[k][1]
                grid_copy[i][j] = 0
            return grid_copy

        return 0

    def resolver(self, grid: list, n_empty: int) -> list | int:
        """
        renvoie 0 si la grille n'est pas résoluble, la grille remplie sinon

        :param grid: grid to consider
        :param n_empty: number of cell to fill
        :return:
        """
        acc = 0
        grid_copy = [row[:] for row in grid]
        empty_coordinates = []

        for k in range(n_empty):
            for i in range(9):
                for j in range(9):
                    if grid_copy[i][j] == 0:
                        empty_coordinates.append([i, j])

                        value = self.available_value(grid_copy, i, j)

                        if len(value) == 1:
                            grid_copy[i][j] = value[0]
                            acc = acc + 1
                            if acc == n_empty:
                                return grid_copy

        return 0

    def xy_position(self, x: int):
        """
        Return x,y coordinates of Xth element of a flatten list[list].

        :param x: index to consider
        :return:
        """

        for i in range(9):
            if x in self.index_grid[i]:

                b = i
                for j in range(9):
                    if x == self.index_grid[b][j]:
                        l = [i, j]

                        return l

        return 0

    def verif(self, grid: list, solution: list):
        """
        Check if user solution is correct

        :param grid: user proposition
        :param solution: solution
        :return:
        """
        grid_copy = [row[:] for row in grid]

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    if solution[i][j] in self.available_value(grid_copy, i, j):
                        grid_copy[i][j] = solution[i][j]
                    else:
                        return 0
        return 1

    def hide_cells(self, n: int):
        """
        Remove randomly n(<57)  cells while keeping the grid solvable.

        :param n: number of cells to hide
        :return: grid with removed value
        """
        # copy grid
        grille = [row[:] for row in self.base_grid]
        hide = 0
        pos = list(range(1, 82))

        while hide != n:

            index_pos = random.choice(pos)
            i, j = self.xy_position(index_pos)
            grille[i][j] = 0
            if self.is_solvable(grille, hide + 1) != 0:
                hide += 1
            else:
                grille[i][j] = self.base_grid[i][j]
            del pos[pos.index(index_pos)]
            if len(pos) == 0:
                hide = n

        return grille

    def sudoku(self) -> list:
        """
        Create a sudoku grid.

        :return: sudoku grid
        """

        x = input('Choose difficulty 1,2,3,4 ou 5\n')
        if x == '1':
            n = random.choice([44, 45, 46])
        elif x == '2':
            n = random.choice([46, 47, 48])
        elif x == '3':
            n = random.choice([48, 49, 50])
        elif x == '4':
            n = random.choice([50, 51, 52, 53, 54])
        else:
            n = random.choice([54, 55, 56])

        while self.fill() != 1:
            self.fill()
        grille = self.hide_cells(n)

        while self.n_missing(grille) != n:
            grille = self.hide_cells(n)

        return grille


if __name__ == "__main__":
    sdk = Sudoku()
    sdk_grid = sdk.sudoku()
    display(sdk_grid)
