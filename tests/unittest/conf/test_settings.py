"""
unittest for Settings object
"""
import os
from unittest import TestCase

from swish_acquisition.conf import (
    ENVIRONMENT_VARIABLE,
    settings
)


class SettingsTestCases(TestCase):

    def setUp(self) -> None:
        os.environ[ENVIRONMENT_VARIABLE] = 'tests.unittest.conf.settings_local'
        settings._setup()
        super().setUpClass()

    def tearDown(self) -> None:
        del os.environ[ENVIRONMENT_VARIABLE]
        settings._setup()
        super().tearDownClass()

    def test_no_settings_module(self):
        """
        Would load default settings module 'settings'
        when no specific module declared by environment variable
        """
        self.assertEqual(str(settings),
                         '<Settings "tests.unittest.conf.settings_local">')

        original_settings = os.environ[ENVIRONMENT_VARIABLE]
        del os.environ[ENVIRONMENT_VARIABLE]
        try:
            settings._setup()
            self.assertEqual(str(settings),
                             '<Settings "swish_acquisition.settings">')
        finally:
            os.environ[ENVIRONMENT_VARIABLE] = original_settings
            settings._setup()

    def test_clean_when_resetup(self):
        """
        Settings key 'NONEXISTENT_SETTING' only exists in settings_local module
        which is only for test case
        """
        self.assertEqual(settings.NONEXISTENT_SETTING,
                         'Only for case '
                         '"tests.unittest.conf.test_settings::SettingsTestCases::test_clean_when_resetup"')

        original_settings = os.environ[ENVIRONMENT_VARIABLE]
        del os.environ[ENVIRONMENT_VARIABLE]
        try:
            settings._setup()
            with self.assertRaises(AttributeError):
                getattr(settings, 'NONEXISTENT_SETTING')
        finally:
            os.environ[ENVIRONMENT_VARIABLE] = original_settings
            settings._setup()

    def test_undeclared_settings(self):
        with self.assertRaises(AttributeError):
            getattr(settings, 'UNAVAILABLE_SETTING')

    def test_boolean_value(self):
        self.assertTrue(settings.DEBUG)

    def test_boolean_value_from_env(self):
        os.environ['DEBUG'] = 'False'
        settings._setup()

        try:
            self.assertFalse(settings.DEBUG)
        finally:
            del os.environ['DEBUG']
            settings._setup()

    def test_positive_boolean_value_from_env(self):
        os.environ['TEST'] = 'True'
        settings._setup()

        try:
            self.assertTrue(settings.TEST)
        finally:
            del os.environ['TEST']
            settings._setup()

    def test_invalid_boolean_value_from_env(self):
        os.environ['TEST'] = 'invalid_boolean'

        try:
            with self.assertRaises(ValueError) as cxt_manager:
                settings._setup()
            expected_exc_msg = (
                'Invalid input [invalid_boolean] converted to boolean'
            )
            self.assertIn(expected_exc_msg, str(cxt_manager.exception))
        finally:
            del os.environ['TEST']
            settings._setup()

    def test_int_value(self):
        expected = 60
        self.assertEqual(settings.THRESHOLD, expected)

    def test_int_value_from_env(self):
        os.environ['THRESHOLD'] = '120'
        settings._setup()

        try:
            self.assertEqual(settings.THRESHOLD, 120)
        finally:
            del os.environ['THRESHOLD']
            settings._setup()

    def test_float_value(self):
        expected = 3.1415927
        self.assertAlmostEqual(settings.PI, expected)

    def test_float_value_from_env(self):
        os.environ['PI'] = '3.14'
        settings._setup()

        try:
            self.assertEqual(settings.PI, 3.14)
        finally:
            del os.environ['PI']
            settings._setup()

    def test_string_value(self):
        expected = 'https://httpbin.org/'
        self.assertEqual(settings.HTTP_SERVICE, expected)

    def test_string_value_from_env(self):
        os.environ['HTTP_SERVICE'] = 'https://kennethreitz.org/'
        settings._setup()

        try:
            self.assertEqual(settings.HTTP_SERVICE, 'https://kennethreitz.org/')
        finally:
            del os.environ['HTTP_SERVICE']
            settings._setup()

    def test_dict_value(self):
        expected = {
            'ENGINE': 'postgres',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': 5432
        }
        self.assertDictEqual(settings.DATABASES['default'], expected)

    def test_dict_value_from_env(self):
        os.environ['DATABASES_DEFAULT_ENGINE'] = 'mysql'
        os.environ['DATABASES_DEFAULT_NAME'] = 'testcasedb'
        os.environ['DATABASES_DEFAULT_USER'] = 'fakeuser'
        os.environ['DATABASES_DEFAULT_PASSWORD'] = '20220922'
        os.environ['DATABASES_DEFAULT_HOST'] = '255.255.255.255'
        os.environ['DATABASES_DEFAULT_PORT'] = '5434'
        settings._setup()

        try:
            expected = {
                'ENGINE': 'mysql',
                'NAME': 'testcasedb',
                'USER': 'fakeuser',
                'PASSWORD': '20220922',
                'HOST': '255.255.255.255',
                'PORT': 5434
            }
            self.assertDictEqual(settings.DATABASES['default'], expected)
        finally:
            del os.environ['DATABASES_DEFAULT_ENGINE']
            del os.environ['DATABASES_DEFAULT_NAME']
            del os.environ['DATABASES_DEFAULT_USER']
            del os.environ['DATABASES_DEFAULT_PASSWORD']
            del os.environ['DATABASES_DEFAULT_HOST']
            del os.environ['DATABASES_DEFAULT_PORT']
            settings._setup()

    def test_list_value(self):
        expected = [
            'mock@demoemail.com',
            'fake@demoemail.com'
        ]
        self.assertListEqual(settings.EMAILS, expected)

    def test_list_value_from_env(self):
        os.environ['EMAILS'] = '["mock_env@demoemail.com", "fake_env@demoemail.com"]'
        settings._setup()
        try:
            expected = [
                'mock_env@demoemail.com',
                'fake_env@demoemail.com'
            ]
            self.assertListEqual(settings.EMAILS, expected)
        finally:
            del os.environ['EMAILS']
            settings._setup()

    def test_unmatched_data_type(self):
        os.environ['THRESHOLD'] = 'invalid_threshold_value_type_as_string'
        try:
            with self.assertRaises(ValueError):
                settings._setup()
        finally:
            del os.environ['THRESHOLD']
            settings._setup()

    def test_setting_key_exceed_max_length(self):
        original_settings = os.environ[ENVIRONMENT_VARIABLE]
        os.environ[ENVIRONMENT_VARIABLE] = 'tests.unittest.conf.settings_with_long_keys'
        try:
            with self.assertRaises(ValueError) as cxt_manager:
                settings._setup()
            expected_exc_msg = (
                'The length of environment key '
                '[THIS_IS_A_VERY_LONG_CHARACTER_AS_SETTING_KEY_'
                'IT_IS_DIFFICULT_TO_COMPOSE_TOO_MANY_CHARACTERS_AS_VARIA ...] '
                'should be less than 100')
            self.assertIn(expected_exc_msg, str(cxt_manager.exception))
        finally:
            os.environ[ENVIRONMENT_VARIABLE] = original_settings
            settings._setup()

    def test_invalid_list_env_value(self):
        os.environ['EMAILS'] = 'mock_env@demoemail.com,fake_env@demoemail.com'
        try:
            with self.assertRaises(ValueError) as cxt_manager:
                settings._setup()
            expected_exc_msg = (
                'Value of environment variable [EMAILS] is not an illegal JSON array'
            )
            self.assertIn(expected_exc_msg, str(cxt_manager.exception))
        finally:
            del os.environ['EMAILS']
            settings._setup()

    def test_invalid_json_array_env_value(self):
        os.environ['EMAILS'] = '{"EMAILS":["mock_env@demoemail.com","fake_env@demoemail.com"]}'
        try:
            with self.assertRaises(ValueError) as cxt_manager:
                settings._setup()
            expected_exc_msg = (
                'Value of environment variable [EMAILS] is not an illegal JSON array'
            )
            self.assertIn(expected_exc_msg, str(cxt_manager.exception))
        finally:
            del os.environ['EMAILS']
            settings._setup()
