import pytest

from k8s.http import build_url, _request_prepare


def test_core_url():
    expected = "https://host:1234/api/v1/resource"
    assert build_url("host", 1234, "resource", is_core=True) == expected


def test_app_url():
    expected = "https://host:1234/apis/apps/v1/resource"
    assert build_url("host", 1234, "resource", is_core=False) == expected


def test_namespaced_app():
    expected = "https://host:1234/apis/apps/v1/namespaces/test/resource"
    assert build_url("host", 1234, "resource", is_core=False, namespace="test") == expected


def test_namespaced_core():
    expected = "https://host:1234/api/v1/namespaces/test/resource"
    assert build_url("host", 1234, "resource", is_core=True, namespace="test") == expected


def test_request_invalid_url():
    with pytest.raises(ValueError):
        assert _request_prepare("invalid_url")


def test_authenticated_request():
    request = _request_prepare("https://kubernetes:1234/api/v1/resource", token="of_zeh_tokens")
    assert request.headers["Authorization"] == "Bearer of_zeh_tokens"

