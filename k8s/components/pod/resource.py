from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus

from .consts import ContainerState, Phase, STATUSES


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
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        PENDING = "pending"

    def __init__(self, data):
        super(Pod, self).__init__(data)

        self.containers = [Container(c) for c in self._status["containerStatuses"]]
        self.phase = Phase(self._status["phase"])

    def _get_status(self, cnd_type, cnd_status):
        if self.phase != Phase.running and self.phase != Phase.succeeded:
            return NaemonStatus(
                NaemonState.CRITICAL,
                self.perf.UNAVAILABLE,
                "Unexpected Phase for {kind} {name}: {0}".format(self.phase.value, **self.meta)
            )
        elif cnd_type in STATUSES:
            if cnd_status == "True":
                return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
        elif cnd_type not in STATUSES and cnd_status == "True":
            return NaemonStatus(NaemonState.WARNING, self.perf.DEGRADED)
        elif self.phase == Phase.pending:
            return NaemonStatus(NaemonState.WARNING, self.perf.PENDING)
