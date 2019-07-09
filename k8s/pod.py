from .consts import ContainerState, PodPhase


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
        self.phase = PodPhase(status["phase"])

