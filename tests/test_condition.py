import pytest

from k8s.resource import Condition


def test_textkey_custom(meta):
    textval = "test"

    condition_data = {
        "type": textval,
        "status": "True",
        "lastTransitionTime": "2019-07-03T09:25:48Z"
    }

    assert Condition(condition_data, meta, textkey="type").type == textval


def test_message(meta):
    condition_data = {
        "type": "MemoryPressure",
        "message": "<<message>>",
        "status": "True",
        "lastTransitionTime": "2019-07-03T09:25:48Z"
    }

    assert Condition(condition_data, meta).message == "test_kind test_name: <<message>> since 2019-07-03T09:25:48Z"


def test_textkey_invalid(meta):
    with pytest.raises(AssertionError):
        Condition([0], meta, textkey="foo")
