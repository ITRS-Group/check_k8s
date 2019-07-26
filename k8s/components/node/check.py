import logging

from k8s.exceptions import NagiosCritical, NagiosWarning
from k8s.resource import Resource


def check_nodes(items):
    """Checks the health of the provided Nodes

    Documentation:
    https://kubernetes.io/docs/concepts/architecture/nodes/#condition
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#node-v1-core

    :param items: List of Nodes
    :return: Nodes health summary
    """

    for item in items:
        node = Resource(item, kind="Node")

        for cond in node.conditions:
            if cond.type == "Ready" and cond.status != "True":
                raise NagiosCritical(cond.message)
            elif cond.type != "Ready" and cond.status == "True":
                raise NagiosWarning(cond.message)

            logging.debug(cond.message)

    return "Found {} healthy Nodes".format(len(items))
