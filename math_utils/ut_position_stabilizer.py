from position_stabilizer import position_stabilizer, remove_big_errors
from position_stabilizer import clac_error_and_pos
import unittest


class Test_stabilizer(unittest.TestCase):
    def test_simple(self):
        p = position_stabilizer(10, 10)
        self.assertFalse(p.is_ready())

    def test_not_enough_measurments(self):
        l = {"lat": 0, "lon": 0}
        p = position_stabilizer(10, 10)
        p.add_measurment(l["lat"], l["lon"])
        self.assertFalse(p.is_ready())

    def test_enough_measurments(self):
        l = {"lat": 45.4545, "lon": 134.324234}
        p = position_stabilizer(10, 10)

        for r in range(1, 15):
            p.add_measurment(l["lat"], l["lon"])

        calculated = p.get_position()
        self.assertTrue(p.is_ready())
        self.assertAlmostEqual(calculated["lat"], l["lat"])
        self.assertAlmostEqual(calculated["lon"], l["lon"])

    def test_bad_accuracy(self):
        p = position_stabilizer(10, 10)

        for r in range(1, 15):
            p.add_measurment(r, r)

        self.assertFalse(p.is_ready())

    def test_good_accuracy(self):
        p = position_stabilizer(10, 10)

        meters_1 = 0.0000089949
        for r in range(-6, 6):
            p.add_measurment(r * meters_1, r * meters_1)

        self.assertTrue(p.is_ready())

    def test_sdfsdf_accuracy(self):
        p = position_stabilizer(10, 10)

        meters_1 = 0.0000089949 * 0.01
        for r in range(-20, 20):
            p.add_measurment(r * meters_1, r * meters_1)

        p.add_measurment(90, 90)
        self.assertTrue(p.is_ready())


class Test_remove_big_errors(unittest.TestCase):
    def test_nothing_removed(self):
        m_list = []

        for i in range(0, 10):
            m_list.append({"lat": 0, "lon": 0})

        result = remove_big_errors(m_list)
        self.assertEqual(m_list, result)

    def test_one_removed(self):
        m_list = []

        for i in range(0, 10):
            m_list.append({"lat": 0, "lon": 0})

        m_list_error = m_list[:]
        m_list_error.append({"lat": 10, "lon": 10})
        result = remove_big_errors(m_list_error)
        self.assertEqual(m_list, result)

    def test_simple2(self):
        m_list = []
        l = {"lat": 45.4545, "lon": 134.324234}

        for r in range(1, 15):
            m_list.append(l)

        result = remove_big_errors(m_list)
        self.assertEqual(m_list, result)

    def test_simple3(self):
        m_list = [{'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234}]

        result = remove_big_errors(m_list)
        self.assertEqual(m_list, result)


class Test_calc_errors(unittest.TestCase):
    def test_simple(self):
        m_list = [{'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234},
                  {'lat': 45.4545, 'lon': 134.324234}]
        r = clac_error_and_pos(m_list)
        self.assertAlmostEqual(r["lat"], 45.4545)
        self.assertAlmostEqual(r["lon"], 134.324234)
        self.assertAlmostEqual(r["err"], 0, 8)

if __name__ == '__main__':
    unittest.main()
