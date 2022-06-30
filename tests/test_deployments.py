from k8s.components.deployment import check_deployments, Deployment
from k8s.result import Result, Output
from k8s.consts import NaemonState


def test_perfkey_available(deployment_full):
    _, status = Deployment(deployment_full).condition
    assert status.perfkey == Deployment.PerfMap.AVAILABLE


def test_perfkey_degraded(deployment_full, deployment_replicas_degraded):
    deployment_full["status"].update(deployment_replicas_degraded)
    _, status = Deployment(deployment_full).condition
    assert status.perfkey == Deployment.PerfMap.DEGRADED


def test_kind(deployment_full):
    assert Deployment(deployment_full)._kind == "Deployment"


def test_result(deployment_full, ignore_none):
    result = check_deployments([deployment_full], ignore_none)
    assert isinstance(result, Result)


def test_output(deployment_full, ignore_none):
    output = check_deployments([deployment_full], ignore_none).output
    assert isinstance(output, Output)


def test_replicas(deployment_full):
    replica_data = deployment_full["status"]
    replicas = Deployment(deployment_full).replicas

    assert replicas.total == replica_data["replicas"]
    assert replicas.ready == replica_data["readyReplicas"]
    assert replicas.available == replica_data["availableReplicas"]
    assert replicas.updated == replica_data["updatedReplicas"]


def test_replicas_available(deployment_full, ignore_none):
    output = check_deployments([deployment_full], ignore_none).output
    assert output.state == NaemonState.OK


def test_replicas_ignored(deployment_full, ignore_none):
    output = check_deployments([deployment_full], ignore_none).output
    assert output.state == NaemonState.OK


def test_replicas_unavailable(deployment_full, ignore_none):
    replicas = deployment_full["status"]
    replicas["availableReplicas"] = 0
    output = check_deployments([deployment_full], ignore_none).output
    assert output.state == NaemonState.CRITICAL


def test_replicas_not_updated(deployment_full, ignore_none):
    replicas = deployment_full["status"]
    replicas["updatedReplicas"] = 0
    output = check_deployments([deployment_full], ignore_none).output
    assert output.state == NaemonState.CRITICAL


def test_replicas_not_updated_ignored(deployment_full, ignore_all_deployment):
    replicas = deployment_full["status"]
    replicas["updatedReplicas"] = 0
    output = check_deployments([deployment_full], ignore_all_deployment).output
    lines = output.message.split('\n')
    assert output.state == NaemonState.OK
    assert lines[1] == "|available=0 unavailable=0 degraded=0 noreps=0"


def test_replicas_degraded(deployment_full, deployment_replicas_degraded, ignore_none):
    deployment_full["status"].update(deployment_replicas_degraded)
    output = check_deployments([deployment_full], ignore_none).output
    assert output.state == NaemonState.WARNING


def test_replicas_degraded_ignored(deployment_full, deployment_replicas_degraded, ignore_all_deployment):
    deployment_full["status"].update(deployment_replicas_degraded)
    output = check_deployments([deployment_full], ignore_all_deployment).output
    lines = output.message.split('\n')
    assert output.state == NaemonState.OK
    assert lines[1] == "|available=0 unavailable=0 degraded=0 noreps=0"
