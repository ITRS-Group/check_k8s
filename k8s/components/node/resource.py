from k8s.resource import Resource
from k8s.consts import State


class Node(Resource):
    def __init__(self, data):
        super(Node, self).__init__(data)

        # https://kubernetes.io/docs/concepts/architecture/nodes/#manual-node-administration
        self.unschedulable = data["spec"].get("unschedulable", False)

    def _condition_to_alert(self, _type, status):
        if _type == "Ready" and status != "True":
            return State.CRITICAL
        elif _type != "Ready" and status == "True":
            return State.WARNING
