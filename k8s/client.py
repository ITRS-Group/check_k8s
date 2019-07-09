import json
import re

from urllib import request


class Client:
    def __init__(self, host, port, use_ssl, path_base="/api/v1"):
        """Client for interacting with a Kubernetes TCP server

        :param host: Kubernetes host
        :param port: Kubernetes port
        :param path_base: API base path
        :param use_ssl: Whether to use SSL
        """

        self.host = host
        self.port = port
        self.scheme = "https" if use_ssl else "http"

        self.base_url = "{scheme}://{host}:{port}".format(
            scheme=self.scheme,
            host=self.host,
            port=self.port
        )
        self.path_base = path_base

    @staticmethod
    def build_path(*parts):
        """Convenience method for building an rfc1738 path given any number of parts

        :param parts: path parts
        :return: URL path string
        """

        path = ""

        for part in parts:
            path = "/{0}/{1}".format(path, part)

        return re.sub(r"/+", "/", path.rstrip("/"))

    def get(self, resource, namespace=None):
        """Query the given API resource using HTTP GET

        :param resource: Resource name (pod, replicaset, etc)
        :param namespace: Only look within this namespace
        :return: Response data (dict)
        """

        url = self.base_url + self.build_path(
            self.path_base,
            ("namespaces", namespace, resource) if namespace else resource
        )

        response = request.urlopen(url).read()
        return json.loads(response.decode("utf-8"))
