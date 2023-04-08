"""
From operations and results such as \n
["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"] \n
this class makes an object representing the square:

+-+-+-+-+-+-+-+\n
| |+| |-| |=|6|\n
+-+-+-+-+-+-+-+\n
|+|X|-|X|*|X|X|\n
+-+-+-+-+-+-+-+\n
| |-| |*| |=|8|\n
+-+-+-+-+-+-+-+\n
|+|X|*|X|/|X|X|\n
+-+-+-+-+-+-+-+\n
| |*| |/| |=|3|\n
+-+-+-+-+-+-+-+\n
|=|X|=|X|=|X|X|\n
+-+-+-+-+-+-+-+\n
|4|X|3|X|4|X|X|\n
+-+-+-+-+-+-+-+\n
"""


class Square:
    def __init__(self, operations_and_results: list[str]):
        self.equations = []
        for row in operations_and_results:
            self.equations.append((row[:2], row[2:], int(row[2:])))
        print(self.equations)

    def __str__(self):
        horizontal_split = "+-+-+-+-+-+-+-+\n"
        final_string = horizontal_split
        for row_index in range(5):
            quotient, remainder = divmod(row_index, 2)
            if remainder:
                first = _
                second = _
                third = _
                final_string += f"|{first}|X|{second}|X|{third}|X|X|\n"
            else:
                (op_1, op_2), number, _ = self.equations[quotient]
                final_string += f"| |{op_1}| |{op_2}| |=|{number}|\n"
            final_string += horizontal_split
        # Last few lines are different:
        final_string +=\
            f"|=|X|=|X|=|X|X|\n+-+-+-+-+-+-+-+\n" \
            f"|{self.equations[3][1]}|X|{self.equations[4][1]}" \
            f"|X|{self.equations[5][1]}|X|X|\n+-+-+-+-+-+-+-+\n"
        return final_string


if __name__ == '__main__':
    print(Square(["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"]))
