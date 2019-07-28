import re
import os
import json

from urllib import request


def build_url(host, port, resource, use_ssl, is_core=True, namespace=None):
    """Kubernetes URL builder

    :param host: Kubernetes host
    :param port: Kubernetes port
    :param is_core: Is core-type API
    :param resource: Resource name
    :param use_ssl: Whether to use SSL
    :param namespace: Optional namespace
    """

    scheme = "https" if use_ssl else "http"
    path_base = "api/v1" if is_core else "apis/apps/v1"
    path_parts = ("namespaces", namespace, resource) if namespace else resource

    return "{0}://{1}:{2}/{path}".format(
        scheme,
        host,
        port,
        path=re.sub(r"/+", "/", os.path.join(path_base, path_parts).rstrip("/"))
    )


def http_request(url, *args, **kwargs):
    """HTTP Request

    Performs a HTTP request and deserializes the response document (JSON) into a Python dictionary object.

    :param url: HTTP URL
    :param args: Args to pass along to `urllib.request.urlopen`
    :param kwargs: Kwargs to pass along to `urllib.request.urlopen`
    :return: data, status
    """

    response = request.urlopen(url, *args, **kwargs)
    return json.loads(response.read().decode("utf-8")).get("items"), response.getcode()
