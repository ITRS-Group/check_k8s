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

    msg = Condition(condition_data, meta).message
    assert msg == "test_kind test_name: condition MemoryPressure since 2019-07-03T09:25:48Z"


def test_message_negative(meta):
    condition_data = {
        "type": "Ready",
        "message": "<<message>>",
        "status": "False",
        "lastTransitionTime": "2019-07-03T09:25:48Z"
    }

    msg = Condition(condition_data, meta).message
    assert msg == "test_kind test_name: condition not Ready since 2019-07-03T09:25:48Z"


def test_textkey_invalid(meta):
    with pytest.raises(AssertionError):
        Condition([0], meta, textkey="foo")
