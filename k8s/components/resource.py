import logging

from enum import Enum
from abc import ABC, abstractmethod

from k8s.exceptions import (
    MetaNotFound,
    ConditionsNotFound,
    StatusNotFound,
    HealthUnknown,
)

from k8s.consts import NaemonState


class NaemonStatus:
    def __init__(self, state, perfkey=None, msg_override=None):
        self.state = state
        self.perfkey = perfkey
        self.msg_override = msg_override


class Resource(ABC):
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
            raise MetaNotFound(
                "Malformed response: metadata not found for kind {}".format(self._kind)
            )

        self.meta = dict(kind=self._kind, name=data["metadata"]["name"])

        # Status
        if "status" not in data or not data["status"]:
            raise StatusNotFound("Malformed response: status not found", **self.meta)

        self._status = data["status"]

    @property
    def perf(self):
        return self.PerfMap

    @abstractmethod
    def _get_status(self, cond_type, cond_status):
        """Determines status using a Kubernetes Condition's  type and status

        :param cond_type: Kubernetes condition type
        :param cond_status: Kubernetes condition status
        :return: (<Severity>, <message>)
        """

    @property
    def condition(self):
        """Returns the Resources status and associated message

        If state cannot be determined, the HealthUnknown exception is raised.

        :return: (message, status)
        """

        if "conditions" not in self._status or not len(self._status["conditions"]):
            raise ConditionsNotFound(
                "No conditions found, cannot check health", **self.meta
            )

        status_ok = None

        for cnd in self._status["conditions"]:
            status = self._get_status(cnd["type"], cnd["status"])
            if not status:
                continue

            message = status.msg_override or self._format_message(cnd)
            logging.debug(message)

            if status.state == NaemonState.OK:
                # Only store last successful condition
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

    def _format_message(self, condition):
        """Converts a Kubernetes condition into a human-readable message

        :param condition: Condition dict
        :return: Formatted condition message
        """

        return "{kind} {name}: {0} {1} since {2}".format(
            "condition" if condition["status"] == "True" else "condition [not]",
            condition["type"],
            condition["lastTransitionTime"],
            **self.meta
        )
