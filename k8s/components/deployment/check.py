from k8s.exceptions import NagiosCritical, NagiosWarning

from .resource import Deployment

from k8s.consts import State

from collections import namedtuple


Counters = namedtuple("StateCounters", ["OK", "WARNING", "CRITICAL", "UNKNOWN"])


def state_counters(items):
    counters = {s: 0 for s in State._member_map_.values()}
    for _, state, _ in items:
        counters[state] += 1

    # return Counters(**counters)
    return counters


def check_deployments(items):
    """Checks the health of the provided Deployments

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/deployment
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of Deployments
    :return: Deployments health summary
    """

    alerts = [Deployment(i).alert for i in items]
    counter = state_counters(alerts)
    print(counter)

    for a in alerts:
        if not a:
            continue

    return "Found {} healthy Deployments".format(len(items))
