import logging

from k8s import Client, Monitor

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")


def main():
    client = Client("localhost", 8080, use_ssl=False)
    mon = Monitor(client)

    mon.pod_status()


if __name__ == "__main__":
    main()
