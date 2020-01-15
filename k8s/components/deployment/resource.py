from collections import namedtuple
from enum import Enum

from k8s.resource import Resource
from k8s.consts import State

Replicas = namedtuple("Replicas", ["total", "ready", "updated", "available"])


class Deployment(Resource):
    class PerfdataMapping(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        NOREPS = "noreps"

    def __init__(self, data):
        super(Deployment, self).__init__(data)

        self.replicas = Replicas(
            self._status.get("replicas", 0),
            self._status.get("readyReplicas", 0),
            self._status.get("updatedReplicas", 0),
            self._status.get("availableReplicas", 0)
        )

    def _get_status(self, cond_type, cond_state):
        reps = self.replicas
        perf = self.PerfdataMapping

        if cond_type == "Available" and cond_state != "True":
            return State.CRITICAL, perf.UNAVAILABLE
        elif reps.available < reps.total or reps.updated < reps.total:
            if reps.available != 0 and reps.updated != 0:
                return State.WARNING, perf.DEGRADED
            return State.CRITICAL, perf.NOREPS
        else:
            return State.OK, perf.AVAILABLE
