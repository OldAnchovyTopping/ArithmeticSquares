from puzzle_class import Square
from copy import deepcopy
from itertools import permutations


def permutation_bruteforce(grid: Square) -> Square:
    """The simplest possible algorithm. Returns ONE solution (if it exists)."""
    for perm in permutations(range(1, 1 + grid.dimension ** 2)):
        grid.change_entries(perm)
        if grid.are_all_constraints_satisfied():
            return grid


def primitive_row_recursion(
    grid: Square, unused: list[int], depth: int, limit: int
) -> Square | None:
    """Recursive method of solution that fills the tiles row by row.
    Whenever it fills a row/column, it checks if the equations is correct.
    Returns ONE solution, if one exists."""
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
        maybe_s = primitive_row_recursion(grid, still_unused, depth + 1, limit)
        if maybe_s is not None:
            return maybe_s
    grid.single_entry_change(depth, 0)
    return None


def is_combo_doable(
    the_combo: list[int], positions, possible: list[set[int]]
) -> bool:
    """
    Helper method of iterative_deletion; checks if all tiles in the_combo
    have a value which is listed as possible in the tile.

    :param the_combo: Asked for entries of the row/column
    :param positions: the positions on which this combination belongs
    :param possible: tile possibilities
    :return: "all entries in the_combo are possible in their tiles" (True/False)
    """
    for index, value in enumerate(the_combo):
        if value not in possible[positions[index]]:
            return False
    return True


def iterative_deletion(dimension: int, tile_possible: list[set[int]],
                       available_combos: list[list[tuple[int]]]):
    """Iteratively deletes possibilities.
    First, it prunes all combos that are not doable (see above).
    Then, based on that, it removes some tile entries, which are no longer
    achievable through any combination.
    This is repeated until no change is made.
    """
    dim_squared = dimension * dimension
    # First some index pre-work:
    eq_indices = []
    for i in range(dimension):
        eq_indices.append(tuple(range(i*dimension, (i+1)*dimension)))
    for i in range(dimension, 2 * dimension):
        eq_indices.append(tuple(range(i-dimension, dim_squared, dimension)))
    # Now we iteratively eliminate possible combos:
    previous_combos = available_combos[:]
    change_was_made = True
    while change_was_made:
        combos_tiles_together = []
        change_was_made = False
        # print(tile_possible)
        # print(previous_combos)
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
        if not all(tile_possible):  # Some tile has no possibilities!
            return [], []
    return previous_combos, tile_possible


def rows_recursively(dim: int, depth: int,
                     combos: list[list[tuple[int]]], grid_possibilities):
    """Given an ensemble of possible combos, the function recursively fills in
    all rows.

    After fixing each row, the grid_possibilities are changed to
    reflect this change (those positions are fixed to {number}, and this number
    is removed from all other tiles).
    """
    # print(depth)
    # print(grid_possibilities)
    if dim == depth:
        # Bottom of generators.
        yield grid_possibilities
    else:
        for new_row in combos[depth]:
            limited_possible = deepcopy(grid_possibilities)  # Copy over.
            for index, number in enumerate(new_row, start=depth * dim):
                limited_possible[index] = {number}  # Overwrite.
                # And delete it from anywhere else:
                for delete_index in range((depth + 1) * dim, dim ** 2):
                    limited_possible[delete_index].discard(number)
            # print(limited_possible)
            for options in limited_possible:
                if not options:
                    break
            else:  # I.e. if every tile has a possibility remaining.
                cs_left, maybe_s = iterative_deletion(
                    dim, limited_possible, combos
                )
                # print(maybe_s)
                if not maybe_s:  # There is a tile with no possibilities, skip
                    continue
                elif sum(map(len, maybe_s)) == dim ** 2:
                    # Already we have a single digit everywhere.
                    if set(map(lambda x: next(iter(x)), maybe_s)) ==\
                            set(range(1, dim ** 2 + 1)):
                        # Now we checked that we used all the digits.
                        yield maybe_s
                else:
                    yield from rows_recursively(dim, depth+1, cs_left, maybe_s)


def possibility_collapse(grid: Square) -> list[Square] | Square | None:
    """Finds ALL solutions of the given arithmetic square.

    This function first calculates all possibilities in all rows/columns, then
    iteratively reduces these options.

    To finish, it recurses down the rows."""
    combos_and_tiles = grid.options_in_all_equations()
    grid_possibilities = []
    d_sq = grid.dimension ** 2
    for index in range(d_sq):
        q, r = divmod(index, grid.dimension)
        row_possible = combos_and_tiles[q][1][r]
        column_possible = combos_and_tiles[grid.dimension + r][1][q]
        grid_possibilities.append(row_possible.intersection(column_possible))
    combos = [combos_and_tiles[i][0] for i in range(2 * grid.dimension)]
    # Iteratively reduce the possibilities:
    remaining_combos, grid_possibilities =\
        iterative_deletion(grid.dimension, grid_possibilities, combos)
    if not grid_possibilities:  # Early break if no solutions
        return None
    solution_list = []
    for solution in rows_recursively(grid.dimension, 0,
                                     remaining_combos, grid_possibilities):
        copied_grid = deepcopy(grid)
        for index in range(d_sq):
            tile_entry = solution[index].pop()
            copied_grid.single_entry_change(index, tile_entry)
        solution_list.append(copied_grid)
    if not solution_list:
        # No solutions.
        return None
    if len(solution_list) == 1:
        # Exactly one solution.
        return solution_list[0]
    # Multiple solutions.
    return solution_list


def given_result_list(operations: list[str], results: list[int]) -> dict:
    assert len(operations) == len(results)
    assert not(len(results) & 1)
    dimension = len(results) // 2
    result_options: set[tuple[int]] = set(permutations(results))
    solution_dict = {}
    for mask in result_options:
        # print(mask)
        true_operations = operations[:]
        for index, number in enumerate(mask):
            true_operations[index] = true_operations[index] + str(number)
        # print(true_operations)
        the_grid = Square(dimension, true_operations)
        potential_solutions = possibility_collapse(the_grid)
        if potential_solutions is not None:
            solution_dict[mask] = potential_solutions
    return solution_dict


if __name__ == '__main__':
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    order_16 = Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                          "--/-1", "++-4", "*-+25", "+*/9"])
    small = Square(2, ["+6", "+4", "+5", "+5"])
    column_order_16 = Square(4, ["--/-1", "++-4", "*-+25", "+*/9",
                                 "++-2", "*--15", "+-*96", "--/-1"])
    gmp_33 = Square(3, ["/*2", "*-1", "+-4", "/*2", "*-1", "-+8"])
    # print(permutation_bruteforce(first_33))
    # print(permutation_bruteforce(order_16))
    # print(possibility_collapse(column_order_16))
    ops = ["**", "*+", "++", "++", "**", "*-"]
    numbers = [18, 18, 18, 18, 20, 20]
    # ops = ["+-", "-+", "/*", "*-", "/*", "++"]
    # numbers = [11, 12, 12, 12, 12, 21]
    solutions = given_result_list(ops, numbers)
    for key, sols in solutions.items():
        print(f"Solutions for the mask {key}:")
        if isinstance(sols, Square):
            print(sols)
        else:
            for v in sols:
                print(v)
