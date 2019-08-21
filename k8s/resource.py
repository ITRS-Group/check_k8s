import logging

from k8s.exceptions import MetaNotFound, ConditionsNotFound, StatusNotFound
from k8s.consts import Severity


class Resource:
    def __init__(self, data, kind=None):
        self._alerts = {
            Severity.CRITICAL: [],
            Severity.WARNING: []
        }

        # Custom kind, in case we want to use `Resource` directly
        self._kind = kind or self.__class__.__name__
        self._data = data

        # Check & set metadata
        if "metadata" not in data or not data["metadata"]:
            raise MetaNotFound("Malformed response: metadata not found for kind {}".format(self._kind))

        self.meta = dict(kind=self._kind, name=data["metadata"]["name"])

        # Check & set status
        if "status" not in data or not data["status"]:
            raise StatusNotFound("Malformed response: status not found", **self.meta)

        self._status = data["status"]

        # Convert Kubernetes conditions to Nagios alerts
        if "conditions" not in self._status or not len(self._status["conditions"]):
            raise ConditionsNotFound("No conditions found, cannot check health", **self.meta)

        for data in self._status["conditions"]:
            message = self._condition_message(data)
            logging.debug(message)

            level = self._condition_severity(data["type"], data["status"])
            self._register_alert(level, message)

    def _register_alert(self, level, message):
        """Safely registers an alert

        :param level: Severity[level]
        :param message: Formatted message
        :return:
        """

        if level is None:
            return

        assert isinstance(level, Severity), "{} is not a known Severity".format(level)

        self._alerts[level] = message

    def _condition_message(self, data):
        """Default condition message-builder for producing a human-readable message

        Can be easily overridden i subclasses.

        :param data: Condition dict object
        :return: Formatted condition message
        """

        return "{kind} {name}: {0} {1} since {2}".format(
            "condition" if data["status"] == "True" else "condition [not]",
            data["type"],
            data["lastTransitionTime"],
            **self.meta
        )

    def _condition_severity(self, _type, status):
        """Abstract method for converting a `Resource`s Kubernetes condition to Nagios severity

        :param _type: Kubernetes condition type
        :param status: Kubernetes condition status
        :return: (<Severity>, <message>)
        """

        raise NotImplementedError

    @property
    def alerts_critical(self):
        return self._alerts[Severity.CRITICAL]

    @property
    def alerts_warning(self):
        return self._alerts[Severity.WARNING]
