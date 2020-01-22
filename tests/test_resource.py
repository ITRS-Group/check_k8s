import pytest

from k8s.components.node import Node
from k8s.exceptions import MetaNotFound, StatusNotFound, ConditionsNotFound


def test_no_meta(node_base):
    del node_base["metadata"]
    with pytest.raises(MetaNotFound):
        Node(node_base)


def test_empty_meta(node_base):
    node_base["metadata"] = {}
    with pytest.raises(MetaNotFound):
        Node(node_base)


def test_no_status(node_base):
    del node_base["status"]
    with pytest.raises(StatusNotFound):
        Node(node_base)


def test_empty_status(node_base):
    node_base["status"] = {}
    with pytest.raises(StatusNotFound):
        Node(node_base)


def test_no_conditions(node_base):
    with pytest.raises(ConditionsNotFound):
        getattr(Node(node_base), "condition")


def test_empty_conditions(node_base):
    with pytest.raises(ConditionsNotFound):
        getattr(Node(node_base), "condition")


def test_kind(node_full):
    class Test(Node):
        def _get_status(self, cnd_type, cnd_status):
            pass

    assert Test(node_full)._kind == "Test"


def test_override_kind(node_full):
    class Test(Node):
        def __init__(self, data):
            super(Test, self).__init__(data, kind="test_kind")

        def _get_status(self, cnd_type, cnd_status):
            pass

    assert Test(node_full)._kind == "test_kind"
