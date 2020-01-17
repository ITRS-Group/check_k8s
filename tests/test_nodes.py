from k8s.result import Result, Output
from k8s.components.node import check_nodes, Node
from k8s.consts import RESULT_CRITICAL, RESULT_SUCCESS, RESULT_WARNING


def test_kind(node_full):
    assert Node(node_full).unschedulable is False
    assert Node(node_full)._kind == "Node"


def test_result(node_full):
    result = check_nodes([node_full])
    assert isinstance(result, Result)


def test_output(node_full):
    output = check_nodes([node_full]).output
    assert isinstance(output, Output)


def test_ready(node_base, node_ready):
    node_base["status"]["conditions"] = node_ready
    assert check_nodes([node_base]).output.message.startswith(RESULT_SUCCESS)


def test_not_ready(node_base, node_not_ready):
    node_base["status"]["conditions"] = node_not_ready
    assert check_nodes([node_base]).output.message.startswith(RESULT_CRITICAL)


def test_memory_pressure(node_base, node_memory_pressure):
    node_base["status"]["conditions"] = node_memory_pressure
    assert check_nodes([node_base]).output.message.startswith(RESULT_WARNING)
