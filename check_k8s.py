import sys
import logging
import traceback

from urllib.error import URLError

from k8s import NagiosError, parse_cmdline, components
from k8s.utils import build_url, http_request
from k8s.consts import NAGIOS_MSG


def nagios_msg(msg, channel=sys.stderr):
    print(msg, file=channel)


def main():
    args = parse_cmdline(sys.argv[1:])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    health_check, is_core = components.MAPPINGS[args.resource]

    # Build URL using input arguments
    url = build_url(
        host=args.host,
        port=args.port,
        use_ssl=not args.no_ssl,
        resource=args.resource,
        is_core=is_core,
        namespace=args.namespace
    )

    # Request and check health data
    try:
        response, status = http_request(url)
        result = health_check(response)
        nagios_msg(NAGIOS_MSG.format(level="OK", message=result), channel=sys.stdout)
    except NagiosError as e:
        nagios_msg(NAGIOS_MSG.format(level=e.level, message=e.message))
        sys.exit(e.code)
    except URLError as e:
        nagios_msg(NAGIOS_MSG.format(level="CRITICAL", message=e.reason))
        sys.exit(1)
    except Exception as e:
        if args.debug:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stdout)

        nagios_msg(NAGIOS_MSG.format(level="UNKNOWN", message=e))
        sys.exit(2)


if __name__ == "__main__":
    main()
