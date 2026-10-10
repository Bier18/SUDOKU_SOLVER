
import Solver

game_version = "0.2.1"

if __name__ == "__main__":

    start_message = "############################\n"
    start_message += "WELCOME IN SUDOKU SOLVER " + game_version + "\n"
    start_message += "############################\n"

    print(start_message)

    # crea il risolutore
    solver = Solver.Solver()
    # avvia il gioco
    solver.solve()