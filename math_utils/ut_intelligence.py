import unittest
from intelligence import where_to_move_relative, where_to_move_absolute


class Test_where_to_move_relative(unittest.TestCase):
    def test_zero(self):
        r = where_to_move_relative(0, 0)
        self.assertAlmostEqual(r, 0, 5)

    def test_one(self):
        r = where_to_move_relative(1, 0)
        self.assertAlmostEqual(r, 1, 5)

    def test_minus_one(self):
        r = where_to_move_relative(-1, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_359(self):
        r = where_to_move_relative(359, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_1(self):
        r = where_to_move_relative(1, 359)
        self.assertAlmostEqual(r, 2, 5)

    def test_180(self):
        r = where_to_move_relative(90, -90)
        self.assertAlmostEqual(r, 180, 5)


class Test_where_to_move_absolute(unittest.TestCase):
    def test_zero(self):
        r = where_to_move_absolute(0, 0)
        self.assertAlmostEqual(r, 0, 5)

    def test_one(self):
        r = where_to_move_absolute(1, 0)
        self.assertAlmostEqual(r, 1, 5)

    def test_minus_one(self):
        r = where_to_move_absolute(-1, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_359(self):
        r = where_to_move_absolute(359, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_1(self):
        r = where_to_move_absolute(1, 359)
        self.assertAlmostEqual(r, 361, 5)

    def test_180(self):
        r = where_to_move_absolute(90, -90)
        self.assertAlmostEqual(r, -270, 5)

    def test_far_more(self):
        r = where_to_move_absolute(5, 720)
        self.assertAlmostEqual(r, 725, 5)


if __name__ == '__main__':
    unittest.main()

