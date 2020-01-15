from enum import Enum

NAGIOS_MSG = "{state} - {message}"
PERFDATA_SEPARATOR = " "


class State(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
