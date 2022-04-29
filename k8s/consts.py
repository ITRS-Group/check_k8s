from enum import Enum

NAGIOS_MSG = "{state} - {message}"
PERFDATA_SEPARATOR = " "

RESULT_SUCCESS = "All checks were successful"
RESULT_CRITICAL = "One or more errors encountered"
RESULT_WARNING = "One or more warnings encountered"

VERSION = "1.1.0"


class NaemonState(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3
