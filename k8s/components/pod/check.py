from k8s.exceptions import NagiosCritical, NagiosWarning

from .resource import Pod
from .consts import Phase


def check_pods(items):
    """Check health of one or more Pods and associated Containers

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#list-pod-v1-core

    :param items: List of Pods
    :return: Pods health summary
    """

    for item in items:
        pod = Pod(item)

        if pod.phase == Phase.pending:
            raise NagiosWarning("{kind} {name} is {0}".format(pod.phase.value, **pod.meta))
        elif pod.phase != Phase.running and pod.phase != Phase.succeeded:
            raise NagiosCritical("Unexpected Phase for {kind} {name}: {0}".format(pod.phase.value, **pod.meta))

        if pod.alerts_critical:
            raise NagiosCritical(pod.alerts_critical[0])
        elif pod.alerts_warning:
            raise NagiosWarning(pod.alerts_warning[0])

    return "Found {} healthy Pods".format(len(items))
