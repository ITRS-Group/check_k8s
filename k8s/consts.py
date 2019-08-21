from enum import Enum

NAGIOS_MSG = "{state} - {message}"


class Severity(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
