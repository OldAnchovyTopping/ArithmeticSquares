from puzzle_class import Square
from itertools import permutations


def permutation_bruteforce(grid: Square) -> Square:
    for perm in permutations(range(1, 1 + grid.dimension ** 2)):
        grid.change_entries(perm)
        if grid.are_all_constraints_satisfied():
            return grid


def row_recursion(
    grid: Square, unused: list[int], depth: int, limit: int
) -> Square | None:
    # print(grid)
    # Base case:
    if depth == limit:
        grid.single_entry_change(depth, unused[0])
        return grid if grid.are_all_constraints_satisfied() else None
    row_index, column_index = divmod(depth, grid.dimension)
    for index, new_value in enumerate(unused):
        grid.single_entry_change(depth, new_value)
        if row_index == grid.dimension - 1:
            # Final row, check column!
            if not grid.check_column(column_index):
                continue
        elif column_index == grid.dimension - 1:
            # Final row entry; check the row!
            if not grid.check_row(row_index):
                continue
        # If the checks pass, we recurse:
        still_unused = unused[:index] + unused[index + 1:]
        maybe_s = row_recursion(grid, still_unused, depth + 1, limit)
        if maybe_s is not None:
            return maybe_s
    grid.single_entry_change(depth, 0)
    return None


def ordered_recursion(
    grid: Square, unused: list[int], tile_order: list[int],
) -> Square | None:
    # Base case:
    if len(unused) == 1:
        grid.single_entry_change(tile_order[0], unused[0])
        return grid if grid.are_all_constraints_satisfied() else None


if __name__ == '__main__':
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    print(permutation_bruteforce(first_33))
    order_16 = Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                          "--/-1", "++-4", "*-+25", "+*/9"])
    print(permutation_bruteforce(order_16))
    small = Square(2, ["+6", "+4", "+7", "+3"])
    print(row_recursion(small, [1, 2, 3, 4], 0, 3))
    print(row_recursion(first_33, list(range(1, 10)), 0, 8))
    column_order_16 = Square(4, ["--/-1", "++-4", "*-+25", "+*/9",
                                 "++-2", "*--15", "+-*96", "--/-1"])
    print(row_recursion(column_order_16, list(range(1, 17)), 0, 15))
