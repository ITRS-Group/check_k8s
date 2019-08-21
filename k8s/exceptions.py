from k8s.consts import Severity


class PluginException(Exception):
    state = None

    def __init__(self, message, **meta):
        if not meta:
            self.message = message
        else:
            self.message = "{kind} {name}: {0}".format(message, **meta)


class NagiosWarning(PluginException):
    state = Severity.WARNING


class NagiosCritical(PluginException):
    state = Severity.CRITICAL


class NagiosUnknown(PluginException):
    state = Severity.UNKNOWN


class MetaNotFound(NagiosUnknown):
    pass


class StatusNotFound(NagiosUnknown):
    pass


class ConditionsNotFound(NagiosUnknown):
    pass

