import logging

from .consts import PodPhase, ContainerState, ServiceStatus
from .exceptions import NagiosCritical, NagiosWarning, NagiosUnknown


class Monitor:
    MSG_STATUS = "Unexpected {type} state for {name}: {state}, expected: {expected}"
    POD_CONDS_HEALTHY = ["Ready", "Initialized", "ContainersReady"]

    def __init__(self, client):
        self.client = client

    def _raise_for_status(self, severity, **kwargs):
        msg = self.MSG_STATUS.format(**kwargs)

        if severity == ServiceStatus.CRITICAL:
            raise NagiosCritical(msg)

        raise NagiosWarning(msg)

    def pod_status(self, *args, **kwargs):
        for pod in self.client.get_pods(*args, **kwargs):
            meta = dict(type="Pod", name=pod.name)
            if pod.phase != PodPhase.running:
                self._raise_for_status(
                    ServiceStatus.CRITICAL,
                    **meta,
                    state=pod.phase,
                    expected=PodPhase.running.value,
                )
            elif set(self.POD_CONDS_HEALTHY) >= set(pod.conditions):
                self._raise_for_status(
                    ServiceStatus.CRITICAL,
                    **meta,
                    state=pod.conditions,
                    expected=self.POD_CONDS_HEALTHY,
                )

            logging.debug("OK: Pod {0} looks healthy".format(pod.name))
