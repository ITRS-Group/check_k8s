import pytest

from k8s.components.node import check_nodes, Node
from k8s.exceptions import NagiosCritical, NagiosWarning


def test_type(node_full):
    assert Node(node_full).unschedulable is False
    assert Node(node_full)._kind == "Node"


def test_ready(node_base, node_ready):
    node_base["status"]["conditions"] = node_ready
    assert check_nodes([node_base]) == "Found 1 healthy Nodes"


def test_not_ready(node_base, node_not_ready):
    node_base["status"]["conditions"] = node_not_ready
    with pytest.raises(NagiosCritical):
        check_nodes([node_base])


def test_memory_pressure(node_base, node_memory_pressure):
    node_base["status"]["conditions"] = node_memory_pressure
    with pytest.raises(NagiosWarning):
        check_nodes([node_base])
