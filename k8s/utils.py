import re
import os
import json
import ssl

from urllib import request


def build_url(host, port, resource, is_core=True, namespace=None):
    """Kubernetes URL builder

    :param host: Kubernetes host
    :param port: Kubernetes port
    :param is_core: Is core-type API
    :param resource: Resource name
    :param namespace: Optional namespace
    """

    path_base = "api/v1" if is_core else "apis/apps/v1"
    path_parts = ("namespaces", namespace, resource) if namespace else resource

    return "https://{0}:{1}/{path}".format(
        host,
        port,
        path=re.sub(r"/+", "/", os.path.join(path_base, path_parts).rstrip("/"))
    )


def http_request(url, *args, token=None, insecure=False, **kwargs):
    """HTTP Request

    Performs a HTTP request and deserializes the response document (JSON) into a Python dictionary object.

    :param url: HTTP URL
    :param args: Args to pass along to `urllib.request.urlopen`
    :param token: Authentication Bearer Token
    :param insecure: Allow insecure connections
    :param kwargs: Kwargs to pass along to `urllib.request.urlopen`
    :return: data, status
    """

    if token:
        kwargs["headers"] = dict(
            Authorization="Bearer {}".format(token)
        )

    urlopen_opts = {}

    if insecure:
        urlopen_opts.update({
            "context": ssl._create_unverified_context()
        })

    req = request.Request(url, *args, **kwargs)
    resp = request.urlopen(req, **urlopen_opts)
    return json.loads(resp.read().decode("utf-8")).get("items"), resp.getcode()
