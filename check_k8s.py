#!/usr/bin/env python3

import sys
import logging
import traceback

from urllib.error import URLError, HTTPError

from k8s.components import MAPPINGS
from k8s.cli import parse_cmdline
from k8s.http import build_url, handle_http_error, make_requests
from k8s.consts import NAGIOS_MSG, NaemonState
from k8s.result import Output


def main():
    parsed = parse_cmdline(sys.argv[1:])

    if parsed.debug:
        logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    health_check, is_core = MAPPINGS[parsed.resource]

    output = []
    urls = []
    if parsed.namespace is not None:
        for i in parsed.namespace.split(","):

            # Build URL using input arguments
            urls.append(
                build_url(
                    host=parsed.host,
                    port=parsed.port,
                    resource=parsed.resource,
                    is_core=is_core,
                    namespace=i,
                    labelSelector=parsed.selector,
                )
            )
    else:
        # Build URL using input arguments
        urls.append(
            build_url(
                host=parsed.host,
                port=parsed.port,
                resource=parsed.resource,
                is_core=is_core,
                namespace=None,
                labelSelector=parsed.selector,
            )
        )
    # Request and check health data
    try:
        output = make_requests(urls, parsed, health_check)
    except HTTPError as e:
        msg = handle_http_error(e)
        output = Output(
            NaemonState.UNKNOWN,
            "{0}: {1}".format(e.code, msg),
            sys.stdout,
        )
    except URLError as e:
        output = Output(NaemonState.UNKNOWN, e.reason, sys.stdout)
    except Exception as e:
        if parsed.debug:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, file=sys.stdout)
        output = Output(NaemonState.UNKNOWN, e, sys.stdout)

    msg = NAGIOS_MSG.format(state=output.state.name, message=output.message)
    output.channel.write(msg)
    sys.exit(output.state.value)


if __name__ == "__main__":
    main()
