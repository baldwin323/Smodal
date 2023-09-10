import unittest
import logging
from Smodal.logging import logger

class TestLogger(unittest.TestCase):
    
    def setUp(self):
        self.logger = logger

    def test_logger_name(self):
        self.assertEqual(self.logger.name, __name__)

    def test_console_handler_level(self):
        console_handler_level = next(handler.level for handler in self.logger.handlers if isinstance(handler, logging.StreamHandler))
        self.assertEqual(console_handler_level, logging.INFO)

    def test_file_handler_level(self):
        file_handler_level = next(handler.level for handler in self.logger.handlers if isinstance(handler, logging.FileHandler))
        self.assertEqual(file_handler_level, logging.ERROR)

    def test_handler_types(self):
        handler_types = [type(handler) for handler in self.logger.handlers]
        self.assertTrue(logging.StreamHandler in handler_types)
        self.assertTrue(logging.FileHandler in handler_types)

    def test_handler_levels(self):
        handler_levels = [handler.level for handler in self.logger.handlers]
        self.assertIn(logging.INFO, handler_levels)
        self.assertIn(logging.ERROR, handler_levels)

    def test_handler_formatters(self):
        handler_formatters = [str(type(handler.formatter)) for handler in self.logger.handlers]
        self.assertIn(str(type(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))), handler_formatters)
        self.assertIn(str(type(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s - line %(lineno)d'))), handler_formatters)

    def test_logfile_filename(self):
        file_handler_filename = next(handler.baseFilename for handler in self.logger.handlers if isinstance(handler, logging.FileHandler))
        self.assertEqual(file_handler_filename, 'app.log')

if __name__ == '__main__':
    unittest.main()