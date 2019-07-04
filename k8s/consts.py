from enum import Enum


class ServiceStatus(Enum):
    """Nagios Service status
    https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/pluginapi.html
    """

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


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
