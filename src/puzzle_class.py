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


from math import ceil, log10


class Square:
    def __init__(self, dimension: int, operations_and_results: list[str]):
        self.dimension = dimension
        self.width = ceil(2 * log10(self.dimension))
        assert self.dimension * 2 == len(operations_and_results),\
            "There needs to be twice as many equations as the dimension."
        # First how thick are the columns; we want all same-width.
        minus = self.dimension - 1
        for row in operations_and_results:
            difference = len(row) - minus
            if difference > self.width:
                self.width = difference
        self.equations = []
        # Because there is one fewer operations than numbers in rows/columns.
        for row in operations_and_results:
            offset_ops = [op.rjust(self.width) for op in row[:minus]]
            result_str = row[minus:].rjust(self.width)
            self.equations.append((offset_ops, result_str, int(row[minus:])))
        print(self.equations)

    def __str__(self):
        split = "+" + ("-" * self.width + "+") * (2 * self.dimension + 1) + "\n"
        xs = "X" * self.width
        spaces = " " * self.width
        equals = spaces[:-1] + "="
        final = split
        for row_index in range(2 * self.dimension - 1):
            quotient, remainder = divmod(row_index, 2)
            if remainder:
                for index in range(self.dimension, 2 * self.dimension):
                    final += f"|{self.equations[index][0][quotient]}|"
                    final += xs
                final += f"|{xs}|\n"
            else:
                for operation in self.equations[quotient][0]:
                    final += f"|{spaces}|{operation}"
                final += f"|{spaces}|{equals}|{self.equations[quotient][1]}|\n"
            final += split
        # Last few lines are different:
        for _ in range(self.dimension):
            final += f"|{equals}|{xs}"
        final += f"|{xs}|\n{split}"
        for index in range(self.dimension, 2 * self.dimension):
            final += f"|{self.equations[index][1]}|"
            final += xs
        final += f"|{xs}|\n{split}"
        return final


if __name__ == '__main__':
    print(Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"]))
    print(Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                     "--/-1", "++-4", "*-+25", "+*/9"]))
