import pytest

from k8s.components.deployment import check_deployments, Deployment
from k8s.exceptions import NagiosCritical, NagiosWarning


def test_deployment_type(deployment_full):
    assert Deployment(deployment_full)._kind == "Deployment"


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
    with pytest.raises(NagiosCritical):
        check_deployments([deployment_full])


def test_check_replicas_not_updated(deployment_full):
    replicas = deployment_full["status"]
    replicas["updatedReplicas"] = 0
    with pytest.raises(NagiosCritical):
        check_deployments([deployment_full])


def test_check_replicas_degraded(deployment_full, deployment_replicas_degraded):
    deployment_full["status"].update(deployment_replicas_degraded)
    with pytest.raises(NagiosWarning):
        check_deployments([deployment_full])
