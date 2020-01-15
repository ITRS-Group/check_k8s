from enum import Enum

from k8s.resource import Resource
from k8s.consts import State


class Node(Resource):
    class PerfdataMapping(Enum):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        DEGRADED = "degraded"
        UNSCHEDULABLE = "unschedulable"

    def __init__(self, data):
        super(Node, self).__init__(data)

        # https://kubernetes.io/docs/concepts/architecture/nodes/#manual-node-administration
        self.unschedulable = data["spec"].get("unschedulable", False)

    def _get_status(self, _type, status):
        perf = self.PerfdataMapping

        if _type == "Ready" and status != "True":
            return State.CRITICAL, perf.UNAVAILABLE
        elif _type != "Ready" and status == "True":
            return State.WARNING, perf.DEGRADED
        elif self.unschedulable:
            # @TODO - custom override when supported: "Node {} is ready, but unschedulable".format(node.meta["name"])
            return State.WARNING, perf.UNSCHEDULABLE
        else:
            return State.OK, perf.AVAILABLE
