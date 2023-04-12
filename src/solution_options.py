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


def is_combo_doable(
    the_combo: list[int], positions, possible: list[set[int]]
) -> bool:
    for index, value in enumerate(the_combo):
        if value not in possible[positions[index]]:
            return False
    return True


def possibility_collapse(grid: Square) -> Square | None:
    combos_and_tiles = grid.options_in_all_equations()
    grid_possibilities = []
    d_sq = grid.dimension ** 2
    for index in range(d_sq):
        q, r = divmod(index, grid.dimension)
        row_possible = combos_and_tiles[q][1][r]
        column_possible = combos_and_tiles[grid.dimension + r][1][q]
        grid_possibilities.append(row_possible.intersection(column_possible))
    # First some index pre-work:
    eq_indices = []
    for i in range(grid.dimension):
        eq_indices.append(tuple(range(i*grid.dimension, (i+1)*grid.dimension)))
    for i in range(grid.dimension, 2 * grid.dimension):
        eq_indices.append(tuple(range(i-grid.dimension, d_sq, grid.dimension)))
    # Now we iteratively eliminate possible combos:
    previous_combos = [combos_and_tiles[i][0] for i in range(2*grid.dimension)]
    change_was_made = True
    while change_was_made:
        combos_tiles_together = []
        change_was_made = False
        print("Start of next iteration")
        print(grid_possibilities)
        for i, equation in enumerate(previous_combos):
            eq_combos = []
            eq_possible = [set() for _ in range(grid.dimension)]
            print(i, equation)
            for combo in equation:
                if is_combo_doable(combo, eq_indices[i], grid_possibilities):
                    eq_combos.append(combo)
                    for index in range(grid.dimension):
                        eq_possible[index].add(combo[index])
            combos_tiles_together.append((eq_combos, eq_possible))
        for index in range(d_sq):
            q, r = divmod(index, grid.dimension)
            row_possible = combos_tiles_together[q][1][r]
            column_possible = combos_tiles_together[grid.dimension + r][1][q]
            row_column_intersection = row_possible.intersection(column_possible)
            if row_column_intersection != grid_possibilities[index]:
                change_was_made = True
            grid_possibilities[index] = row_column_intersection
        previous_combos = [combos_tiles_together[i][0] for i in
                           range(2 * grid.dimension)]
    for p in previous_combos:
        print(p)
    return


if __name__ == '__main__':
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    order_16 = Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                          "--/-1", "++-4", "*-+25", "+*/9"])
    small = Square(2, ["+6", "+4", "+7", "+3"])
    column_order_16 = Square(4, ["--/-1", "++-4", "*-+25", "+*/9",
                                 "++-2", "*--15", "+-*96", "--/-1"])
    gmp_33 = Square(3, ["/*2", "*-1", "+-4", "/*2", "*-1", "-+8"])
    # print(permutation_bruteforce(first_33))
    # print(permutation_bruteforce(order_16))
    # print(row_recursion(small, [1, 2, 3, 4], 0, 3))
    # print(row_recursion(first_33, list(range(1, 10)), 0, 8))
    # print(row_recursion(column_order_16, list(range(1, 17)), 0, 15))
    # print(row_recursion(gmp_33, list(range(1, 10)), 0, 8))
    print(possibility_collapse(first_33))
