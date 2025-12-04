import logging
import sys
from typing import Optional

class LoggerService:
    """
    Singleton Logger Service.
    """
    _instance: Optional['LoggerService'] = None
    _logger: logging.Logger

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self._logger = logging.getLogger("ConsensusSimulation")
        self._logger.setLevel(logging.INFO)
        
        # Check if handlers already exist to avoid duplicate logs
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self._logger

    @staticmethod
    def log_info(message: str):
        LoggerService().get_logger().info(message)

    @staticmethod
    def log_warning(message: str):
        LoggerService().get_logger().warning(message)

    @staticmethod
    def log_error(message: str):
        LoggerService().get_logger().error(message)
