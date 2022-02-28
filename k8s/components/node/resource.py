from enum import Enum

from k8s.consts import NaemonState

from ..resource import Resource, NaemonStatus


class Node(Resource):
    class PerfMap(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        UNSCHEDULABLE = "unschedulable"

    def __init__(self, data, *args, **kwargs):
        super(Node, self).__init__(data, *args, **kwargs)

        # https://kubernetes.io/docs/concepts/architecture/nodes/#manual-node-administration
        self.unschedulable = data["spec"].get("unschedulable", False)

    def _get_status(self, cnd_type, cnd_status):
        if self.unschedulable:
            return NaemonStatus(
                NaemonState.WARNING,
                self.perf.UNSCHEDULABLE,
                "Node {} is ready, but unschedulable".format(self.meta["name"]),
            )
        elif cnd_type == "Ready":
            if cnd_status == "True":
                return NaemonStatus(NaemonState.OK, self.perf.AVAILABLE)
            else:
                return NaemonStatus(NaemonState.CRITICAL, self.perf.UNAVAILABLE)
        elif cnd_type != "Ready" and cnd_status == "True":
            return NaemonStatus(NaemonState.WARNING, self.perf.DEGRADED)
