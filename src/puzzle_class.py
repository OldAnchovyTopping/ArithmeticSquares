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
        # print(self.equations)
        self.entries = [[0 for _ in range(dimension)] for _ in range(dimension)]
        dim_sq = dimension * dimension + 1
        self.number_strs = {n: str(n).rjust(self.width) for n in range(dim_sq)}
        # print(self.number_strs)

    def __str__(self):
        split = "+" + ("-" * self.width + "+") * (2 * self.dimension + 1) + "\n"
        xs = "X" * self.width
        equals = " " * (self.width - 1) + "="
        final = split
        for row_index in range(2 * self.dimension - 1):
            quotient, remainder = divmod(row_index, 2)
            if remainder:
                for index in range(self.dimension, 2 * self.dimension):
                    final += f"|{self.equations[index][0][quotient]}|"
                    final += xs
                final += f"|{xs}|\n"
            else:
                for value, operation in zip(self.entries[quotient],
                                            self.equations[quotient][0]):
                    final += f"|{self.number_strs[value]}|{operation}"
                num_str = self.number_strs[self.entries[quotient][-1]]
                final += f"|{num_str}|{equals}|{self.equations[quotient][1]}|\n"
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

    def check_row(self, index: int) -> bool:
        """
        Checks if the index-mentioned row is filled in AND
        that it satisfies the grid equation.

        :param index: The row index to look at.
        :return: Whether the equation evaluated
            in order matches the given target.
        """
        assert index < self.dimension, "Row index too big!"
        result = self.entries[index][0]
        if not result:
            # This entry is not filled in, so false.
            return False
        for op, num in zip(self.equations[index][0], self.entries[index][1:]):
            if not num:
                # This entry is not filled in, so false.
                return False
            op = op[-1]
            match op:
                case "+":
                    result += num
                case "-":
                    result -= num
                case "*":
                    result *= num
                case "/":
                    result /= num
                case _:
                    raise(ValueError(f"{op} is not one of the four operations"))
        return result == self.equations[index][2]  # Check if they match.

    def check_column(self, index: int) -> bool:
        """
        Checks if the index-mentioned row is filled in AND
        that it satisfies the grid equation.

        :param index: The  column index to look at.
        :return: Whether the equation evaluated
            in order matches the given target.
        """
        assert index < self.dimension, "Column index too big!"
        result = self.entries[0][index]
        if not result:
            # This entry is not filled in, so false.
            return False
        eq_index = self.dimension + index
        for row_index in range(1, self.dimension):
            number = self.entries[row_index][index]
            if not number:
                # This entry is not filled in, so false.
                return False
            op = self.equations[eq_index][0][row_index - 1][-1]
            match op:
                case "+":
                    result += number
                case "-":
                    result -= number
                case "*":
                    result *= number
                case "/":
                    result /= number
                case _:
                    raise(ValueError(f"'{op}' is not in the four operations"))
        return result == self.equations[eq_index][2]  # Check if they match.

    def are_all_constraints_satisfied(self) -> bool:
        for i in range(self.dimension):
            if not(self.check_column(i) and self.check_row(i)):
                return False
        return True

    def change_entries(self, new_entries: list[int] | tuple[int]):
        assert len(new_entries) == self.dimension ** 2,\
            "Incorrect number of entries"
        increasing = 0
        for row_index in range(self.dimension):
            for column_index in range(self.dimension):
                self.entries[row_index][column_index] = new_entries[increasing]
                increasing += 1


if __name__ == '__main__':
    # unknown solution:
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    print(first_33)
    first_33.change_entries([5, 7, 6, 8, 4, 2, 9, 1, 3])
    print(first_33)
    print(first_33.are_all_constraints_satisfied())
    # 1-16 in row-order:
    print(Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                     "--/-1", "++-4", "*-+25", "+*/9"]))
