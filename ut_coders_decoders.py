import unittest
from message_coders_decoders import rotate_to_position_msg


class Test_rotate_to_position_msg(unittest.TestCase):
    def test_move_to_zero(self):
        message = rotate_to_position_msg("00", 0)
        self.assertEqual(message, "$O00W+00000\n")

    def test_move_to_plus_position(self):
        message = rotate_to_position_msg("00", 1000)
        self.assertEqual(message, "$O00W+01000\n")

    def test_move_to_minus_position(self):
        message = rotate_to_position_msg("00", -1000)
        self.assertEqual(message, "$O00W-01000\n")

    def test_move_to_max_minus_position(self):
        message = rotate_to_position_msg("00", -32000)
        self.assertEqual(message, "$O00W-32000\n")

    def test_move_to_max_plus_position(self):
        message = rotate_to_position_msg("00", -32000)
        self.assertEqual(message, "$O00W+32000\n")

    def test_move_to_below_min_range(self):
        self.assertRaises(NameError("position_out_of_range"),
                          rotate_to_position_msg, "00", -32001)

    def test_move_to_above_max_range(self):
        self.assertRaises(NameError("position_out_of_range"),
                          rotate_to_position_msg, "00", 32001)

    def test_device_address(self):
        self.assertRaises(NameError("wrong_device_address"),
                          rotate_to_position_msg, "123", 0)

if __name__ == '__main__':
    unittest.main()
