import time
import Grid
from ErrorTypes import *


class Solver:

    K_MAX_NUMBER_OF_OCCURRENCIES = 1
    K_MIN_INPUT_NUMBER           = 17

    def __init__(self):
        self.solver_grid = [[[] for _ in range(9)] for _ in range(9)]
        self.input_sudoku = Grid.Grid()
        self.guess_list = []

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

    # risolve il sudoku
    def solve(self):

        # carica la griglia da file
        ret_code = self.input_sudoku.load_grid()

        if ret_code != GridError.OK:
            ret_code =  SolverError.ERROR_IN_LOADING_GRID

        else:

            ret_code = self.check_input_grid()


            if ret_code == SolverError.OK:

                start = time.perf_counter()

                # trova tutte le possibili soluzioni
                self.fill_guess_list()

                # ordina la lista di possibili soluzioni in base al numero delle stesse
                self.guess_list.sort(key=lambda x: x[-1])

                # risolve il sudoku
                self.backtracking_solver()

                # stampa la soluzione
                self.input_sudoku.print_grid()

                end = time.perf_counter()

                print(f'TEMPO NECESSARIO PER LA SOLUZIONE = {end - start} s')

        return ret_code

    # spiega gli errori
    def get_error_description(self, error):

        match error:

            case SolverError.ERROR_IN_LOADING_GRID:
                return "Errore nel caricamento della griglia"

            case SolverError.ERROR_REPEATED_NUMBER_IN_ROW:
                return "Griglia non valida, numero ripetuto in riga"

            case SolverError.ERROR_REPEATED_NUMBER_IN_COLUMN:
                return "Griglia non valida, numero ripetuto in colonna"

            case SolverError.ERROR_REPEATED_NUMBER_IN_SUBGRID:
                return "Griglia non valida, numero ripetuto nella sottogriglia"

            case SolverError.ERROR_TOO_FEW_NUMBER_IN_INPUT:
                return "Griglia non valida, numero di indizi non sufficiente a risolvere univocamente il puzzle"

            case _:
                return "Errore sconosciuto"

    # controlla se la griglia in input è valida
    def check_input_grid(self):
        valid_input_number = 0
        for i in range(9):
            for j in range(9):
                # se la griglia contiene un elemento valido
                number = self.input_sudoku.grid[i][j]
                if not  number == 0:
                    valid_input_number += 1

                    # estrae la riga e la colonna
                    row = self.input_sudoku.grid[i]
                    column = [self.input_sudoku.grid[row_index][j] for row_index in range(9)]

                    # controlla la sottogriglia
                    subgrid_row_index = (i // 3) * 3
                    subgrid_column_index = (j // 3) * 3
                    for sgrid_row_index in range(subgrid_row_index, subgrid_row_index+3):
                        for sgrid_column_index in range(subgrid_column_index, subgrid_column_index+3):
                            # se trova il numero esce
                            if ( (not sgrid_row_index == i or
                                not sgrid_column_index == j )
                                and number == self.input_sudoku.grid[sgrid_row_index][sgrid_column_index]):
                                return SolverError.ERROR_REPEATED_NUMBER_IN_SUBGRID

                    # se il numero è ripetuto più volte nella stessa riga
                    if row.count(number) > Solver.K_MAX_NUMBER_OF_OCCURRENCIES:
                        # segnala l'errore
                        return SolverError.ERROR_REPEATED_NUMBER_IN_ROW

                    # se il numero è ripetuto più volte nella stessa colonna
                    if column.count(number) > Solver.K_MAX_NUMBER_OF_OCCURRENCIES:
                        # segnala l'errore
                        return SolverError.ERROR_REPEATED_NUMBER_IN_COLUMN

        # controlla se ci sono abbastanza indizi
        if valid_input_number < Solver.K_MIN_INPUT_NUMBER:
            return SolverError.ERROR_TOO_FEW_NUMBER_IN_INPUT

        return SolverError.OK

    # genera un albero di tentativi per risolvere il sudoku
    def backtracking_solver(self):
        # inizializza la variabile per risalire al numero
        number_to_try = 1
        i = 0
        last_number_list = [0 for _ in range(len(self.guess_list))]
        # itera su tutte le guess
        while i < len( self.guess_list ):
            guess = self.guess_list[i]

            # recupera il numero usato come maschera, la riga e la colonna
            mask = guess[0]
            row = guess[1]
            column = guess[2]


            while mask & ( 1 << (number_to_try - 1)) == 0 and number_to_try < 10:
                # aggiorna il numero da trovare
                number_to_try += 1

            # se ho esaurito le possibilità
            if number_to_try == 10:

                # torna indietro
                number_to_try = last_number_list[i-1] + 1
                last_guess = self.guess_list[i-1]
                last_row = last_guess[1]
                last_column = last_guess[2]
                self.input_sudoku.update_cell(0, last_row, last_column)
                i -= 2
            else:

                # se ha trovato il numero corretto e se il numero è valido
                is_number_in_row = self.is_number_in_row(number_to_try, row)
                is_number_in_column = self.is_number_in_column(number_to_try, column)
                is_number_in_subgrid = self.is_number_in_subgrid(number_to_try,row,column)

                if not is_number_in_row and not is_number_in_column and not is_number_in_subgrid:

                    # aggiorna la griglia
                    self.input_sudoku.update_cell(number_to_try,row,column)

                    # salva la guess e resetta il numero
                    last_number_list[i] = number_to_try
                    number_to_try = 1
                # se non è valido continua sul posto
                else:

                    number_to_try += 1
                    i -= 1

            i += 1

    # verifica le possibilità
    def fill_guess_list( self ):
        cell = 0
        # itera su tutte le celle
        while cell < 81:
            row = cell // 9
            column = cell % 9

            # se la cella è vuota
            if self.input_sudoku.grid[row][column] == 0:

                #inizializza il numero per il masking e il counter delle possibilità
                mask = 0
                num_of_choices = 0

                # controlla la guess
                for guess in range(1,10):
                    is_guess_in_row = self.is_number_in_row(guess,row)
                    is_guess_in_column = self.is_number_in_column(guess,column)
                    is_guess_in_subgrid = self.is_number_in_subgrid(guess,row,column)

                    # se la guess non è in una riga, colonna o sottogriglia
                    if ( not is_guess_in_row    and
                         not is_guess_in_column and
                         not is_guess_in_subgrid ):

                        # salva la griglia usando il bitmasking
                        mask |= 1 << ( guess - 1 )
                        # aggiorna il contatore
                        num_of_choices += 1

                # salva le guess possibili
                self.guess_list.append( (mask, row, column, num_of_choices) )

            cell += 1




