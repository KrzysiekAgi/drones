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
        self.assertAlmostEqual(a, 0, 4)

    def test_simple_west(self):
        a = azimuth(0, 0, -0.1, 0)
        self.assertAlmostEqual(a, 270, 4)

    def test_simple_east(self):
        a = azimuth(0, 0, 0.1, 0)
        self.assertAlmostEqual(a, 90, 4)

    def test_simple_south(self):
        a = azimuth(0, 0, 0, -0.1)
        self.assertAlmostEqual(a, 180, 4)

    def test_simple_north_west(self):
        a = azimuth(0, 0, -0.1, 0.1)
        self.assertAlmostEqual(a, 315, 4)

    def test_simple_south_west(self):
        a = azimuth(0, 0, -0.1, -0.1)
        self.assertAlmostEqual(a, 225, 4)

    def test_simple_north_east(self):
        a = azimuth(0, 0, 0.1, 0.1)
        self.assertAlmostEqual(a, 45, 4)

    def test_simple_south_east(self):
        a = azimuth(0, 0, 0.1, -0.1)
        self.assertAlmostEqual(a, 135, 4)


class Test_elevation_calculation(unittest.TestCase):
    def test_above(self):
        result = elevation(0, 0, 0, 0, 0, 100)
        self.assertAlmostEqual(result, 90)

    def test_below(self):
        result = elevation(0, 0, 0, 0, 0, -100)
        self.assertAlmostEqual(result, -90)

    def test_different_site_of_earth(self):
        result = elevation(0, 0, 0, 0, 180, 0)
        self.assertAlmostEqual(result, -90)

    def test_different_site_of_earth_height_does_not_matter(self):
        result = elevation(0, 0, 0, 0, 180, 150)
        self.assertAlmostEqual(result, -90)

    def test_zero_degrees_elevation(self):
        result = elevation(0, 0, 0, 45, 0, 2638.954605879 * 1000)
        self.assertAlmostEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
