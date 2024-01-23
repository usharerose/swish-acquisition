"""
Unit tests for logging configurations

Currently, there is no approach to test the log's final output
here only test two points
* msg in log
* no exception when running logger
"""
import logging
from logging import getLevelName
from unittest import TestCase

from swish_acquisition.logging_config import config_logging


class ConfigLogTestCases(TestCase):

    def setUp(self) -> None:
        self.service_name = None
        self.debug = True
        self._logger_name = 'config_log_test_cases_logger'
        self.setup_logging_config()

    def setup_logging_config(self):
        config_logging(self.service_name, self.debug)

    def _get_logger(self):
        self.setup_logging_config()
        return logging.getLogger(self._logger_name)

    def test_plain_info_log(self):
        logger = self._get_logger()
        with self.assertLogs() as captured:
            logger.info('test INFO message')
        self.assertEqual(len(captured.records), 1)

        log_record, *_ = captured.records
        self.assertEqual(log_record.levelname, getLevelName(logging.INFO))
        self.assertEqual(log_record.getMessage(), 'test INFO message')

    def test_plain_exc_log(self):
        logger = self._get_logger()
        with self.assertLogs() as captured:
            try:
                raise Exception
            except:  # NOQA
                logger.exception('test ERROR level message')
        self.assertEqual(len(captured.records), 1)

        log_record, *_ = captured.records
        self.assertEqual(log_record.levelname, getLevelName(logging.ERROR))
        self.assertEqual(log_record.getMessage(), 'test ERROR level message')
        self.assertIn('Traceback (most recent call last)', log_record.exc_text)

    def test_console_info_log(self):
        self.debug = False
        logger = self._get_logger()
        with self.assertLogs() as captured:
            logger.info('test INFO message')
        self.assertEqual(len(captured.records), 1)

        log_record, *_ = captured.records
        self.assertEqual(log_record.levelname, getLevelName(logging.INFO))
        self.assertEqual(log_record.getMessage(), 'test INFO message')

    def test_console_exc_log(self):
        self.debug = False
        logger = self._get_logger()
        with self.assertLogs() as captured:
            try:
                raise Exception
            except:  # NOQA
                logger.exception('test ERROR level message')
        self.assertEqual(len(captured.records), 1)

        log_record, *_ = captured.records
        self.assertEqual(log_record.levelname, getLevelName(logging.ERROR))
        self.assertEqual(log_record.getMessage(), 'test ERROR level message')
        self.assertIn('Traceback (most recent call last)', log_record.exc_text)

    def test_console_with_service_name(self):
        self.debug = False
        self.service_name = 'test-logging-service'
        logger = self._get_logger()
        with self.assertLogs() as captured:
            logger.info('test INFO message')
        self.assertEqual(len(captured.records), 1)

        log_record, *_ = captured.records
        self.assertEqual(log_record.levelname, getLevelName(logging.INFO))
        self.assertEqual(log_record.getMessage(), 'test INFO message')
