import argparse

from enum import Enum

from .components import MAPPINGS


class Default(Enum):
    timeout = 15.0
    host = "127.0.0.1"
    port = 8080
    no_ssl = False
    debug = False
    namespace = None
    resource = None


opts = [
    (
        "--host",
        {
            "dest": "host",
            "action": "store",
            "type": str,
            "default": Default.host.value,
            "help": "Kubernetes host (default: %(default)s)"
        }
    ),
    (
        "--port",
        {
            "dest": "port",
            "action": "store",
            "type": int,
            "default": Default.port.value,
            "help": "Kubernetes port (default: %(default)s)"
        }
    ),
    (
        "--timeout",
        {
            "dest": "timeout",
            "action": "store",
            "type": float,
            "default": Default.timeout.value,
            "help": "Connection timeout in seconds (default: %(default)s)"
        }
    ),
    (
        "--no_ssl",
        {
            "dest": "no_ssl",
            "action": "store_true",
            "default": Default.no_ssl.value,
            "help": "Disable the use of SSL"
        }
    ),
    (
        "--debug",
        {
            "dest": "debug",
            "action": "store_true",
            "default": Default.debug.value,
            "help": "Enable debug mode"
        }
    ),
    (
        "--resource",
        {
            "dest": "resource",
            "action": "store",
            "type": str,
            "required": True,
            "help": "Resource to monitor",
            "choices": list(MAPPINGS)
        }
    ),
    (
        "--namespace",
        {
            "dest": "namespace",
            "action": "store",
            "type": str,
            "required": False,
            "help": "Look only within this namespace",
        }
    )
]


def parse_cmdline(args):
    parser = argparse.ArgumentParser(
        description="Checks health of a Kubernetes cluster"
    )

    for opt, conf in opts:
        parser.add_argument(opt, **conf)

    return parser.parse_args(args)
