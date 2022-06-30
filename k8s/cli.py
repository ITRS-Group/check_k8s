import argparse

from enum import Enum

from .components import MAPPINGS
from k8s.consts import VERSION


class Default(Enum):
    timeout = 15.0
    host = "127.0.0.1"
    port = 6443
    token = None
    token_file = None
    insecure = False
    debug = False
    namespace = None
    resource = None
    ignore = None
    selector = None


opts = [
    (
        "--host",
        {
            "dest": "host",
            "action": "store",
            "type": str,
            "default": Default.host.value,
            "help": "Kubernetes host (default: %(default)s)",
        },
    ),
    (
        "--port",
        {
            "dest": "port",
            "action": "store",
            "type": int,
            "default": Default.port.value,
            "help": "Kubernetes port (default: %(default)s)",
        },
    ),
    (
        "--token",
        {
            "dest": "token",
            "action": "store",
            "type": str,
            "nargs": "?",
            "default": Default.token.value,
            "help": "Authentication Token",
        },
    ),
    (
        "--token_file",
        {
            "dest": "token_file",
            "action": "store",
            "type": str,
            "nargs": "?",
            "default": Default.token_file.value,
            "help": "Read Token from file",
        },
    ),
    (
        "--timeout",
        {
            "dest": "timeout",
            "action": "store",
            "type": float,
            "default": Default.timeout.value,
            "help": "Connection timeout in seconds (default: %(default)s)",
        },
    ),
    (
        "--insecure",
        {
            "dest": "insecure",
            "action": "store_true",
            "default": Default.insecure.value,
            "help": "Continue on insecure SSL connection",
        },
    ),
    (
        "--debug",
        {
            "dest": "debug",
            "action": "store_true",
            "default": Default.debug.value,
            "help": "Enable debug mode",
        },
    ),
    (
        "--resource",
        {
            "dest": "resource",
            "action": "store",
            "type": str,
            "required": True,
            "help": "Resource to monitor",
            "choices": list(MAPPINGS),
        },
    ),
    (
        "--namespace",
        {
            "dest": "namespace",
            "action": "store",
            "type": str,
            "nargs": "?",
            "default": Default.namespace.value,
            "required": False,
            "help": "Look only within this namespace",
        },
    ),
    (
        "--ignore",
        {
            "dest": "expressions",
            "action": "append",
            "type": str,
            "default": Default.ignore.value,
            "required": False,
            "help": "Regular Expression to match against\
                    the resource names to ignore in the check results.\
                    Can be invoked multiple times.",
        },
    ),
    (
        "--selector",
        {
            "dest": "selector",
            "action": "store",
            "type": str,
            "default": Default.selector.value,
            "required": False,
            "help": "Label selector query to be used.",
        },
    ),
    (
        "--version",
        {
            "action": "version",
            "version": "%(prog)s {}".format(VERSION),
        },
    ),
]


def parse_cmdline(args):
    parser = argparse.ArgumentParser(
        description="Checks health of a Kubernetes cluster"
    )

    for opt, conf in opts:
        parser.add_argument(opt, **conf)

    parsed = parser.parse_args(args)

    if parsed.token and parsed.token_file:
        parser.error("--token and --token_file options are mutually exclusive.")
    elif parsed.token_file:
        with open(parsed.token_file) as fh:
            parsed.token = fh.read().strip()

    return parsed
