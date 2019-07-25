import sys
import logging

from urllib.error import URLError

from k8s import Monitor, NagiosError, parse_cmdline


def main():
    args = parse_cmdline(sys.argv[1:])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

    monitor = Monitor(args.host, args.port, use_ssl=not args.no_ssl)

    try:
        result = monitor.check_wrapped(args.resource, namespace=args.namespace)
        sys.stdout.write(result)
    except NagiosError as e:
        sys.stderr.write(e.message)
        sys.exit(e.code)
    except URLError as e:
        msg = "Server error: {}".format(str(e.reason))
        sys.stderr.write(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
