import unittest
from frequency_lock import frequency_lock
import time


class Test_frequency_lock(unittest.TestCase):
    def test_simple_can(self):
        l = frequency_lock(0.1)
        time.sleep(0.2)
        for i in range(0, 5):
            self.assertTrue(l.can_act())
            time.sleep(0.2)

    def test_cant(self):
        l = frequency_lock(1)
        time.sleep(0.2)
        for i in range(0, 5):
            self.assertFalse(l.can_act())
            time.sleep(0.1)

if __name__ == '__main__':
    unittest.main()