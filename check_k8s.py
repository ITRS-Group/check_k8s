import sys
import logging
import traceback

from collections import namedtuple
from urllib.error import URLError

from k8s.components import MAPPINGS
from k8s.cli import parse_cmdline
from k8s.http import build_url, request
from k8s.consts import NAGIOS_MSG, State
from k8s.exceptions import PluginException


Output = namedtuple("Output", ["state", "message", "channel"])


def main():
    args = parse_cmdline(sys.argv[1:])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    health_check, is_core = MAPPINGS[args.resource]

    # Build URL using input arguments
    url = build_url(
        host=args.host,
        port=args.port,
        resource=args.resource,
        is_core=is_core,
        namespace=args.namespace
    )

    # Request and check health data
    try:
        response, status = request(url, token=args.token, insecure=args.insecure)
        result = health_check(response)
        output = Output(State.OK, result, sys.stdout)
    except PluginException as e:
        output = Output(e.state, e.message, sys.stderr)
    except URLError as e:
        output = Output(State.UNKNOWN, e.reason, sys.stderr)
    except Exception as e:
        if args.debug:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stdout)

        output = Output(State.UNKNOWN, e, sys.stderr)

    msg = NAGIOS_MSG.format(state=output.state.name, message=output.message)
    print(msg, file=output.channel)
    sys.exit(output.state.value)


if __name__ == "__main__":
    main()
