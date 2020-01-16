import logging

from enum import Enum

from k8s.exceptions import (
    MetaNotFound,
    ConditionsNotFound,
    StatusNotFound,
    HealthUnknown
)

from k8s.consts import NaemonState


class NaemonStatus:
    def __init__(self, state, perfkey=None, msg_override=None):
        self.state = state
        self.perfkey = perfkey
        self.msg_override = msg_override


class Resource:
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"

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

    @property
    def perf(self):
        return self.PerfMap

    def _get_status(self, k8s_type, k8s_status):
        """Abstract method for getting a Resource's current status

        :param k8s_type: Kubernetes condition type
        :param k8s_status: Kubernetes condition status
        :return: (<Severity>, <message>)
        """

        raise NotImplementedError

    @property
    def condition(self):
        if "conditions" not in self._status or not len(self._status["conditions"]):
            raise ConditionsNotFound("No conditions found, cannot check health", **self.meta)

        status_ok = None

        for cnd in self._status["conditions"]:
            status = self._get_status(cnd["type"], cnd["status"])
            if not status:
                continue

            message = status.msg_override or self._format_message(cnd)
            logging.debug(message)

            if status.state == NaemonState.OK:
                # Only store latest successful condition
                status_ok = message, status
            else:
                # Immediately return if an issue was encountered
                return message, status

        if not status_ok:
            raise HealthUnknown(
                "Unable to determine the health of one or more {resource} "
                "resources due to one or more unknown conditions."
                "This is most likely a bug, try using the --debug "
                "flag to troubleshoot.".format(resource=self._kind)
            )

        return status_ok

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
