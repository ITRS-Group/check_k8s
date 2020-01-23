import pytest

from k8s.components.pod import check_pods, Pod, Container
from k8s.consts import NaemonState


def test_kind(pod_full):
    assert Pod(pod_full)._kind == "Pod"


def test_valid_phase(pod_full):
    assert Pod(pod_full).phase.value == pod_full["status"]["phase"]


def test_invalid_phase(pod_full):
    pod_full["status"]["phase"] = "Broken"
    with pytest.raises(ValueError):
        assert Pod(pod_full)


def test_valid_container_state(pod_containers):
    container_data = pod_containers[0]
    container_state = list(container_data["state"].keys())
    assert Container(container_data).state.value is container_state[0]


def test_invalid_container_state(pod_containers):
    container_data = pod_containers[0]
    container_data["state"] = dict(Broken="")
    with pytest.raises(ValueError):
        assert Container(container_data)


def test_container_base(pod_full):
    assert Pod(pod_full).containers
    assert Pod(pod_full).containers[0].ready is True


def test_container_count(pod_full, pod_containers):
    assert len(Pod(pod_full).containers) == len(pod_containers)


def test_check_pending(pod_full):
    pod_full["status"]["phase"] = "Pending"
    assert check_pods([pod_full]).output.state == NaemonState.CRITICAL


def test_check_failed(pod_full):
    pod_full["status"]["phase"] = "Failed"
    assert check_pods([pod_full]).output.state == NaemonState.CRITICAL


def test_check_not_running(pod_base, pod_not_ready, pod_containers):
    pod_base["status"]["conditions"] = pod_not_ready
    pod_base["status"]["containerStatuses"] = pod_containers
    assert check_pods([pod_base]).output.state == NaemonState.CRITICAL


def test_check_cond_other(pod_base, pod_condition_other, pod_containers):
    pod_base["status"]["conditions"] = pod_condition_other
    pod_base["status"]["containerStatuses"] = pod_containers
    assert check_pods([pod_base]).output.state == NaemonState.WARNING
