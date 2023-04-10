from puzzle_class import Square
from itertools import permutations


def permutation_bruteforce(grid: Square):
    for perm in permutations(range(1, 1 + grid.dimension ** 2)):
        grid.change_entries(perm)
        if grid.are_all_constraints_satisfied():
            return grid


def naive_recursion(grid: Square):
    pass


if __name__ == '__main__':
    first_33 = Square(3, ["+-6", "-*8", "*/3", "+-4", "-*3", "*/4"])
    print(permutation_bruteforce(first_33))
    order_16 = Square(4, ["++-2", "*--15", "+-*96", "--/-1",
                          "--/-1", "++-4", "*-+25", "+*/9"])
    print(permutation_bruteforce(order_16))
