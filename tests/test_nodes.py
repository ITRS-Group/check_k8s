from k8s.result import Result, Output
from k8s.components.node import check_nodes, Node
from k8s.consts import RESULT_CRITICAL, RESULT_SUCCESS, RESULT_WARNING


def test_kind(node_full):
    assert Node(node_full).unschedulable is False
    assert Node(node_full)._kind == "Node"


def test_result(node_full, ignore_none):
    result = check_nodes([node_full], ignore_none)
    assert isinstance(result, Result)


def test_output(node_full, ignore_none):
    output = check_nodes([node_full], ignore_none).output
    assert isinstance(output, Output)


def test_ready(node_base, node_ready, ignore_none):
    node_base["status"]["conditions"] = node_ready
    assert check_nodes([node_base], ignore_none).output.message.startswith(RESULT_SUCCESS)


def test_ignore_ready(node_base, node_ready, ignore_all_node):
    node_base["status"]["conditions"] = node_ready
    message = check_nodes([node_base], ignore_all_node).output.message
    lines = message.split('\n')
    assert lines[0] == RESULT_SUCCESS
    assert lines[1] == "|available=0 unavailable=0 degraded=0 unschedulable=0"


def test_not_ready(node_base, node_not_ready, ignore_none):
    node_base["status"]["conditions"] = node_not_ready
    assert check_nodes([node_base], ignore_none).output.message.startswith(RESULT_CRITICAL)


def test_ignored_not_ready(node_base, node_not_ready, ignore_all_node):
    node_base["status"]["conditions"] = node_not_ready
    message = check_nodes([node_base], ignore_all_node).output.message
    lines = message.split('\n')
    assert lines[0] == RESULT_SUCCESS
    assert lines[1] == "|available=0 unavailable=0 degraded=0 unschedulable=0"


def test_memory_pressure(node_base, node_memory_pressure, ignore_none):
    node_base["status"]["conditions"] = node_memory_pressure
    assert check_nodes([node_base], ignore_none).output.message.startswith(RESULT_WARNING)


def test_ignored_memory_pressure(node_base, node_memory_pressure, ignore_all_node):
    node_base["status"]["conditions"] = node_memory_pressure
    message = check_nodes([node_base], ignore_all_node).output.message
    lines = message.split('\n')
    assert lines[0] == RESULT_SUCCESS
    assert lines[1] == "|available=0 unavailable=0 degraded=0 unschedulable=0"
