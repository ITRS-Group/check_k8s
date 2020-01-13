from collections import namedtuple

from k8s.resource import Resource
from k8s.consts import State

Replicas = namedtuple("Replicas", ["total", "ready", "updated", "available"])


class Deployment(Resource):
    def __init__(self, data):
        super(Deployment, self).__init__(data)

        self.replicas = Replicas(
            self._status["replicas"],
            self._status["readyReplicas"],
            self._status["updatedReplicas"],
            self._status["availableReplicas"]
        )

    def _get_status(self, cond_type, cond_state):
        reps = self.replicas

        if cond_type == "Available" and cond_state != "True":
            return State.CRITICAL, "unavailable"
        elif reps.available < reps.total or reps.updated < reps.total:
            if reps.available != 0 and reps.updated != 0:
                return State.WARNING, "degraded"

            return State.CRITICAL, "unavailable"
        else:
            return State.OK, "available"
