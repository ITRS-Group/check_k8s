class NagiosError(Exception):
    code = None
    level = None

    def __init__(self, message, **meta):
        if not meta:
            self.message = message
        else:
            self.message = "{kind} {name}: {0}".format(message, **meta)


class NagiosWarning(NagiosError):
    code = 1
    level = "WARNING"


class NagiosCritical(NagiosError):
    code = 2
    level = "CRITICAL"


class NagiosUnknown(NagiosError):
    code = 3
    level = "UNKNOWN"
