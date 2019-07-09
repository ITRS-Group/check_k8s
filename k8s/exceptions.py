class NagiosError(Exception):
    code = None
    prefix = None

    def __init__(self, message):
        self.message = "{0} - {1}".format(self.prefix, message)


class NagiosWarning(NagiosError):
    code = 1
    prefix = "WARNING"


class NagiosCritical(NagiosError):
    code = 2
    prefix = "CRITICAL"


class NagiosUnknown(NagiosError):
    code = 3
    prefix = "UNKNOWN"
