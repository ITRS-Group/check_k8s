from k8s.exceptions import NagiosCritical, NagiosWarning

from .resource import Deployment


def check_deployments(items):
    """Checks the health of the provided Deployments

    Documentation:
    https://kubernetes.io/docs/concepts/workloads/controllers/deployment
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#list-all-namespaces-29

    :param items: List of Deployments
    :return: Deployments health summary
    """

    for item in items:
        deployment = Deployment(item)
        reps = deployment.replicas

        if deployment.alerts_critical:
            raise NagiosCritical(deployment.alerts_critical[0])
        elif deployment.alerts_warning:
            raise NagiosWarning(deployment.alerts_warning[0])

        if reps.available < reps.total or reps.updated < reps.total:
            if reps.available != 0 and reps.updated != 0:
                raise NagiosWarning("Deployment degraded", **deployment.meta)

            raise NagiosCritical("Deployment unavailable", **deployment.meta)

    return "Found {} healthy Deployments".format(len(items))
