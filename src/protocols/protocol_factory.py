from src.domain.abstract_protocol import AbstractProtocol
from src.protocols.linear_consensus import LinearConsensus
from src.protocols.max_consensus import MaxConsensus
from src.services.configuration_service import ConfigurationService
from src.services.logger_service import LoggerService


class ProtocolFactory:
    """
    Factory to create protocol instances based on configuration.
    """

    def __init__(self):
        self.config = ConfigurationService().get_configuration()

    def create_protocol(self) -> AbstractProtocol:
        protocol_type = self.config.protocol_type

        if protocol_type == "linear":
            return LinearConsensus()
        elif protocol_type == "max_consensus":
            return MaxConsensus()
        else:
            LoggerService.log_error(f"Unknown protocol type: {protocol_type}")
            raise ValueError(f"Unknown protocol type: {protocol_type}")
