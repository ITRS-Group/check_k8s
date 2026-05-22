from k8s.result import Result

from .resource import Pod

from collections import defaultdict

def check_pods(items, expressions, buffer_time=0.0, group_by_label=None):
    """Check health of one or more Pods and associated Containers

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#list-pod-v1-core

    :param items: List of Pods
    :return: Pods health summary
    """

    # groups = group_by_app_name_label(items)

    return Result(Pod, items, expressions, buffer_time, group_by_label)
