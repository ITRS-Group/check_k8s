import logging

from k8s.exceptions import MetaNotFound, ConditionsNotFound, StatusNotFound


class Resource:
    def __init__(self, data, kind=None):
        # Custom kind, in case we want to use `Resource` directly
        self._kind = kind or self.__class__.__name__
        self._data = data

        # Metadata
        if "metadata" not in data or not data["metadata"]:
            raise MetaNotFound("Malformed response: metadata not found for kind {}".format(self._kind))

        self.meta = dict(kind=self._kind, name=data["metadata"]["name"])

        # Status
        if "status" not in data or not data["status"]:
            raise StatusNotFound("Malformed response: status not found", **self.meta)

        self._status = data["status"]

        # Convert Kubernetes conditions to Nagios alerts
        if "conditions" not in self._status or not len(self._status["conditions"]):
            raise ConditionsNotFound("No conditions found, cannot check health", **self.meta)

    @property
    def conditions(self):
        data = []

        for cnd in self._status["conditions"]:
            message = self._format_message(cnd)
            logging.debug(message)

            state, perfkey = self._get_status(cnd["type"], cnd["status"])
            data.append((message, state, perfkey))

        return data

    def _format_message(self, data):
        """Default condition message-builder for producing a human-readable message

        Can be easily overridden in subclasses.

        :param data: Condition dict object
        :return: Formatted condition message
        """

        return "{kind} {name}: {0} {1} since {2}".format(
            "condition" if data["status"] == "True" else "condition [not]",
            data["type"],
            data["lastTransitionTime"],
            **self.meta
        )

    def _get_status(self, cond_type, cond_state):
        """Abstract method for getting a Resource's current status

        :param cond_type: Kubernetes condition type
        :param cond_state: Kubernetes condition status
        :return: (<Severity>, <message>)
        """

        raise NotImplementedError
