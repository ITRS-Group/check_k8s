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

    def _condition_to_alert(self, _type, status):
        if _type == "Available" and status != "True":
            return State.CRITICAL
