import unittest
from program import azimuth, elevation


def are_floats_close(a, b, relative_difference):
    if abs(a) > 0.00001 and abs(b) > 0.00001:
        d1 = abs(1 - a / b)
        d2 = abs(1 - b / a)
        return d1 < relative_difference or d2 < relative_difference
    else:
        return a == b


class Test_azimuth(unittest.TestCase):
    def test_simple_north(self):
        a = azimuth(0, 0, 0, 0.1)
        self.assertAlmostEqual(a, 0)

    def test_simple_west(self):
        a = azimuth(0, 0, -0.1, 0)
        self.assertAlmostEqual(a, 270)

    def test_simple_east(self):
        a = azimuth(0, 0, 0.1, 0)
        self.assertAlmostEqual(a, 90)

    def test_simple_south(self):
        a = azimuth(0, 0, 0, -0.1)
        self.assertAlmostEqual(a, 180)

    def test_simple_north_west(self):
        a = azimuth(0, 0, -0.1, 0.1)
        self.assertAlmostEqual(a, 315)

    def test_simple_south_west(self):
        a = azimuth(0, 0, -0.1, -0.1)
        self.assertAlmostEqual(a, 225)

    def test_simple_north_east(self):
        a = azimuth(0, 0, 0.1, 0.1)
        self.assertAlmostEqual(a, 45)

    def test_simple_south_east(self):
        a = azimuth(0, 0, 0.1, -0.1)
        self.assertAlmostEqual(a, 135)

class Test_elevation_calculation(unittest.TestCase):
    def test_above(self):
        pass

if __name__ == '__main__':
    unittest.main()

