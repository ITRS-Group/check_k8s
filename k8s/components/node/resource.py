from k8s.resource import Resource


class Node(Resource):
    def __init__(self, data):
        super(Node, self).__init__(data)

        # https://kubernetes.io/docs/concepts/architecture/nodes/#manual-node-administration
        self.unschedulable = data["spec"].get("unschedulable", False)
