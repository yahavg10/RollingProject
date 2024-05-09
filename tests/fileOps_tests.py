import logging
import os
import unittest
from unittest.mock import MagicMock, patch

from utils import calculate_md5, update_cache
from utils.cache_utils import extract_file_hashes, is_md5_match
from utils.logger_utils import create_handler, setup_custom_logger


class TestFileOperations(unittest.TestCase):

    def test_calculate_md5_givenFilePath_returnsMD5Hash(self):
        file_path = "test_file.txt"
        os.stat = MagicMock(return_value=os.stat_result((100, 1234567890, 0, 0, 0, 0, 0)))
        expected_md5 = "098f6bcd4621d373cade4e832627b4f6"
        self.assertEqual(calculate_md5(file_path), expected_md5)

    # noinspection PyTypeChecker
    def test_update_cache_givenLoadMethodAndCacheKeyAndCurrentHash_callsLoadMethodWithParams(self):
        load_method_mock = MagicMock()
        cache_key = "test_key"
        current_hash = "test_hash"
        update_cache(load_method_mock, cache_key, current_hash)
        load_method_mock.assert_called_once_with(cache_key, current_hash)

    @patch('utils.cache_utils.get_cached_hash')
    def test_extract_file_hashes_givenFilePathAndExtractMethod_returnsCachedHashAndCurrentHash(self,
                                                                                               get_cached_hash_mock):
        file_path = "test_file.txt"
        extract_method_mock = MagicMock()
        get_cached_hash_mock.return_value = "cached_hash"
        calculate_md5_mock = MagicMock(return_value="current_hash")
        expected_result = ("cached_hash", "current_hash")
        self.assertEqual(extract_file_hashes(file_path, extract_method_mock), expected_result)
        calculate_md5_mock.assert_called_once_with(file_path=file_path)
        get_cached_hash_mock.assert_called_once_with(file_path, extract_method_mock)

    def test_is_md5_match_givenCachedHashAndCurrentHash_returnsTrueIfMatchesElseFalse(self):
        os.environ["conf_path"] = "base.yml"
        self.assertFalse(is_md5_match(None, "current_hash"))
        self.assertTrue(is_md5_match("cached_hash", "cached_hash"))
        self.assertFalse(is_md5_match("cached_hash", "different_hash"))

    def test_create_handler_givenHandlerNameAndOptionalParams_returnsRespectiveHandler(self):
        # Test create_handler function returns the respective handler based on the handler name
        # Test creation of FileHandler
        file_handler = create_handler("FileHandler", filename="test.log")
        self.assertIsInstance(file_handler, logging.FileHandler)
        self.assertEqual(file_handler.baseFilename, "test.log")
        # Test creation of StreamHandler
        stream_handler = create_handler("StreamHandler")
        self.assertIsInstance(stream_handler, logging.StreamHandler)


class TestLoggerSetup(unittest.TestCase):

    @patch('your_module.create_handler')
    def test_setup_custom_logger_givenLoggerConfig_returnsLoggerWithConfiguredHandlersAndFormatter(self,
                                                                                                   create_handler_mock):
        # Test setup_custom_logger function returns logger with configured handlers and formatter
        logger_config = MagicMock()
        handler_name = "FileHandler"
        logger_config.handlers = [handler_name]
        logger_config.fmt = "%(asctime)s - %(levelname)s - %(message)s"
        logger_config.datefmt = "%Y-%m-%d %H:%M:%S"
        logger_config.logger_name = "test_logger"
        logger_config.base_level = logging.INFO
        logger_config.log_file_path = "test.log"
        handler_mock = MagicMock()
        create_handler_mock.return_value = handler_mock
        logger = setup_custom_logger(logger_config)
        self.assertEqual(logger.name, "test_logger")
        self.assertEqual(logger.level, logging.INFO)
        create_handler_mock.assert_called_once_with(handler_name=handler_name, filename="test.log")
        handler_mock.setFormatter.assert_called_once()
