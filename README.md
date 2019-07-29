check_k8s: Kubernetes plugin for Nagios
===

Modular Nagios plugin built using the Python standard library for monitoring Kubernetes Clusters.

It currently supports monitoring of *Pods*, *Nodes* and *Deployments*. 

Usage
===

```
$ python3 check_k8s.py -h

python3 check_k8s.py -h                                                                                                                                                                 rbw@goris
usage: check_k8s.py [-h] [--host HOST] [--token TOKEN] [--port PORT]
                    [--timeout TIMEOUT] [--insecure] [--debug] --resource
                    {pods,nodes,deployments} [--namespace NAMESPACE]

Checks health of a Kubernetes cluster

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Kubernetes host (default: 127.0.0.1)
  --token TOKEN         Authentication Bearer Token
  --port PORT           Kubernetes port (default: 16443)
  --timeout TIMEOUT     Connection timeout in seconds (default: 15.0)
  --insecure            Continue on insecure SSL connection
  --debug               Enable debug mode
  --resource {pods,nodes,deployments}
                        Resource to monitor
  --namespace NAMESPACE
                        Look only within this namespace
```

Component system
===

The check_k8s plugin comes with a simple component system, which not only simplifies testing and
provides modularity and maintainability--it also makes extending the plugin with more monitoring features easy as pie.

Resources
---

Typically, components make use of the `k8s.Resource` class, which provides common functionality for working with Kubernetes APIs.

Mappings
---

The `k8s.components.mappings` are automatically picked up by the CLI as Enums and provides a glue between input data and component
entry points.

Extending
---

Take a look at the [existing components](k8s/components) to get started, and check out the [Kubernetes API reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/) for details about the various Kubernetes APIs available.
