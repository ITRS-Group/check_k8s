from .resource import Resource, PodResource, ReplicasetResource
from .client import Client


class Monitor:
    mappings = dict(
        pod=PodResource,
        replicaset=ReplicasetResource,
        deployment="deployment",
        daemonset="daemonset",
        node="node",
        service="service"
    )

    def __init__(self, *args, **kwargs):
        self.client = Client(*args, **kwargs)

    def check_wrapped(self, resource, **kwargs):
        """Resource check wrapper

        Resolves and executes a Kubernetes check given a resource name.

        :param resource: Resource name
        :param kwargs: Kwargs to pass along to the actual check
        :return: Check result
        """

        assert resource in self.mappings, "Unknown resource: {0}".format(resource)

        cls = self.mappings[resource]

        assert issubclass(cls, Resource)

        return cls(self.client).check(**kwargs)
