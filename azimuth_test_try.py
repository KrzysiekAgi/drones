import unittest
from math import radians
from azimuth_try import azimuth

class Test_azimuth(unittest.TestCase):
    def test_north_PL(self):
        a = azimuth(51, 17, 51.1, 17)
        self.assertAlmostEqual(a, 0, 1)

    def test_north_PL_2(self):
        a = azimuth(51, 17, 52, 17)
        self.assertAlmostEqual(a, 0, 1)

    def test_east_PL(self):
        a = azimuth(51, 17, 51, 17.1)
        self.assertAlmostEqual(a, 90, 1) 

    def test_simple_north(self):
        a = azimuth(0, 0, 0.1, 0)
        self.assertAlmostEqual(a, 0, 1)

    def test_simple_west(self):
        a = azimuth(0, 0, 0, -0.1)
        self.assertAlmostEqual(a, 270, 1)

    def test_simple_east(self):
        a = azimuth(0, 0, 0, 0.0000001)
        self.assertAlmostEqual(a, 90, 1)

    def test_simple_south(self):
        a = azimuth(0, 0, -0.1, 0)
        self.assertAlmostEqual(a, 180, 1)

    def test_simple_north_west(self):
        a = azimuth(0, 0, 0.1, -0.1)
        self.assertAlmostEqual(a, 315, 1)

    def test_simple_south_west(self):
        a = azimuth(0, 0, -0.1, -0.1)
        self.assertAlmostEqual(a, 225, 1)

    def test_simple_north_east(self):
        a = azimuth(0, 0, 0.00001, 0.00001)
        self.assertAlmostEqual(a, 45, 1)

    def test_simple_south_east(self):
        a = azimuth(0, 0, -0.1, 0.1)
        self.assertAlmostEqual(a, 135, 1)

    def test_simple_debug3(self):
        a = azimuth(0, 0, 0, 0.00000001)
        self.assertAlmostEqual(a, 90, 1)

    def test_simple_debug2(self):
        a = azimuth(51.0, 17.0, 51.0, 17.000000001)
        self.assertAlmostEqual(a, 135, 1)

    #def test_simple_debug(self):
        #a = azimuth(51.1017933333, 17.08882, 51.1018308, 17.0887996)
        #self.assertAlmostEqual(a, 315, 1)


if __name__ == '__main__':
	unittest.main()