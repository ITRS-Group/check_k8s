from k8s.consts import State


class UnknownState(Exception):
    pass


class PluginException(Exception):
    state = None

    def __init__(self, message, **meta):
        if not meta:
            self.message = message
        else:
            self.message = "{kind} {name}: {0}".format(message, **meta)


class NagiosWarning(PluginException):
    state = State.WARNING


class NagiosCritical(PluginException):
    state = State.CRITICAL


class NagiosUnknown(PluginException):
    state = State.UNKNOWN
