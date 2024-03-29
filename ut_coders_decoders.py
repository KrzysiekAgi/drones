import unittest
from message_coders_decoders import rotate_to_position_msg, move_up_down_msg
from message_coders_decoders import get_position_msg, sleep_msg
from message_coders_decoders import enable_device_msg, decode_tilt_msg
from message_coders_decoders import decode_gprmc_msg, gprmc_position
from message_coders_decoders import nmea_latitude_to_degrees
from message_coders_decoders import nmea_longitude_to_degrees
from message_coders_decoders import gprmc_position_request


class Test_gprmc_position_request(unittest.TestCase):
    def test_basic(self):
        message = gprmc_position_request()
        self.assertEqual(message, "$OGPRMC\n")


class Test_rotate_to_position_msg(unittest.TestCase):
    def test_move_to_zero(self):
        message = rotate_to_position_msg("00", 0)
        self.assertEqual(message, "$O00W0\n")

    def test_move_to_plus_position(self):
        message = rotate_to_position_msg("00", 1000)
        self.assertEqual(message, "$O00W+1000\n")

    def test_move_to_minus_position(self):
        message = rotate_to_position_msg("00", -1000)
        self.assertEqual(message, "$O00W-1000\n")

    def test_move_to_max_minus_position(self):
        message = rotate_to_position_msg("00", -32000)
        self.assertEqual(message, "$O00W-32000\n")

    def test_move_to_max_plus_position(self):
        message = rotate_to_position_msg("00", 32000)
        self.assertEqual(message, "$O00W+32000\n")

    def test_move_to_below_min_range(self):
        self.assertRaises(TypeError,
                          rotate_to_position_msg, "00", -32001)

    def test_move_to_above_max_range(self):
        self.assertRaises(TypeError,
                          rotate_to_position_msg, "00", 32001)

    def test_device_address(self):
        self.assertRaises(TypeError,
                          rotate_to_position_msg, "123", 0)


class Test_move_up_down_msg(unittest.TestCase):
    def test_move_up(self):
        message = move_up_down_msg("00", 32000)
        self.assertEqual(message, "$O00U32000\n")

    def test_move_down(self):
        message = move_up_down_msg("00", -32000)
        self.assertEqual(message, "$O00D32000\n")

    def test_move_below_min_range(self):
        self.assertRaises(TypeError,
                          move_up_down_msg, "00", -32001)

    def test_move_above_max_range(self):
        self.assertRaises(TypeError,
                          move_up_down_msg, "00", 32001)

    def test_device_address(self):
        self.assertRaises(TypeError,
                          move_up_down_msg, "aaa", "12")


class Test_query_position_msg(unittest.TestCase):
    def test_msg(self):
        self.assertEqual(get_position_msg("00"), "$O00R\n")

    def test_device_address(self):
        self.assertRaises(TypeError,
                          get_position_msg, "aaa", "12")


class Test_query_sleep_msg(unittest.TestCase):
    def test_msg(self):
        self.assertEqual(sleep_msg("00"), "$O00S\n")

    def test_device_address(self):
        self.assertRaises(TypeError,
                          sleep_msg, "aaa")


class Test_query_enable_msg(unittest.TestCase):
    def test_msg(self):
        self.assertEqual(enable_device_msg("00"), "$O00E\n")

    def test_device_address(self):
        self.assertRaises(TypeError,
                          enable_device_msg, "aaa")


class Test_decode_position_msg(unittest.TestCase):
    def test_negative(self):
        result = decode_tilt_msg("$O00R-2380\n")
        self.assertEqual(result, -2380)

    def test_positive(self):
        result = decode_tilt_msg("$O00R+2380\n")
        self.assertEqual(result, 2380)

    def test_malformed_message(self):
        self.assertRaises(ValueError,
                          decode_tilt_msg,
                          "$O00R+2380a\n")


class Test_decode_gprmc_msg(unittest.TestCase):
    def test_simple(self):
        msg = "$GPRMC,220516,A,5133.8200,N,00042.2400,W,173.8,231.8,130694,004.2,W*70\n"
        result = decode_gprmc_msg(msg)
        expected = gprmc_position(51.5636, -0.704, 231.8, 004.2, "A")
        self.assertEqual(result, expected)

    def test_void_message(self):
        msg = "$$GPRMC,215656.086,V,,,,,0.00,0.00,010816,,,N*4E:159.7,1,-1\n"
        result = decode_gprmc_msg(msg)
        expected = gprmc_position(0, 0, 0, 0, "V")
        self.assertEqual(result, expected)

    def test_start_checking_checksum(self):
        self.assertFalse(True)  # add more test to this class

    def test_task(self):
        self.assertFalse(True)  # add more test to this class


class Test_decode_nmea_latitude(unittest.TestCase):
    def test_just_degrees_north(self):
        result = nmea_latitude_to_degrees("1100.0000", "N")
        self.assertAlmostEqual(result, 11)

    def test_just_degrees_south(self):
        result = nmea_latitude_to_degrees("1100.0000", "S")
        self.assertAlmostEqual(result, -11)

    def test_just_degrees_south_with_minutes(self):
        result = nmea_latitude_to_degrees("1122.3333", "S")
        self.assertAlmostEqual(result, -(11 + 22.3333 / 60))

    def test_just_degrees_north_with_minutes(self):
        result = nmea_latitude_to_degrees("1122.3333", "N")
        self.assertAlmostEqual(result, (11 + 22.3333 / 60))

    def test_wrong_string_degrees_short(self):
        self.assertRaises(TypeError,
                          nmea_latitude_to_degrees, "122.3333", "N")

    def test_wrong_string__minutes_short(self):
        self.assertRaises(TypeError,
                          nmea_latitude_to_degrees, "1122.333", "N")

    def test_wrong_string_bad_direction(self):
        self.assertRaises(TypeError,
                          nmea_latitude_to_degrees, "1122.3333", "sdf")


class Test_decode_nmea_longitude(unittest.TestCase):
    def test_just_degrees_north(self):
        result = nmea_longitude_to_degrees("11100.0000", "E")
        self.assertAlmostEqual(result, 111)

    def test_just_degrees_south(self):
        result = nmea_longitude_to_degrees("11100.0000", "W")
        self.assertAlmostEqual(result, -111)

    def test_just_degrees_west_with_minutes(self):
        result = nmea_longitude_to_degrees("11122.3333", "W")
        self.assertAlmostEqual(result, -(111 + 22.3333 / 60))

    def test_just_degrees_east_with_minutes(self):
        result = nmea_longitude_to_degrees("11122.3333", "E")
        self.assertAlmostEqual(result, (111 + 22.3333 / 60))

    def test_wrong_string_degrees_short(self):
        self.assertRaises(TypeError,
                          nmea_longitude_to_degrees, "122.3333", "W")

    def test_wrong_string__minutes_short(self):
        self.assertRaises(TypeError,
                          nmea_longitude_to_degrees, "11122.333", "W")

    def test_wrong_string_bad_direction(self):
        self.assertRaises(TypeError,
                          nmea_longitude_to_degrees, "1122.3333", "N")


if __name__ == '__main__':
    unittest.main()
