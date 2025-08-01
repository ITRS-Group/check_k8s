from enum import Enum

STATUSES = ["Ready", "Initialized", "PodScheduled", "ContainersReady", "PodReadyToStartContainers"]


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
