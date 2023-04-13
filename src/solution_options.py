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


def iterative_deletion(dimension: int, tile_possible: list[set[int]],
                       combos_and_tiles):
    dim_squared = dimension * dimension
    # First some index pre-work:
    eq_indices = []
    for i in range(dimension):
        eq_indices.append(tuple(range(i*dimension, (i+1)*dimension)))
    for i in range(dimension, 2 * dimension):
        eq_indices.append(tuple(range(i-dimension, dim_squared, dimension)))
    # Now we iteratively eliminate possible combos:
    previous_combos = [combos_and_tiles[i][0] for i in range(2 * dimension)]
    change_was_made = True
    while change_was_made:
        combos_tiles_together = []
        change_was_made = False
        print("Start of next iteration")
        # print(grid_possibilities)
        for i, equation in enumerate(previous_combos):
            eq_combos = []
            eq_possible = [set() for _ in range(dimension)]
            # print(i, equation)
            for combo in equation:
                if is_combo_doable(combo, eq_indices[i], tile_possible):
                    eq_combos.append(combo)
                    for index in range(dimension):
                        eq_possible[index].add(combo[index])
            combos_tiles_together.append((eq_combos, eq_possible))
        for index in range(dim_squared):
            q, r = divmod(index, dimension)
            row_possible: set[int] = combos_tiles_together[q][1][r]
            col_possible: set[int] = combos_tiles_together[dimension + r][1][q]
            r_c_intersection: set[int] = row_possible.intersection(col_possible)
            if r_c_intersection != tile_possible[index]:
                change_was_made = True
            tile_possible[index] = r_c_intersection
        previous_combos = [combos_tiles_together[i][0] for i in
                           range(2 * dimension)]
    return previous_combos, tile_possible


def columns_recursively(first: list[int], possible: list[list[tuple[int]]],
                        depth: int, limit: int):
    if depth == limit:
        pass


def possibility_collapse(grid: Square) -> Square | None:
    combos_and_tiles = grid.options_in_all_equations()
    grid_possibilities = []
    d_sq = grid.dimension ** 2
    for index in range(d_sq):
        q, r = divmod(index, grid.dimension)
        row_possible = combos_and_tiles[q][1][r]
        column_possible = combos_and_tiles[grid.dimension + r][1][q]
        grid_possibilities.append(row_possible.intersection(column_possible))
    # Iteratively reduce the possibilities:
    remaining_combos, grid_possibilities =\
        iterative_deletion(grid.dimension, grid_possibilities, combos_and_tiles)

    for p in remaining_combos:
        print(len(p), p)
    for t in grid_possibilities:
        print(len(t))
    for first_row in remaining_combos[0]:
        limited_possible = grid_possibilities[:]  # Copy over.
        for index, number in enumerate(first_row):
            limited_possible[index] = {number}  # Overwrite.
            # And delete it from anywhere else:
            for delete_index in range(grid.dimension, d_sq):
                limited_possible[delete_index].discard(number)
        print(first_row)
        print(limited_possible)

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
    print(possibility_collapse(gmp_33))
