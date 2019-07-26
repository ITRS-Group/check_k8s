import logging

from k8s.exceptions import NagiosCritical, NagiosWarning, NagiosUnknown

from .resource import Pod
from .consts import Phase, CONDS_GOOD


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

        if pod.phase != Phase.running:
            raise NagiosCritical("Unexpected Phase for {kind} {name}: {0}".format(pod.phase.value, **pod.meta))
        elif pod.phase == Phase.pending:
            raise NagiosWarning("{kind} {name} is {0}".format(pod.phase.value, **pod.meta))

        for cond in pod.conditions:
            status_msg = (
                "{kind} {name}: {status} since {date}".format(
                    status=cond["type"],
                    date=cond["lastTransitionTime"],
                    **pod.meta
                )
            )

            if cond["type"] in CONDS_GOOD and cond["status"] != "True":
                raise NagiosCritical(status_msg)
            elif cond["type"] not in CONDS_GOOD and cond["status"] == "True":
                raise NagiosWarning(status_msg)

            logging.debug(status_msg)

    return "Found {} healthy Pods".format(len(items))
