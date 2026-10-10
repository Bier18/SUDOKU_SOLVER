import Grid

class Solver:

    def __init__(self):
        self.solver_grid = [[[] for _ in range(9)] for _ in range(9)]
        self.input_sudoku = Grid.Grid()

    # controlla se un numero compare su una riga
    def is_number_in_row(self, number, row_index) -> bool :
        return number in self.input_sudoku.grid[row_index]

    # controlla se un numero compare su una colonna
    def is_number_in_column(self, number, column_index) -> bool :
        column = [ self.input_sudoku.grid[row_index][column_index] for row_index in range(9)]
        return number in column

    # controlla se un numero è presente in una sottogriglia
    def is_number_in_subgrid(self,number,row,column) -> bool:
        row_index = (row // 3) * 3
        column_index = (column // 3) * 3

        for i in range(row_index, row_index+3):
            for j in range(column_index, column_index+3):
                if self.input_sudoku.grid[i][j] == number:
                    return True
        return False

    # valuta i possibili candidati
    def check_guess(self):

        row = 0
        column = 0
        guess = 1

        # cerca i potenziali numeri validi nella griglia
        while guess < 10:

            # se la cella è vuota
            if self.input_sudoku.grid[row][column] == 0:
                # controlla la riga
                is_number_in_row = self.is_number_in_row(guess, row)
                # controlla la colonna
                is_number_in_column = self.is_number_in_column(guess,column)

                # se un numero non compare lo salva come potenziale candidato
                if not is_number_in_row and not is_number_in_column:

                    self.solver_grid[row][column].append(guess)

            # se ho finito le colonne
            if column == 8:
                # resetta l'indice e avanza la riga
                column = 0
                row += 1
            else:
                column += 1

            # se ho finito la griglia
            if row == 9:
                # prova il numero successivo e resetta gli indici
                row = 0
                column = 0
                guess += 1

    # elimina i numeri presenti nella sottogriglia
    def reduce_grid(self) -> bool :
        reduced = False
        row = 0
        column = 0

        while row < 9:
            # se ho dei potenziali candidati
            if len( self.solver_grid[row][column] ) > 0:
                # controlla la presenza nella sottogriglia
                for guess in self.solver_grid[row][column]:
                    # se il numero è presente
                    if self.is_number_in_subgrid(guess,row,column) or self.is_number_in_column(guess,column) or self.is_number_in_row(guess,row):
                        # lo rimuove
                        self.solver_grid[row][column].remove(guess)

                        # aggiorna il flag
                        if not reduced:
                            reduced = True

            # se ho finito le colonne
            if column == 8:
                # resetta l'indice e avanza la riga
                column = 0
                row += 1
            else:
                column += 1

        return reduced

    # aggiorna la griglia
    def update_grid(self):
        row = 0
        column = 0

        while row < 9:
            if len( self.solver_grid[row][column] ) == 1:
                solution = self.solver_grid[row][column][0]
                self.input_sudoku.update_cell(solution,row,column)

            # se ho finito le colonne
            if column == 8:
                # resetta l'indice e avanza la riga
                column = 0
                row += 1
            else:
                column += 1

    # risolve il sudoku
    def solve(self):

        # carica la griglia da file
        self.input_sudoku.load_grid()

        # trova le possibili soluzioni
        self.check_guess()

        i_can_reduce = True

        # riduce la griglia finchè è possibile
        while i_can_reduce:

            i_can_reduce = self.reduce_grid()

            # aggiorna la griglia
            self.update_grid()

        # controlla se il sudoku è effettivamente risolto
        solved = True

        for row in self.input_sudoku.grid:
            solved = not 0 in row

        if solved:
            # mostra il risultato
            self.input_sudoku.print_grid()
        else:
            self.solver_tree()

    # genera un albero di tentativi per risolvere il sudoku
    def solver_tree(self):
        print(self.solver_grid[1][4])

        index = 0
        attempt = 0
        last_attempt_list = []
        num_iteration = 0

        # itera su tutta la griglia
        while index < 81:
            row = index // 9
            column = index % 9

            # se ho dei numeri possibili
            if len(self.solver_grid[row][column]) > 0:

                if  attempt < len(self.solver_grid[row][column]):

                    # salva il tentativo
                    last_attempt_list.append(attempt)
                    guess = self.solver_grid[row][column][attempt]

                    # e se il numero è valido nella configurazione corrente
                    if ( not self.is_number_in_row(guess,row) and
                         not self.is_number_in_column(guess,column) and
                         not self.is_number_in_subgrid(guess,row,column) ):

                        # aggiorna la griglia
                        self.input_sudoku.update_cell(guess,row,column)

                        # resetta attempt
                        attempt = 0
                    else:
                        # se ho ancora numeri li provo sulla stessa cella
                        attempt += 1
                        index -= 1
                else:
                    # torno indietro e provo un'altra guess e rimuovo la soluzione dalla griglia
                    attempt = last_attempt_list.pop() + 1
                    self.input_sudoku.update_cell(0,row,column)
                    index -= 2


            index += 1
            num_iteration += 1

            if num_iteration == 1000000:
                self.input_sudoku.print_grid()
                num_iteration = 0













