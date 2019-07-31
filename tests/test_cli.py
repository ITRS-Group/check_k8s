import pytest

from k8s.cli import parse_cmdline, Default


def test_resource_valid():
    assert parse_cmdline(['--resource', 'nodes']).resource == "nodes"
    assert parse_cmdline(['--resource', 'deployments']).resource == "deployments"
    assert parse_cmdline(['--resource', 'pods']).resource == "pods"


def test_resource_invalid():
    with pytest.raises(SystemExit):
        parse_cmdline(['--resource', 'node'])

    with pytest.raises(SystemExit):
        parse_cmdline(['--resource', 'PODS'])

    with pytest.raises(SystemExit):
        parse_cmdline(['--resource', 'Deployments'])

    with pytest.raises(SystemExit):
        parse_cmdline([])


def test_opts():
    def parser(args):
        return parse_cmdline(['--resource', 'nodes'] + args)

    assert parser(["--namespace", "test"]).namespace == "test"
    assert parser(["--debug"]).debug is True
    assert parser(["--insecure"]).insecure is True
    assert parser(["--timeout", "123.0"]).timeout == 123.0
    assert parser(["--port", "1234"]).port == 1234
    assert parser(["--token", "token123"]).token == "token123"
    assert parser([]).debug is Default.debug.value
    assert parser([]).insecure is Default.insecure.value
    assert parser([]).timeout is Default.timeout.value
    assert parser([]).port is Default.port.value
    assert parser([]).host is Default.host.value
