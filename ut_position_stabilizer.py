import position_stabilizer
import unittest


class Test_stabilizer(unittest.TestCase):
    def test_simple(self):
        p = position_stabilizer.position_stabilizer(10, 10)
        self.assertFalse(p.is_ready())

    def test_not_enough_measurments(self):
        l = {"lat": 0, "lon": 0}
        p = position_stabilizer.position_stabilizer(10, 10)
        p.add_measurment(l["lat"], l["lon"])
        self.assertFalse(p.is_ready())

    def test_enough_measurments(self):
        l = {"lat": 45.4545, "lon": 134.324234}
        p = position_stabilizer.position_stabilizer(10, 10)

        for r in range(1,15):
            p.add_measurment(l["lat"], l["lon"])

        calculated = p.get_position()
        self.assertTrue(p.is_ready())
        self.assertAlmostEqual(calculated["lat"], l["lat"])
        self.assertAlmostEqual(calculated["lon"], l["lon"])

    def test_bad_accuracy(self):
        l = {"lat": 0, "lon": 0}
        p = position_stabilizer.position_stabilizer(10, 10)

        for r in range(1,15):
            p.add_measurment(p, p)

        self.assertFalse(p.is_ready())

if __name__ == '__main__':
    unittest.main()