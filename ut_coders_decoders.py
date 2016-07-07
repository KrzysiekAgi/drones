import unittest
from message_coders_decoders import rotate_to_position_msg, move_up_down_msg


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


class Test_move_up_down_msg(unittest.TestCase):
    def test_move_up(self):
        message = move_up_down_msg("00", 32000)
        self.assertEqual(message, "$O00U+00100\n")

    def test_move_down(self):
        message = move_up_down_msg("00", -3200)
        self.assertEqual(message, "$O00U+00100\n")

    def test_move_below_min_range(self):
        self.assertRaises(NameError("position_out_of_range"),
                          move_up_down_msg, "00", -32001)

    def test_move_above_max_range(self):
        self.assertRaises(NameError("position_out_of_range"),
                          move_up_down_msg, "00", 32001)

    def test_device_address(self):
        self.assertRaises(NameError("wrong_device_address"),
                          move_up_down_msg, "aaa", "12")


if __name__ == '__main__':
    unittest.main()
