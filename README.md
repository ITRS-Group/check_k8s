check_k8s: Kubernetes plugin for Nagios
===

![Travis (.com)](https://img.shields.io/travis/com/itrs-group/check_k8s) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ITRS-Group/check_k8s.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ITRS-Group/check_k8s/context:python) ![GitHub](https://img.shields.io/github/license/itrs-group/check_k8s)

Nagios plugin for monitoring Kubernetes Clusters, built using the Python standard library.

It currently supports monitoring of *Pods*, *Nodes* and *Deployments*.

Usage
===

```
$ python3 check_k8s.py -h

usage: check_k8s.py [-h] [--host HOST] [--token TOKEN]
                    [--token_file TOKEN_FILE] [--port PORT]
                    [--timeout TIMEOUT] [--insecure] [--debug] --resource
                    {pods,nodes,deployments} [--namespace NAMESPACE]
                    [--ignore EXPRESSIONS] [--selector SELECTOR]
                    [--version]

Checks health of a Kubernetes cluster

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Kubernetes host (default: 127.0.0.1)
  --token TOKEN         Authentication Token
  --token_file TOKEN_FILE
                        Read Token from file
  --port PORT           Kubernetes port (default: 6443)
  --timeout TIMEOUT     Connection timeout in seconds (default: 15.0)
  --insecure            Continue on insecure SSL connection
  --debug               Enable debug mode
  --resource {pods,nodes,deployments}
                        Resource to monitor
  --namespace NAMESPACE
                        Look only within this namespace
  --ignore EXPRESSIONS  Regular Expression to match against the resource
                        names to ignore in the check results. Can be
                        invoked multiple times.
  --selector SELECTOR   Label selector query to be used.
  --version             show program's version number and exit

```

Component system
===

The check_k8s plugin comes with a simple component system, making it easy to add support for additional Kubernetes Resources.

Resources
---

Typically, components make use of the `k8s.Resource` class, which provides common functionality for working with Kubernetes APIs.

Mappings
---

The `k8s.components.mappings` are automatically picked up by the CLI as Resource Enums and provides a glue between input data and component
entry points.

Extending
---

Take a look at the [existing components](k8s/components) to get started, and check out the [Kubernetes API reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/) for details about the various Kubernetes APIs available.
