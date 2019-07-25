import logging

from enum import Enum

from k8s.exceptions import NagiosCritical, NagiosWarning, NagiosUnknown

from .base import Resource


class ContainerState(Enum):
    """Container state
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#containerstate-v1-core
    """

    running = "running"
    terminated = "terminated"
    waiting = "waiting"


class Phase(Enum):
    """Pod phase
    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase
    """

    pending = "Pending"
    running = "Running"
    succeeded = "Succeeded"
    failed = "Failed"
    unknown = "Unknown"


class Pod:
    class Container:
        def __init__(self, data):
            self.name = data["name"]
            self.ready = data["ready"]

            # State is always a single-item dict, with a nested dict as value.
            # https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#containerstate-v1-core
            state = list(data["state"].keys())

            # Ensure state is known
            self.state = ContainerState(state[0])

    containers = []

    def __init__(self, data):
        status = data["status"]

        self.name = data["metadata"]["name"]
        self.meta = dict(type="Pod", name=self.name)
        self.containers = [Pod.Container(c) for c in status["containerStatuses"]]
        self.conditions = [c["type"] for c in status["conditions"] if c["status"] == "True"]
        self.phase = Phase(status["phase"])


class PodResource(Resource):
    __kind__ = "pods"

    MSG_UNHEALTHY = "Unexpected {type} state for {name}: {state}, expected: {expected}"
    CONDS_HEALTHY = ["Ready", "Initialized", "ContainersReady"]

    def check(self, **kwargs):
        """Check health of one or more Pods

        Considers a Pod healthy if it includes `CONDS_HEALTHY`

        API docs:
        https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#list-pod-v1-core

        :param kwargs: Kwargs to pass along to `Client.get`
        """

        response = self._request(**kwargs)

        for data in response:
            pod = Pod(data)

            # Ensure the Pod is in "running" phase
            if pod.phase != Phase.running:
                raise NagiosCritical(
                    self.MSG_UNHEALTHY.format(
                        **pod.meta,
                        state=pod.phase,
                        expected=Phase.running.value
                    )
                )
            # Ensure the Pod is healthy
            elif not all(cond in pod.conditions for cond in self.CONDS_HEALTHY):
                raise NagiosCritical(
                    self.MSG_UNHEALTHY.format(
                        **pod.meta,
                        state=pod.conditions,
                        expected=self.CONDS_HEALTHY
                    )
                )

            logging.debug("{type} {name} and its {count} Containers looks healthy".format(
                **pod.meta, count=len(pod.containers)
            ))

        return "Found {} healthy Pods".format(len(response))
