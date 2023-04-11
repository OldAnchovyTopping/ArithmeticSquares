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


from itertools import combinations, permutations
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
        self.print_data = []
        self.equations = []
        # Because there is one fewer operations than numbers in rows/columns.
        for row in operations_and_results:
            offset_ops = [op.rjust(self.width) for op in row[:minus]]
            result_str = row[minus:].rjust(self.width)
            self.print_data.append((offset_ops, result_str, int(row[minus:])))
            self.equations.append((row[:minus], int(row[minus:])))
        # Now make lists for the numbers and their pretty-printing counterparts:
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
            quot, rem = divmod(row_index, 2)
            if rem:
                for index in range(self.dimension, 2 * self.dimension):
                    final += f"|{self.print_data[index][0][quot]}|"
                    final += xs
                final += f"|{xs}|\n"
            else:
                for value, operation in zip(self.entries[quot],
                                            self.print_data[quot][0]):
                    final += f"|{self.number_strs[value]}|{operation}"
                num_str = self.number_strs[self.entries[quot][-1]]
                final += f"|{num_str}|{equals}|{self.print_data[quot][1]}|\n"
            final += split
        # Last few lines are different:
        for _ in range(self.dimension):
            final += f"|{equals}|{xs}"
        final += f"|{xs}|\n{split}"
        for index in range(self.dimension, 2 * self.dimension):
            final += f"|{self.print_data[index][1]}|"
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
        return result == self.equations[index][1]  # Check if they match.

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
            op = self.equations[eq_index][0][row_index - 1]
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
        return result == self.equations[eq_index][1]  # Check if they match.

    def are_all_constraints_satisfied(self) -> bool:
        """Checks if all rows and columns obey the equations."""
        for i in range(self.dimension):
            if not(self.check_column(i) and self.check_row(i)):
                return False
        return True

    def change_entries(self, new_entries: list[int] | tuple[int]):
        """
        Changes all entries.

        :param new_entries: New entries.
        :return: None
        """
        assert len(new_entries) == self.dimension ** 2,\
            "Incorrect number of entries"
        increasing = 0
        for row_index in range(self.dimension):
            for column_index in range(self.dimension):
                self.entries[row_index][column_index] = new_entries[increasing]
                increasing += 1

    def single_entry_change(self, position: int, value: int):
        """
        Changes a single entry.

        :param position: If q*dim + r = position, then entry[q][r] is changed.
        :param value: The new value.
        :return: None
        """
        assert 0 <= position < self.dimension ** 2, "Position index is too big!"
        assert 0 <= value <= self.dimension ** 2, "Number value is too big!"
        quotient, remainder = divmod(position, self.dimension)
        self.entries[quotient][remainder] = value

    def equation_possibilities(self, index):
        operations, target = self.equations[index]
        used_numbers = range(1, 1 + self.dimension ** 2)
        possible_combinations = []
        for combo in combinations(used_numbers, self.dimension):
            for eq_entries in permutations(combo):
                computed_result = eq_entries[0]
                for operation, number in zip(operations, eq_entries[1:]):
                    match operation:
                        case "+":
                            computed_result += number
                        case "-":
                            computed_result -= number
                        case "*":
                            computed_result *= number
                        case "/":
                            computed_result /= number
                        case _:
                            raise (ValueError(f"{operation} is not one of"
                                              f"the four operations"))
                if computed_result == target:
                    possible_combinations.append(eq_entries)
        tile_possibilities = [set() for _ in range(self.dimension)]
        for entries in possible_combinations:
            for index in range(self.dimension):
                tile_possibilities[index].add(entries[index])
        return possible_combinations, tile_possibilities

    def options_in_all_equations(self):
        option_list = []
        for index in range(2 * self.dimension):
            option_list.append(self.equation_possibilities(index))
        return option_list


if __name__ == '__main__':
    # [5, 7, 6, 8, 4, 2, 9, 1, 3]:
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    print(first_33)
    first_33.change_entries([5, 7, 6, 8, 4, 2, 9, 1, 3])
    print(first_33)
    print(first_33.are_all_constraints_satisfied())
    # 1-16 in row-order:
    print(Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                     "--/-1", "++-4", "*-+25", "+*/9"]))
