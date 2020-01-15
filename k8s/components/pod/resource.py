from enum import Enum

from k8s.resource import Resource
from k8s.consts import State

from .consts import ContainerState, Phase, CONDITIONS_HEALTHY


class Container:
    def __init__(self, data):
        self.name = data["name"]
        self.ready = data["ready"]

        # Container State is a single-item dict, with a nested dict value.
        # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#containerstate-v1-core
        state = list(data["state"].keys())

        # Ensure state is known
        self.state = ContainerState(state[0])


class Pod(Resource):
    class PerfdataMapping(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        PENDING = "pending"

    def __init__(self, data):
        super(Pod, self).__init__(data)

        self.containers = [Container(c) for c in self._status["containerStatuses"]]
        self.phase = Phase(self._status["phase"])

    def _get_status(self, _type, status):
        perf = self.PerfdataMapping

        if _type in CONDITIONS_HEALTHY and status != "True":
            return State.CRITICAL, perf.UNAVAILABLE
        elif self.phase != Phase.running and self.phase != Phase.succeeded:
            # @TODO - custom override when supported:
            # "Unexpected Phase for {kind} {name}: {0}".format(pod.phase.value, **pod.meta)
            return State.CRITICAL, perf.UNAVAILABLE
        elif _type not in CONDITIONS_HEALTHY and status == "True":
            return State.WARNING, perf.DEGRADED
        elif self.phase == Phase.pending:
            return State.WARNING, perf.PENDING
        else:
            return State.OK, perf.AVAILABLE

