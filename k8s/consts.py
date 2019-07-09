from enum import Enum


class InputDefault(Enum):
    """CLI defaults"""

    timeout = 15.0
    host = "127.0.0.1"
    port = 8080
    no_ssl = False
    debug = False
    namespace = None
    resource = None


class ContainerState(Enum):
    """K8s Container state
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#containerstate-v1-core
    """

    running = "running"
    terminated = "terminated"
    waiting = "waiting"


class PodPhase(Enum):
    """K8s Pod phase
    https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase
    """

    pending = "Pending"
    running = "Running"
    succeeded = "Succeeded"
    failed = "Failed"
    unknown = "Unknown"
