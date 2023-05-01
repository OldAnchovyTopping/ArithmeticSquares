from puzzle_class import Square


if __name__ == '__main__':
    print("Welcome to the solver of arithmetic squares.")
    print("Would you like to revise the rules [r] "
          "or have the computer solve [s] one for you?")
    first_instruction = input()
    while first_instruction not in {"r", "s"}:
        print("*** Please type either r, or s and then press ENTER. ***\n")
        print("Would you like to revise the rules [r] "
              "or have the computer solve [s] one for you?")
        first_instruction = input()
    # Rules of the puzzle + an example.
    if first_instruction == "r":
        print("Here are the rules:")
        print("Place each of the numbers 1-9 (or 1-n^2 in a general square of "
              "side n) into the blank tiles of the square.")
        print("Each row and column should satisfy the given equation.")
        print("Note, that the operations are evaluated left-to-right "
              "or top-to-bottom; This means, that 6+5*3 = 33 and NOT 21.")
        input("Press ENTER to see an example grid and its solution.\n")
        print("Here is the example (left) and its solution (right):")
        print("+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "| |+| |-| |=|6|      ->      |5|+|7|-|6|=|6|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "|+|X|-|X|*|X|X|      ->      |+|X|-|X|*|X|X|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "| |-| |*| |=|8|      ->      |8|-|4|*|2|=|8|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "|+|X|*|X|/|X|X|      ->      |+|X|*|X|/|X|X|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "| |*| |/| |=|3|      ->      |9|*|1|/|3|=|3|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "|=|X|=|X|=|X|X|      ->      |=|X|=|X|=|X|X|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n"
              "|4|X|3|X|4|X|X|      ->      |4|X|3|X|4|X|X|\n"
              "+-+-+-+-+-+-+-+      ->      +-+-+-+-+-+-+-+\n")
        input("Press ENTER to continue to setting a problem and solving.\n")
    print("To solve a grid, you first have to input it.")
    print("Let us work with this example:")
    print("+-+-+-+-+-+-+-+\n"
          "| |/| |*| |=|2|\n"
          "+-+-+-+-+-+-+-+\n"
          "|/|X|*|X|-|X|X|\n"
          "+-+-+-+-+-+-+-+\n"
          "| |*| |-| |=|1|\n"
          "+-+-+-+-+-+-+-+\n"
          "|*|X|-|X|+|X|X|\n"
          "+-+-+-+-+-+-+-+\n"
          "| |+| |-| |=|4|\n"
          "+-+-+-+-+-+-+-+\n"
          "|=|X|=|X|=|X|X|\n"
          "+-+-+-+-+-+-+-+\n"
          "|2|X|1|X|8|X|X|\n"
          "+-+-+-+-+-+-+-+\n")
    # Wanting an integer that is the grid dimension:
    while True:
        try:
            size = int(input("Enter the size of the side of the grid. In the "
                             "above example, you'd type 3 (then press ENTER):"))
            break
        except ValueError:
            print("Please type a single integer, then press ENTER.")
    print(f"\nNow, you should specify {2*size} equations that are in the grid.")
    print("First specify the operations with no spaces, then the result. "
          "Finally, separate these by single commas.")
    print("For the above, you may write: /*2, *-1, +-4, /*2, *-1, -+8")
    while True:
        try:
            equations = list(map(lambda x: x.strip(), input().split(",")))
            solver_object = Square(size, equations)
            break
        except ValueError as e:
            print(e)
            print("Please type the desired equations again, following the "
                  "guidelines:\n")
            print("First specify the operations with no spaces, then the "
                  "result. Finally, separate these by single commas.")
            print(f"You should specify {2*size} equations like this.")
        except AssertionError:
            print("You have not specified the correct amount of equations. "
                  "Try again, please.")
    print(equations)
    print(solver_object)
