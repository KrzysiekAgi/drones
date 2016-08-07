import unittest
from intelligence import where_to_move


class Test_where_to_move(unittest.TestCase):
    def test_zero(self):
        r = where_to_move(0, 0)
        self.assertAlmostEqual(r, 0, 5)

    def test_one(self):
        r = where_to_move(1, 0)
        self.assertAlmostEqual(r, 1, 5)

    def test_minus_one(self):
        r = where_to_move(-1, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_359(self):
        r = where_to_move(359, 0)
        self.assertAlmostEqual(r, -1, 5)

    def test_1(self):
        r = where_to_move(1, 359)
        self.assertAlmostEqual(r, 2, 5)

    def test_180(self):
        r = where_to_move(90, -90)
        self.assertAlmostEqual(r, 180, 5)

if __name__ == '__main__':
    unittest.main()