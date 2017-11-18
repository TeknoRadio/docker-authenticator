import datetime
from unittest import TestCase
from authenticator.index import Users
from tests import time_plus_two, time_minus_two


class UsersTestCase(TestCase):
    def setUp(self):
        self.users = Users(filename='authenticator/.users.yml')

    def test_that_get_attr_returns_attr_when_found(self):
        self.assertEqual(self.users.get_attr('administrator', 'password'), 'some_pass')

    def test_that_get_attr_returns_none_when_user_or_attr_not_found(self):
        self.assertIsNone(self.users.get_attr('administrator', 'pssword'))
        self.assertIsNone(self.users.get_attr('tor', 'password'))

    def test_that_password_returns_a_password_when_found(self):
        self.assertEqual(self.users.password('administrator'), 'some_pass')

    def test_that_password_returns_none_when_password_or_user_not_found(self):
        self.assertIsNone(self.users.password('tor'))

    def test_that_timeslot_returns_timeslot_when_present(self):
        self.users['some_user'] = {
            "timeslot": '22:00|23:00'
        }
        self.assertEqual(self.users.timeslot('some_user'), '22:00|23:00')

    def test_that_timeslot_returns_24_hour_timeslot_when_value_is_always(self):
        self.users['some_user'] = {
            "timeslot": 'always',
        }
        self.assertEqual(self.users.timeslot('some_user'), '00:00|23:59')

    def test_that_dateslot_returns_timeslot_when_present(self):
        self.users['some_user'] = {
            "dateslot": '1-1-1970|1-2-1970',
        }
        self.assertEqual(self.users.dateslot('some_user'), '1-1-1970|1-2-1970')

    def test_that_dateslot_returns_5000_year_timeslot_when_value_is_always(self):
        self.users['some_user'] = {
            "dateslot": 'always',
        }
        self.assertEqual(self.users.dateslot('some_user'), '11-09-1982|11-09-6982')

    def test_that_start_time_returns_a_combination_of_the_first_time_and_date_field_in_dict(self):
        self.users['some_user'] = {
            "dateslot": '1-1-1970|1-2-1970',
            "timeslot": '22:00|23:00'
        }
        self.assertEqual(self.users.start_time('some_user'), datetime.datetime(1970, 1, 1, 22, 0))

    def test_that_stop_time_returns_a_combination_of_the_second_time_and_date_field_in_dict(self):
        self.users['some_user'] = {
            "dateslot": '1-1-1970|1-2-1970',
            "timeslot": '22:00|23:00'
        }
        self.assertEqual(self.users.stop_time('some_user'), datetime.datetime(1970, 2, 1, 23, 0))

    def test_that_validate_user_returns_false_by_default(self):
        self.users['some_user'] = {
            "password": "pass",
            "dateslot": '',
            "timeslot": ''
        }
        self.assertFalse(self.users.validate_user('some_user', 'pass'))

    def test_that_post_request_from_always_allowed_returns_true(self):
        self.users['some_user'] = {
            "password": "pass",
            "dateslot": 'always',
            "timeslot": 'always'
        }
        self.assertTrue(self.users.validate_user('some_user', 'pass'))

    def test_that_post_request_from_history_returns_false(self):
        self.users['some_user'] = {
            "password": "pass",
            "dateslot": '1-1-1970|1-2-1970',
            "timeslot": '22:00|23:00'
        }
        self.assertFalse(self.users.validate_user('some_user', 'pass'))

    def test_that_post_request_in_future_forbidden_returns_false(self):
        self.users['some_user'] = {
            "password": "pass",
            "dateslot": '1-1-5000|1-2-5021',
            "timeslot": '22:00|23:00'
        }
        self.assertFalse(self.users.validate_user('some_user', 'pass'))

    def test_that_post_request_from_timeslot_not_allowed_returns_false(self):
        self.users['some_user'] = {
            "password": "pass",
            "dateslot": '1-1-5000|1-2-5021',
            "timeslot": '22:00|23:00'
        }
        self.assertFalse(self.users.validate_user('some_user', 'pass'))

    def test_that_post_request_from_timeslot_allowed_returns_true(self):
        self.users['some_user'] = {
            "password": "pass",
            "timeslot": '{}|{}'.format(time_minus_two.strftime('%H:%M'), time_plus_two.strftime('%H:%M')),
            "dateslot": '{}|{}'.format(time_plus_two.strftime('%d-%m-%Y'), time_plus_two.strftime('%d-%m-%Y')),
        }
        self.assertTrue(self.users.validate_user('some_user', 'pass'))
