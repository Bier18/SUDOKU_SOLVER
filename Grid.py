from ErrorTypes import GridError
class Grid:

    def __init__(self):
        self.grid = []


    # inizializza la griglia da file di testo
    def load_grid(self):
        ret_code = 0
        # apre il file
        with open("grid.txt", 'r') as i_file:
            #  legge le righe del file
            for line in i_file:
                # toglie il carattere \n
                line = line.strip()
                # popola la griglia
                row = [int(c) for c in line if c.isdigit()]
                if len(row) < 9:
                    ret_code = GridError.ERROR_WRONG_CHAR_IN_INPUT_FILE
                elif len(row) > 9:
                    ret_code = GridError.ERROR_WRONG_LINE_LENGTH_IN_INPUT_FILE
                else:
                    self.grid.append(row)

        if ret_code != GridError.OK :
            return ret_code
        else:
            # stampa di debug
            self.print_grid()

        return GridError.OK

    # interpreta gli errori
    def get_Error_Description(self, error_code):
        match error_code:

            case GridError.ERROR_WRONG_CHAR_IN_INPUT_FILE:
                return "Carattere in input errato"
            case GridError.ERROR_WRONG_LINE_LENGTH_IN_INPUT_FILE:
                return "Errore nella lunghezza della riga"
            case _:
                return "Errore sconosciuto"

    # mostra la griglia
    def print_grid( self ):

        grid_to_print = ""

        for i in range(9):

            if i % 3 == 0:
                grid_to_print += "+--- --- -+--- --- -+--- --- -+" + "\n"

            for j in range(9):
                digit = self.grid[i][j]

                # se l'elemento è un numero lo stampa
                if digit != 0:
                    string_digit = str(digit)
                # altrimenti casella vuota
                else:
                    string_digit = "."

                if j % 3 == 0:
                    grid_to_print += ( "| " + string_digit + " " )
                else:
                    grid_to_print += (" " + string_digit + " ")

            grid_to_print += "|\n"

        grid_to_print += "+--- --- -+--- --- -+--- --- -+" + "\n"

        print( grid_to_print )

    def update_cell(self, number, row, column):
        self.grid[row][column] = number
