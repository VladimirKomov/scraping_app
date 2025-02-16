import logging

class LoggerConfig:
    """Singleton Logger"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerConfig, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        self.logger = logging.getLogger("MicroserviceLogger")

    @staticmethod
    def get_logger():
        return LoggerConfig().logger

