#Task 6: More on Classes
class TictactoeException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Board:

    valid_moves = [
        "upper left",
        "upper center",
        "upper right",
        "middle left",
        "center",
        "middle right",
        "lower left",
        "lower center",
        "lower right"
    ]
        
    def __init__(self):
        self.board_array = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        self.turn = "X"


    def __str__(self):
        lines = []

        lines.append(f"{self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]}")
        lines.append(f"{self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]}")
        lines.append(f"{self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]}")

        return "\n".join(lines)

    def move(self, move_string):

        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")

        move_index = Board.valid_moves.index(move_string)

        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][column] = self.turn

        self.last_move = move_string

        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        cat = True

        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break

        if cat:
            return (True, "Cat's Game.")

        win = False

        for i in range(3):  # check rows
            if self.board_array[i][0] != " ":
                if (
                    self.board_array[i][0] == self.board_array[i][1]
                    and self.board_array[i][1] == self.board_array[i][2]
                ):
                    win = True
                    break

        if not win:
            for i in range(3):  # check columns
                if self.board_array[0][i] != " ":
                    if (
                        self.board_array[0][i] == self.board_array[1][i]
                        and self.board_array[1][i] == self.board_array[2][i]
                    ):
                        win = True
                        break

        if not win:
            if self.board_array[1][1] != " ":
                if (
                    self.board_array[0][0] == self.board_array[1][1]
                    and self.board_array[2][2] == self.board_array[1][1]
                ):
                    win = True

                if (
                    self.board_array[0][2] == self.board_array[1][1]
                    and self.board_array[2][0] == self.board_array[1][1]
                ):
                    win = True

        if not win:
            if self.turn == "X":
                return (False, "X's turn.")
            else:
                return (False, "O's turn.")
        else:
            if self.turn == "O":
                return (True, "X has won")
            else:
                return (True, "O has won")
    


board = Board()

game_over = False

while not game_over:

    print(board)

    move = input(f"{board.turn}'s turn: ")

    try:
        board.move(move)

    except TictactoeException as e:
        print(e.message)
        continue

    game_over, message = board.whats_next()

    print(message)