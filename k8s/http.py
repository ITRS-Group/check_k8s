import re
import os
import json
import ssl
import urllib.request
import urllib.parse


def build_url(host, port, resource, is_core=True, namespace=None, labelSelector=None):
    """Kubernetes URL builder

    :param host: Kubernetes host
    :param port: Kubernetes port
    :param is_core: Is core-type API
    :param resource: Resource name
    :param namespace: Optional namespace
    """

    path_base = "api/v1" if is_core else "apis/apps/v1"
    path_parts = ["namespaces", namespace, resource] if namespace else (resource,)
    path_full = re.sub(r"/+", "/", os.path.join(path_base, *path_parts).rstrip("/"))

    if labelSelector:
        labelSelector = "?labelSelector=" + urllib.parse.quote_plus(labelSelector)
        path_full += labelSelector

    return "https://{0}:{1}/{2}".format(host, port, path_full)


def _request_prepare(*args, token=None, **kwargs):
    """Prepare HTTP request

    Creates a Request object, to be sent with `urllib.request.urlopen`

    :param args: Args to pass along to `urllib.Request`
    :param token: Authentication Bearer Token
    :param kwargs: Kwargs to pass along to `urllib.Request`
    :return: instance of `urllib.Request`
    """

    headers = kwargs.pop("headers", {})

    if token:
        headers.update({"Authorization": "Bearer {}".format(token)})

    return urllib.request.Request(*args, headers=headers, **kwargs)


def request(*args, insecure=False, **kwargs):
    """Perform HTTP Request

    Performs a HTTP request, returning the response as a Python dictionary.

    :param args: Args to pass along to `urllib.request.urlopen`
    :param insecure: Allow insecure connections
    :param kwargs: Kwargs to pass along to `urllib.request.urlopen`
    :return: data, status
    """

    urlopen_opts = {}
    req = _request_prepare(*args, **kwargs)

    if insecure:
        urlopen_opts.update(dict(context=ssl._create_unverified_context()))

    resp = urllib.request.urlopen(req, **urlopen_opts)
    return json.loads(resp.read().decode("utf-8")).get("items"), resp.getcode()
