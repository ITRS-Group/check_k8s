from k8s.exceptions import NagiosCritical, NagiosWarning

from .resource import Node


def check_nodes(items):
    """Checks the health of the provided Nodes

    Documentation:
    https://kubernetes.io/docs/concepts/architecture/nodes/#condition
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#node-v1-core

    :param items: List of Nodes
    :return: Nodes health summary
    """

    for item in items:
        node = Node(item)

        if node.alerts_critical:
            raise NagiosCritical(node.alerts_critical[0])
        elif node.alerts_warning:
            raise NagiosWarning(node.alerts_warning[0])

        if node.unschedulable:
            raise NagiosWarning("Node {} is ready, but unschedulable".format(node.meta["name"]))

    return "Found {} healthy Nodes".format(len(items))
