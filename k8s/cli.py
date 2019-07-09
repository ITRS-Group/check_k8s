import argparse

from .consts import InputDefault
from .monitor import Monitor


cmdline_args = [
    (
        "--host",
        {
            "dest": "host",
            "action": "store",
            "type": str,
            "default": InputDefault.host.value,
            "help": "Kubernetes host (default: %(default)s)"
        }
    ),
    (
        "--port",
        {
            "dest": "port",
            "action": "store",
            "type": int,
            "default": InputDefault.port.value,
            "help": "Kubernetes port (default: %(default)s)"
        }
    ),
    (
        "--timeout",
        {
            "dest": "timeout",
            "action": "store",
            "type": float,
            "default": InputDefault.timeout.value,
            "help": "Connection timeout in seconds (default: %(default)s)"
        }
    ),
    (
        "--no_ssl",
        {
            "dest": "no_ssl",
            "action": "store_true",
            "default": InputDefault.no_ssl.value,
            "help": "Disable the use of SSL"
        }
    ),
    (
        "--debug",
        {
            "dest": "debug",
            "action": "store_true",
            "default": InputDefault.debug.value,
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
            "choices": [r for r in Monitor.get_mappings()]
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

    for arg, config in cmdline_args:
        parser.add_argument(arg, **config)

    return parser.parse_args(args)
