import unittest

from logic.arrange_the_ships_logic import ArrangeTheShipsLogic


class ArrangeTheShipsLogicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.arrange_the_ships_logic = ArrangeTheShipsLogic(None, None, for_test=True)
        field = self.create_field()
        self.arrange_the_ships_logic.field_size = (10, 10)
        self.arrange_the_ships_logic.field_for_related_entity = field

    def test_get_possible_related_entity_subject_to_axis(self):
        expected_on_first_case = [(0, 0), (1, 0), (2, 0), (3, 0)]
        actual_on_first_case \
            = self.arrange_the_ships_logic\
                  .get_possible_related_entity_subject_to_axis(
                   4, (0, 0), 'x')
        self.assertEqual(expected_on_first_case, actual_on_first_case)

        expected_on_second_case = [(0, 0), (0, 1), (0, 2), (0, 3)]
        actual_on_second_case \
            = self.arrange_the_ships_logic \
                  .get_possible_related_entity_subject_to_axis(
                   4, (0, 0), 'y')
        self.assertEqual(expected_on_second_case, actual_on_second_case)

    def test_is_a_related_entity_with_entity(self):
        self.arrange_the_ships_logic.field_for_related_entity[0][1][1] = 1
        actual = self.arrange_the_ships_logic.is_a_related_entity(0, (1, 1))
        self.assertEqual(True, actual)

    def test_is_a_related_entity_without_entity(self):
        actual = self.arrange_the_ships_logic.is_a_related_entity(0, (1, 1))
        self.assertEqual(False, actual)

    def test_determine_axis_x(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][i][0] = 4
        expected = 'x'
        actual = self.arrange_the_ships_logic.determine_axis(0, (0, 0))
        self.assertEqual(expected, actual)

    def test_determine_axis_y(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][0][i] = 4
        expected = 'y'
        actual = self.arrange_the_ships_logic.determine_axis(0, (0, 0))
        self.assertEqual(expected, actual)

    def test_find_related_entity_on_the_field_x_axis_angle(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][i][0] = 4
        expected = [(0, 0), (1, 0), (2, 0), (3, 0)]
        actual_for_first_case \
            = self.arrange_the_ships_logic\
                  .find_related_entity_on_the_field(
                   0, 'x', (0, 0), 4)
        actual_for_second_case \
            = self.arrange_the_ships_logic \
                  .find_related_entity_on_the_field(
                   0, 'x', (1, 0), 4)
        self.assertEqual(expected, actual_for_first_case)
        self.assertEqual(expected, actual_for_second_case)

    def test_find_related_entity_on_the_field_x_axis_centre(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][i][3] = 4
        expected = [(0, 3), (1, 3), (2, 3), (3, 3)]
        actual_for_first_case \
            = self.arrange_the_ships_logic\
                  .find_related_entity_on_the_field(
                   0, 'x', (0, 3), 4)
        actual_for_second_case \
            = self.arrange_the_ships_logic \
                  .find_related_entity_on_the_field(
                   0, 'x', (1, 3), 4)
        self.assertEqual(expected, actual_for_first_case)
        self.assertEqual(expected, actual_for_second_case)

    def test_find_related_entity_on_the_field_y_axis_centre(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][3][i] = 4
        expected = [(3, 0), (3, 1), (3, 2), (3, 3)]
        actual_for_first_case \
            = self.arrange_the_ships_logic\
                  .find_related_entity_on_the_field(
                   0, 'y', (3, 0), 4)
        actual_for_second_case \
            = self.arrange_the_ships_logic \
                  .find_related_entity_on_the_field(
                   0, 'y', (3, 1), 4)
        self.assertEqual(expected, actual_for_first_case)
        self.assertEqual(expected, actual_for_second_case)

    def test_find_related_entity_on_the_field_y_axis_angle(self):
        for i in range(4):
            self.arrange_the_ships_logic.field_for_related_entity[0][0][i] = 4
        expected = [(0, 0), (0, 1), (0, 2), (0, 3)]
        actual_for_first_case \
            = self.arrange_the_ships_logic\
                  .find_related_entity_on_the_field(
                   0, 'y', (0, 0), 4)
        actual_for_second_case \
            = self.arrange_the_ships_logic \
                  .find_related_entity_on_the_field(
                   0, 'y', (0, 1), 4)
        self.assertEqual(expected, actual_for_first_case)
        self.assertEqual(expected, actual_for_second_case)

    @staticmethod
    def create_field():
        field = {0: {}, 1: {}}
        for x in range(10):
            field[0][x] = {}
            for y in range(10):
                field[0][x][y] = 0
        return field

    def test_calculate_the_number_of_ships_on_the_field(self):
        multiplicities = [1, 2, 2, 5, 10, 20, 40, 81,
                          163, 327, 655, 1310, 2621, 5242,
                          10485, 20971, 41943, 83886, 167772, 335544]
        number_of_cells = [100, 200, 256, 512, 1024, 2048, 4096,
                           8192, 16384, 32768, 65536, 131072,
                           262144, 524288, 1048576, 2097152,
                           4194304, 8388608, 16777216, 33554432]
        for index, multiplicity in enumerate(multiplicities):
            expected = {
                4: 1 * multiplicity,
                3: 2 * multiplicity,
                2: 3 * multiplicity,
                1: 4 * multiplicity
            }
            actual \
                = self.arrange_the_ships_logic\
                .calculate_the_number_of_related_entity_on_the_field(
                 number_of_cells[index])
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
