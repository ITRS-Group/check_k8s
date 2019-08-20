import logging

from k8s.exceptions import MetaNotFound, ConditionsNotFound, StatusNotFound
from k8s.consts import State


class Resource:
    def __init__(self, data, kind=None):
        self._kind = kind or self.__class__.__name__
        self._data = data
        self._alerts = {State.CRITICAL: [], State.WARNING: []}

        if "metadata" not in data or not data["metadata"]:
            raise MetaNotFound("Malformed response: metadata not found for kind {}".format(self._kind))

        self.meta = dict(kind=self._kind, name=data["metadata"]["name"])

        if "status" not in data or not data["status"]:
            raise StatusNotFound("Malformed response: status not found", **self.meta)

        self._status = data["status"]

        if "conditions" not in self._status or not len(self._status["conditions"]):
            raise ConditionsNotFound("No conditions found, cannot check health", **self.meta)

        for data in self._status["conditions"]:
            message = self._get_condition_msg(data)
            logging.debug(message)

            level = self._condition_to_alert(data["type"], data["status"])

            if level:
                self._alerts[level].append(message)

    def _get_condition_msg(self, data):
        """Converts parts of a condition to a human-readable message

        :param data: Condition object
        :return: Formatted condition message
        """

        return "{kind} {name}: {0} {1} since {2}".format(
            "condition" if data["status"] == "True" else "condition [not]",
            data["type"],
            data["lastTransitionTime"],
            **self.meta
        )

    def _condition_to_alert(self, _type, status):
        """Converts a `Resource`s Kubernetes conditions to Nagios alerts

        :param _type: Kubernetes condition type
        :param status: Kubernetes condition status
        :return: (<Severity>, <message>)
        """

        raise NotImplementedError

    @property
    def alerts_critical(self):
        return self._alerts[State.CRITICAL]

    @property
    def alerts_warning(self):
        return self._alerts[State.WARNING]
