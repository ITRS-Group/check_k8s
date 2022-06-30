from k8s.result import Result

from .resource import Node


def check_nodes(items, expressions):
    """Checks the health of the provided Nodes

    Documentation:
    https://kubernetes.io/docs/concepts/architecture/nodes/#condition
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#node-v1-core

    :param items: List of Nodes
    :return: Nodes health summary
    """

    return Result(Node, items, expressions)
