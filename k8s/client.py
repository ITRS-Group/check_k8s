import json
import re

from urllib import request

from .pod import Pod


class Client:
    def __init__(self, *address, use_ssl=True, path_base="/api/v1"):
        """Client for interacting with a Kubernetes TCP server

        :param address: TCP address (host, port) tuple
        :param use_ssl: Whether to use SSL, default to true
        """

        self.host, self.port = address
        self._path_base = path_base
        self.scheme = "https" if use_ssl else "http"

    @staticmethod
    def build_path(*parts):
        """Convenience method for building an rfc1738 path given any number of parts

        :param parts: path parts
        :return: URL path string
        """

        path = ""

        for part in parts:
            path = f"/{path}/{part}"

        return re.sub(r"/+", "/", path.rstrip("/"))

    @property
    def _base_url(self):
        return "{scheme}://{host}:{port}".format(scheme=self.scheme, host=self.host, port=self.port)

    def get(self, resource, namespace=None, pod_name=None):
        if namespace:
            resource = "namespaces", namespace, resource, pod_name or ""

        url = self._base_url + self.build_path(self._path_base, resource)
        response = request.urlopen(url).read()
        return json.loads(response.decode("utf-8"))

    def get_pods(self, **kwargs):
        for pod_data in self.get("pods", **kwargs).get("items"):
            yield Pod(pod_data)
