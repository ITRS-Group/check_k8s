from k8s.components.deployment import check_deployments, Deployment
from k8s.result import Result, Output
from k8s.consts import NaemonState


def test_deployment_type(deployment_full):
    assert Deployment(deployment_full)._kind == "Deployment"


def test_result(deployment_full):
    result = check_deployments([deployment_full])
    assert isinstance(result, Result)


def test_output(deployment_full):
    output = check_deployments([deployment_full]).output
    assert isinstance(output, Output)


def test_deployment_replicas(deployment_full):
    replica_data = deployment_full["status"]
    replicas = Deployment(deployment_full).replicas

    assert replicas.total == replica_data["replicas"]
    assert replicas.ready == replica_data["readyReplicas"]
    assert replicas.available == replica_data["availableReplicas"]
    assert replicas.updated == replica_data["updatedReplicas"]


def test_check_replicas_unavailable(deployment_full):
    replicas = deployment_full["status"]
    replicas["availableReplicas"] = 0
    output = check_deployments([deployment_full]).output
    assert output.state == NaemonState.CRITICAL


def test_check_replicas_not_updated(deployment_full):
    replicas = deployment_full["status"]
    replicas["updatedReplicas"] = 0
    output = check_deployments([deployment_full]).output
    assert output.state == NaemonState.CRITICAL


def test_check_replicas_degraded(deployment_full, deployment_replicas_degraded):
    deployment_full["status"].update(deployment_replicas_degraded)
    output = check_deployments([deployment_full]).output
    assert output.state == NaemonState.WARNING
