from unittest.mock import create_autospec
import pytest
import json

from urllib.error import HTTPError
from k8s.http import build_url, _request_prepare, handle_http_error


def test_core_url():
    expected = "https://host:1234/api/v1/resource"
    assert build_url("host", 1234, "resource", is_core=True) == expected


def test_app_url():
    expected = "https://host:1234/apis/apps/v1/resource"
    assert build_url("host", 1234, "resource", is_core=False) == expected


def test_namespaced_app():
    expected = "https://host:1234/apis/apps/v1/namespaces/test/resource"
    assert (
        build_url("host", 1234, "resource", is_core=False, namespace="test") == expected
    )


def test_namespaced_core():
    expected = "https://host:1234/api/v1/namespaces/test/resource"
    assert (
        build_url("host", 1234, "resource", is_core=True, namespace="test") == expected
    )


def test_request_invalid_url():
    with pytest.raises(ValueError):
        assert _request_prepare("invalid_url")


def test_authenticated_request():
    request = _request_prepare(
        "https://kubernetes:1234/api/v1/resource", token="of_zeh_tokens"
    )
    assert request.headers["Authorization"] == "Bearer of_zeh_tokens"

def read():
    raise json.JSONDecodeError("test", "test", 1)

def test_json_decode():
    mock = create_autospec(HTTPError)
    mock.read = read
    mock.reason = "HTTPError reason"

    assert handle_http_error(mock) == "HTTPError reason"

def test_labelSelector_equality_based_equal():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key%3Dvalue"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key=value") == expected


def test_labelSelector_equality_based_double_equal():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key%3D%3Dvalue"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key==value") == expected


def test_labelSelector_equality_based_not_equal():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key%21%3Dvalue"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key!=value") == expected


def test_labelSelector_set_based_in():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key+in+%28value%29"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key in (value)") == expected


def test_labelSelector_set_based_notin():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key+notin+%28value1%2C+value2%29"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key notin (value1, value2)") == expected


def test_labelSelector_set_based_key():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=key"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="key") == expected


def test_labelSelector_set_based_not_key():
    expected = "https://host:1234/api/v1/namespaces/test/resource?labelSelector=%21key"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test",
        labelSelector="!key") == expected

