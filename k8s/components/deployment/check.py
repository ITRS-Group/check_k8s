from k8s.result import Result

from .resource import Deployment


def check_deployments(items, expressions):
    """Checks the health of the provided Deployments

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/deployment
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of Deployments
    :return: Deployments health summary
    """

    return Result(Deployment, items, expressions)
