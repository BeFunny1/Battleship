import unittest

from logic.arrange_the_ships_logic import ArrangeTheShipsLogic


class ArrangeTheShipsLogicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.arrange_the_ships_logic = ArrangeTheShipsLogic()

    def test_calculate_the_number_of_ships_on_the_field(self):
        multiplicities = [1, 2, 2, 5, 10, 20, 40, 81,
                          163, 327, 655, 1310, 2621, 5242,
                          10485, 20971, 41943, 83886, 167772, 335544]
        sizes = [100, 200, 256, 512, 1024, 2048, 4096,
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
            actual = self.arrange_the_ships_logic.calculate_the_number_of_ships_on_the_field(sizes[index])
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
