import unittest
from program import azimuth


def are_floats_close(a, b, relative_difference):
    if abs(a) > 0.00001 and abs(b) > 0.00001:
        d1 = abs(1 - a / b)
        d2 = abs(1 - b / a)
        return d1 < relative_difference or d2 < relative_difference
    else:
        return a == b


class Test_azimuth(unittest.TestCase):
    def test_simple_north(self):
        a = azimuth(0, 0, 0, 1)
        self.assertTrue(are_floats_close(a, 0, 0.01)) #ok; przeciez d2=1-az/0 jak to przeszlo?

    def test_simple_west(self):
        a = azimuth(0, 0, -1, 0)
        self.assertTrue(are_floats_close(a, 270, 0.01)) 

    def test_simple_east(self):
        a = azimuth(0, 0, 1, 0) 
        self.assertTrue(are_floats_close(a, 90, 0.01))

    def test_simple_south(self):
        a = azimuth(0, 0, 0, -1)
        self.assertTrue(are_floats_close(a, 180, 0.01))

    def test_simple_north_west(self):
        a = azimuth(0, 0, -1, 1)
        self.assertTrue(are_floats_close(a, 315, 0.01))

    def test_simple_south_west(self):
        a = azimuth(0, 0, -1, -1)
        self.assertTrue(are_floats_close(a, 225, 0.01))

    def test_simple_north_east(self):
        a = azimuth(0, 0, 1, 1)
        self.assertTrue(are_floats_close(a, 45, 0.01)) #ok

    def test_simple_south_east(self):
        a = azimuth(0, 0, 1, -1)
        self.assertTrue(are_floats_close(a, 135, 0.01))

if __name__ == '__main__':
    unittest.main()

