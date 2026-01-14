from typing import Optional
from src.models.configuration import SimulationConfiguration
from src.services.logger_service import LoggerService


class ConfigurationService:
    """
    Singleton Configuration Service to manage simulation settings.
    """

    _instance: Optional["ConfigurationService"] = None
    _config: Optional[SimulationConfiguration] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationService, cls).__new__(cls)
        return cls._instance

    def set_configuration(self, config: SimulationConfiguration):
        self._config = config
        LoggerService.log_info(f"Configuration set: {config}")

    def get_configuration(self) -> SimulationConfiguration:
        if self._config is None:
            raise ValueError("Configuration has not been set yet.")
        return self._config
