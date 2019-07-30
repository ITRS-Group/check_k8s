import pytest

from k8s.resource import Resource
from k8s.exceptions import MetaNotFound, StatusNotFound, ConditionsNotFound


def test_no_meta(node_base):
    del node_base["metadata"]
    with pytest.raises(MetaNotFound):
        Resource(node_base)


def test_empty_meta(node_base):
    node_base["metadata"] = {}
    with pytest.raises(MetaNotFound):
        Resource(node_base)


def test_no_status(node_base):
    del node_base["status"]
    with pytest.raises(StatusNotFound):
        Resource(node_base)


def test_empty_status(node_base):
    node_base["status"] = {}
    with pytest.raises(StatusNotFound):
        Resource(node_base)


def test_no_conditions(node_base):
    with pytest.raises(ConditionsNotFound):
        Resource(node_base)


def test_empty_conditions(node_base):
    with pytest.raises(ConditionsNotFound):
        Resource(node_base)


def test_kind(node_full):
    assert Resource(node_full)._kind == "Resource"


def test_override_kind(node_full):
    assert Resource(node_full, kind="test_kind")._kind == "test_kind"


def test_condition_textkey(node_base):
    textkey = "message"
    node_base["status"]["conditions"] = [{
        "type": "MemoryPressure",
        "message": "<<message>>",
        "status": "True",
        "lastTransitionTime": "2019-07-03T09:25:48Z"
    }]

    assert Resource(node_base, condition_textkey=textkey).conditions[0].text == "<<message>>"
