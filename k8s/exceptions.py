class ApplicationError(Exception):
    def __init__(self, message, **meta):
        if not meta:
            self.message = message
        else:
            self.message = "{kind} {name}: {0}".format(message, **meta)


class HealthUnknown(ApplicationError):
    pass


class MetaNotFound(ApplicationError):
    pass


class StatusNotFound(ApplicationError):
    pass


class ConditionsNotFound(ApplicationError):
    pass
