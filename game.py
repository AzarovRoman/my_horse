import random

from itertools import product, permutations, chain
from string import ascii_uppercase, digits
from collections import namedtuple

coordinates = namedtuple('coord', ('x', 'y'))
DIGITS = digits[1:9]
LETTERS = ascii_uppercase[:8]


class Cell:
    def __init__(self):
        self.check_horse = False
        self.check_use = False

    def fill(self):
        if self.check_horse:
            return '?'
        elif self.check_use:
            return 'X'
        else:
            return ' '


class Field:
    def __init__(self):
        self.field = []

    def filling(self):
        for row_index in range(8):
            line = []
            for column_index in range(8):
                cell = Cell()
                line.append(cell)
            self.field.append(line)
        return self.field

    def visual(self):
        for number, line in zip(DIGITS, self.field):
            print('--------' * 8)
            print(number, end='')
            print('|       ' * 8)
            for element in line:
                print(f' |   {element.fill()}  ', end='')
            print()
            print(' |      ' * 8)

        for letter in LETTERS:
            print(f'     {letter}  ', end='')
        print()


class Horse:
    def __init__(self, field):
        self.field = field
        self.current_coordinates = None

    def convert_coordinates(self, coordinate):
        try:
            y_coord, x_coord = coordinate
            y_coord = LETTERS.index(y_coord.upper())
            x_coord = DIGITS.index(x_coord)
            return y_coord, x_coord

        except ValueError:
            return None

    def move(self, coordinates_movement):
        x_coord, y_coord = coordinates_movement

        if self.current_coordinates is not None:
            x_current, y_current = self.current_coordinates
            self.field[y_current][x_current].check_use = True
            self.field[y_current][x_current].check_horse = False

        self.field[y_coord][x_coord].check_horse = True
        self.current_coordinates = coordinates(x_coord, y_coord)

        return False

    def progress_check(self, coordinates_movements):
        if not self.current_coordinates and coordinates_movements:
            return True

        try:
            y_current, x_current = self.current_coordinates
            y_coord, x_coord = coordinates_movements
            y_res, x_res = abs(y_current - y_coord), abs(x_current - x_coord)

            if not self.field[y_coord][x_coord].check_use:
                return (x_res, y_res) in ((2, 1), (1, 2))

        except TypeError:
            return False

        return False

    def search_movements(self):
        a = [1, -1]
        b = [2, -2]
        movements_list = []

        y_current, x_current = self.current_coordinates
        coords = list(chain(*[permutations(index) for index in product(b, a)]))

        for x, y in coords:
            y += y_current
            x += x_current
            new_coord = coordinates(y, x)
            if 8 > x >= 0 and 8 > y >= 0:
                if not self.field[y][x].check_use:
                    movements_list.append(new_coord)

        return movements_list


def game():
    field = Field()
    horse = Horse(field.filling())
    check_finish = False
    check_gamer = True
    check_horse = False

    while not check_horse:
        movement_coordinates = horse.convert_coordinates(input('выберите куда ставим коня: '))
        if horse.progress_check(movement_coordinates):
            horse.move(movement_coordinates)
            check_horse = True
        else:
            print('-введена неверная координата-')

    while not check_finish:
        field.visual()

        if check_gamer:
            movement_coord = horse.convert_coordinates(input('введите координаты формата А1: '))

            if horse.progress_check(movement_coord):
                horse.move(movement_coord)
                check_gamer = False

            if not horse.search_movements():
                check_finish = True
                break

        else:
            horse.move(random.choice(horse.search_movements()))
            check_gamer = True

        print('\n')

        if horse.search_movements() == ():
            check_finish = True
            break


game()
