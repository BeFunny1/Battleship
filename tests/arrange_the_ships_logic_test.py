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

    def test_user_can_pick_this_cell_null_length(self):
        actual_lvl_one = self.arrange_the_ships_logic.user_can_pick_this_cell(level=0)
        actual_lvl_two = self.arrange_the_ships_logic.user_can_pick_this_cell(level=1)
        expected = False
        self.assertEqual(expected, actual_lvl_one)
        self.assertEqual(expected, actual_lvl_two)

    def test_user_can_pick_this_cell_not_null_length(self):
        self.arrange_the_ships_logic.stack_related_entity_first_lvl.append(1)
        self.arrange_the_ships_logic.stack_related_entity_second_lvl.append(1)

        actual_lvl_one = self.arrange_the_ships_logic.user_can_pick_this_cell(level=0)
        actual_lvl_two = self.arrange_the_ships_logic.user_can_pick_this_cell(level=1)
        expected = True
        self.assertEqual(expected, actual_lvl_one)
        self.assertEqual(expected, actual_lvl_two)

    def test_all_ships_arrange_both_stack_empty(self):
        actual = self.arrange_the_ships_logic.all_ships_arrange()
        expected = True
        self.assertEqual(expected, actual)

    def test_all_ships_arrange_one_stack_not_empty(self):
        self.arrange_the_ships_logic.stack_related_entity_first_lvl.append(1)
        actual = self.arrange_the_ships_logic.all_ships_arrange()
        expected = False
        self.assertEqual(expected, actual)

    def test_all_ships_arrange_both_stack_not_empty(self):
        self.arrange_the_ships_logic.stack_related_entity_first_lvl.append(1)
        self.arrange_the_ships_logic.stack_related_entity_second_lvl.append(1)
        actual = self.arrange_the_ships_logic.all_ships_arrange()
        expected = False
        self.assertEqual(expected, actual)

    def test_get_information_about_all_related_entity_with_related_entity(self):
        level, x, y = 0, 0, 0
        self.arrange_the_ships_logic.field_for_related_entity[level][x][y] = 1
        actual = self.arrange_the_ships_logic.get_information_about_all_related_entity()
        expected = [(0, [(0, 0)])]
        self.assertEqual(expected, actual)

    def test_get_information_about_all_related_entity_without_related_entity(self):
        actual = self.arrange_the_ships_logic.get_information_about_all_related_entity()
        expected = []
        self.assertEqual(expected, actual)

    def test_try_to_change_related_entity_axis_change_possible(self):
        self.arrange_the_ships_logic.field_for_related_entity[0][0][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][1][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][2][0] = 3

        self.arrange_the_ships_logic.try_to_change_related_entity_axis(0, (0, 0))
        actual = self.arrange_the_ships_logic.get_information_about_all_related_entity()
        expected = [(0, [(0, 0), (0, 1), (0, 2)])]
        self.assertEqual(expected, actual)

    def test_try_to_change_related_entity_axis_change_impossible(self):
        self.arrange_the_ships_logic.field_for_related_entity[0][0][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][1][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][2][0] = 3

        self.arrange_the_ships_logic.field_for_related_entity[0][0][2] = 1

        self.arrange_the_ships_logic.try_to_change_related_entity_axis(0, (0, 0))
        actual = self.arrange_the_ships_logic.get_information_about_all_related_entity()
        expected = [(0, [(0, 0), (1, 0), (2, 0)]), (0, [(0, 2)])]
        self.assertEqual(expected, actual)

    def test_delete_related_entity(self):
        self.arrange_the_ships_logic.field_for_related_entity[0][0][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][1][0] = 3
        self.arrange_the_ships_logic.field_for_related_entity[0][2][0] = 3

        self.arrange_the_ships_logic.delete_related_entity(0, (0, 0))
        actual = self.arrange_the_ships_logic.get_information_about_all_related_entity()
        expected = []
        self.assertEqual(expected, actual)

    def test_check_possibility_of_placing_the_related_entity_possible(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 0
        related_entity = [(0, 0), (0, 1), (0, 2)]
        actual = self.arrange_the_ships_logic.check_possibility_of_placing_the_related_entity(0, related_entity)
        expected = True
        self.assertEqual(expected, actual)

    def test_check_possibility_of_placing_the_related_entity_impossible(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 1
        related_entity = [(0, 0), (0, 1), (0, 2)]
        actual = self.arrange_the_ships_logic.check_possibility_of_placing_the_related_entity(0, related_entity)
        expected = False
        self.assertEqual(expected, actual)

    def test_checking_the_placement_area_everything_is_available(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 0
        actual = self.arrange_the_ships_logic.checking_the_placement_area(0, 0, 0, 1, 3)
        expected = True
        self.assertEqual(expected, actual)

    def test_checking_the_placement_area_some_are_unavailable_but_area_available(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 0
        self.arrange_the_ships_logic.field_for_related_entity[0][1][0] = 1
        self.arrange_the_ships_logic.field_for_related_entity[0][2][0] = 1
        actual = self.arrange_the_ships_logic.checking_the_placement_area(0, 3, 3, 5, 5)
        expected = True
        self.assertEqual(expected, actual)

    def test_checking_the_placement_area_some_are_unavailable_and_area_unavailable(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 0
        self.arrange_the_ships_logic.field_for_related_entity[0][1][0] = 1
        self.arrange_the_ships_logic.field_for_related_entity[0][2][0] = 1
        actual = self.arrange_the_ships_logic.checking_the_placement_area(0, 0, 0, 2, 2)
        expected = False
        self.assertEqual(expected, actual)

    def test_checking_the_placement_area_some_everything_is_unavailable(self):
        for x in range(10):
            for y in range(10):
                self.arrange_the_ships_logic.field_for_related_entity[0][x][y] = 1
        actual = self.arrange_the_ships_logic.checking_the_placement_area(0, 0, 0, 2, 2)
        expected = False
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
