
import Solver
from ErrorTypes import SolverError

game_version = "1.1.0"

if __name__ == "__main__":

    start_message = "############################\n"
    start_message += "WELCOME IN SUDOKU SOLVER " + game_version + "\n"
    start_message += "############################\n"

    print(start_message)

    # crea il risolutore
    solver = Solver.Solver()
    # avvia il gioco
    ret_code = solver.solve()

    if ret_code != SolverError.OK:
        print(solver.get_error_description(ret_code))

    # TODO trovare un modo di ottimizzare le prestazioni
    # TODO fare in modo che si possa dare in input il file con un nome qualsiasi