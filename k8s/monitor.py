import logging

from .consts import PodPhase, ContainerState
from .exceptions import NagiosCritical, NagiosWarning, NagiosUnknown
from .pod import Pod


class Monitor:
    MSG_UNHEALTHY = "Unexpected {type} state for {name}: {state}, expected: {expected}"
    POD_HEALTHY_CONDS = ["Ready", "Initialized", "ContainersReady"]

    def __init__(self, client):
        self.mappings = self.get_mappings()
        self.client = client

    @classmethod
    def get_mappings(cls):
        """Resource-name to check-method mappings

        Allows us to store mappings in *one* place, accessible both before and after object instantiation.

        :return: Mappings Dictionary
        """

        return dict(
            pod=cls.check_pods,
            replicaset="replicaset",
            deployment="deployment",
            daemonset="daemonset",
            node="node",
            service="service"
        )

    def check(self, resource, **kwargs):
        """Dynamic resource checker

        Resolves and executes a Kubernetes check given a resource name.

        :param resource: Resource name
        :param kwargs: Kwargs to pass along to the actual check
        :return: Check result
        """

        assert resource in self.mappings, "Unknown resource: {0}".format(resource)

        fn = self.mappings[resource]
        return fn(self, **kwargs)

    def check_pods(self, **kwargs):
        """Check health of one or more Pods

        Considers a Pod healthy if it includes `POD_HEALTHY_CONDS`

        API docs:
        https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#list-pod-v1-core

        :param kwargs: Kwargs to pass along to `k8s.client.Client.get`
        """

        pods = self.client.get("pods", **kwargs).get("items")

        for pod_data in pods:
            pod = Pod(pod_data)

            # Ensure the Pod is in "running" phase
            if pod.phase != PodPhase.running:
                raise NagiosCritical(
                    self.MSG_UNHEALTHY.format(
                        **pod.meta,
                        state=pod.phase,
                        expected=PodPhase.running.value
                    )
                )
            # Ensure the Pod is healthy
            elif not all(cond in pod.conditions for cond in self.POD_HEALTHY_CONDS):
                raise NagiosCritical(
                    self.MSG_UNHEALTHY.format(
                        **pod.meta,
                        state=pod.conditions,
                        expected=self.POD_HEALTHY_CONDS
                    )
                )

            logging.debug("{type} {name} and its {count} Containers looks healthy".format(
                **pod.meta, count=len(pod.containers)
            ))

        return "Found {} healthy Pods".format(len(pods))


