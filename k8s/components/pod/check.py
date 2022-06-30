from k8s.result import Result

from .resource import Pod


def check_pods(items, expressions):
    """Check health of one or more Pods and associated Containers

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#list-pod-v1-core

    :param items: List of Pods
    :return: Pods health summary
    """

    return Result(Pod, items, expressions)
