# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv

import arrays
import factorial
import amutils


def unit_tests():
    arrays.unit_test()
    csv.unit_test()
    amutils.unit_test()


def run():
    print('*******************************************************************')
    unit_tests()
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hello!')  # Press Ctrl+F8 to toggle the breakpoint.
    n = 5
    print(f'factorial of {n} is {factorial.factorial(5)}')
    a = amutils.load("banana.csv")
    print('loaded successfully!')
    a.assert_ok()
    a.explain()
    a.subcols('ascent','distance').explain()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
