from collections import namedtuple
from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus


Replicas = namedtuple("Replicas", ["total", "ready", "updated", "available"])


class Deployment(Resource):
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        NOREPS = "noreps"

    def __init__(self, data, *args, **kwargs):
        super(Deployment, self).__init__(data, *args, **kwargs)

        self.replicas = Replicas(
            self._status.get("replicas", 0),
            self._status.get("readyReplicas", 0),
            self._status.get("updatedReplicas", 0),
            self._status.get("availableReplicas", 0),
        )

    def _get_status(self, cnd_type, cnd_status):
        reps = self.replicas

        if cnd_type == "Available":
            if cnd_status == "True":
                return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
        elif reps.available < reps.total or reps.updated < reps.total:
            if reps.available != 0 and reps.updated != 0:
                return NaemonStatus(NaemonState.WARNING, self.perf.DEGRADED)
            return NaemonStatus(NaemonState.CRITICAL, self.perf.NOREPS)
