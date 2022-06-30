import pytest


@pytest.fixture
def meta():
    return dict(kind="test_kind", name="test_name")


@pytest.fixture
def node_ready():
    return [
        {
            "type": "MemoryPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientMemory",
            "message": "kubelet has sufficient memory available",
        },
        {
            "type": "DiskPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasNoDiskPressure",
            "message": "kubelet has no disk pressure",
        },
        {
            "type": "PIDPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientPID",
            "message": "kubelet has sufficient PID available",
        },
        {
            "type": "Ready",
            "status": "True",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-29T08:34:34Z",
            "reason": "KubeletReady",
            "message": "kubelet is posting ready status. AppArmor enabled",
        },
    ]


@pytest.fixture
def node_not_ready():
    return [
        {
            "type": "MemoryPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientMemory",
            "message": "kubelet has sufficient memory available",
        },
        {
            "type": "DiskPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasNoDiskPressure",
            "message": "kubelet has no disk pressure",
        },
        {
            "type": "PIDPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientPID",
            "message": "kubelet has sufficient PID available",
        },
        {
            "type": "Ready",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-29T08:34:34Z",
            "reason": "KubeletReady",
            "message": "kubelet is posting ready status. AppArmor enabled",
        },
    ]


@pytest.fixture
def node_memory_pressure():
    return [
        {
            "type": "MemoryPressure",
            "status": "True",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientMemory",
            "message": "kubelet has sufficient memory available",
        },
        {
            "type": "DiskPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasNoDiskPressure",
            "message": "kubelet has no disk pressure",
        },
        {
            "type": "PIDPressure",
            "status": "False",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-03T09:25:48Z",
            "reason": "KubeletHasSufficientPID",
            "message": "kubelet has sufficient PID available",
        },
        {
            "type": "Ready",
            "status": "True",
            "lastHeartbeatTime": "2019-07-30T14:06:15Z",
            "lastTransitionTime": "2019-07-29T08:34:34Z",
            "reason": "KubeletReady",
            "message": "kubelet is posting ready status. AppArmor enabled",
        },
    ]


@pytest.fixture
def node_base():
    return {
        "metadata": {
            "name": "goris",
            "selfLink": "/api/v1/nodes/goris",
            "uid": "64d90ab1-5f4b-4fa2-8cf2-e733560f8d52",
            "resourceVersion": "305709",
            "creationTimestamp": "2019-07-03T09:25:48Z",
            "labels": {
                "beta.kubernetes.io/arch": "amd64",
                "beta.kubernetes.io/os": "linux",
                "kubernetes.io/arch": "amd64",
                "kubernetes.io/hostname": "goris",
                "kubernetes.io/os": "linux",
                "microk8s.io/cluster": "true",
            },
            "annotations": {
                "node.alpha.kubernetes.io/ttl": "0",
                "volumes.kubernetes.io/controller-managed-attach-detach": "true",
            },
        },
        "spec": {},
        "status": {
            "capacity": {
                "cpu": "8",
                "ephemeral-storage": "489703416Ki",
                "hugepages-1Gi": "0",
                "hugepages-2Mi": "0",
                "memory": "16181888Ki",
                "pods": "110",
            },
            "allocatable": {
                "cpu": "8",
                "ephemeral-storage": "488654840Ki",
                "hugepages-1Gi": "0",
                "hugepages-2Mi": "0",
                "memory": "16079488Ki",
                "pods": "110",
            },
            "conditions": [],
            "addresses": [
                {"type": "InternalIP", "address": "172.27.75.196"},
                {"type": "Hostname", "address": "goris"},
            ],
            "daemonEndpoints": {"kubeletEndpoint": {"Port": 10250}},
            "nodeInfo": {
                "machineID": "991c63bd7f3a443fb923ba1b0fb0995f",
                "systemUUID": "22c617cc-23e3-11b2-a85c-ee76da7e66ad",
                "bootID": "90399b5a-ce60-4767-8655-56d1853e5c78",
                "kernelVersion": "4.18.0-25-generic",
                "osImage": "Ubuntu 18.10",
                "containerRuntimeVersion": "containerd://1.2.5",
                "kubeletVersion": "v1.15.0",
                "kubeProxyVersion": "v1.15.0",
                "operatingSystem": "linux",
                "architecture": "amd64",
            },
            "images": [
                {
                    "names": [
                        "k8s.gcr.io/heapster-grafana-amd64@sha256:4a472eb4df03f4f557d80e7c6b903d9c8fe31493108b99fbd6da6540b5448d70",
                        "k8s.gcr.io/heapster-grafana-amd64:v4.4.3",
                    ],
                    "sizeBytes": 51566280,
                },
                {
                    "names": [
                        "k8s.gcr.io/kubernetes-dashboard-amd64@sha256:0ae6b69432e78069c5ce2bcde0fe409c5c4d6f0f4d9cd50a17974fea38898747",
                        "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1",
                    ],
                    "sizeBytes": 44907311,
                },
                {
                    "names": [
                        "k8s.gcr.io/heapster-amd64@sha256:59fb34ffd902282d06fcc940a906df9787edf78651743f4c8c4abf8b3468c0e9",
                        "k8s.gcr.io/heapster-amd64:v1.5.2",
                    ],
                    "sizeBytes": 20088732,
                },
                {
                    "names": [
                        "docker.io/coredns/coredns@sha256:e83beb5e43f8513fa735e77ffc5859640baea30a882a11cc75c4c3244a737d3c",
                        "docker.io/coredns/coredns:1.5.0",
                    ],
                    "sizeBytes": 13341835,
                },
                {
                    "names": [
                        "docker.io/cdkbot/addon-resizer-amd64@sha256:a5ff31fb60d32e02780441fc81bc91dd549097d6afeef3c6decb6005289795af",
                        "docker.io/cdkbot/addon-resizer-amd64:1.8.1",
                    ],
                    "sizeBytes": 8343051,
                },
                {
                    "names": [
                        "k8s.gcr.io/heapster-influxdb-amd64@sha256:f433e331c1865ad87bc5387589965528b78cd6b1b2f61697e589584d690c1edd",
                        "k8s.gcr.io/heapster-influxdb-amd64:v1.3.3",
                    ],
                    "sizeBytes": 4748077,
                },
                {
                    "names": [
                        "k8s.gcr.io/pause@sha256:f78411e19d84a252e53bff71a4407a5686c46983a2c2eeed83929b888179acea",
                        "k8s.gcr.io/pause:3.1",
                    ],
                    "sizeBytes": 317164,
                },
            ],
        },
    }


@pytest.fixture
def node_full(node_base, node_ready):
    node_base["status"]["conditions"] = node_ready
    return node_base


@pytest.fixture
def pod_base():
    return {
        "metadata": {
            "name": "monitoring-influxdb-grafana-v4-6b6954958c-n4mtz",
            "generateName": "monitoring-influxdb-grafana-v4-6b6954958c-",
            "namespace": "kube-system",
            "selfLink": "/api/v1/namespaces/kube-system/pods/monitoring-influxdb-grafana-v4-6b6954958c-n4mtz",
            "uid": "cdbd476e-015e-4362-9fe2-59409edc4f2d",
            "resourceVersion": "176358",
            "creationTimestamp": "2019-07-08T22:22:38Z",
            "labels": {
                "k8s-app": "influxGrafana",
                "pod-template-hash": "6b6954958c",
                "version": "v4",
            },
            "annotations": {"scheduler.alpha.kubernetes.io/critical-pod": ""},
            "ownerReferences": [
                {
                    "apiVersion": "apps/v1",
                    "kind": "ReplicaSet",
                    "name": "monitoring-influxdb-grafana-v4-6b6954958c",
                    "uid": "54dd9750-2818-40b9-af6b-269ed9dda0cd",
                    "controller": True,
                    "blockOwnerDeletion": True,
                }
            ],
        },
        "spec": {
            "volumes": [
                {"name": "influxdb-persistent-storage", "emptyDir": {}},
                {"name": "grafana-persistent-storage", "emptyDir": {}},
                {
                    "name": "default-token-279xh",
                    "secret": {"secretName": "default-token-279xh", "defaultMode": 420},
                },
            ],
            "containers": [],
            "restartPolicy": "Always",
            "terminationGracePeriodSeconds": 30,
            "dnsPolicy": "ClusterFirst",
            "serviceAccountName": "default",
            "serviceAccount": "default",
            "nodeName": "goris",
            "securityContext": {},
            "schedulerName": "default-scheduler",
            "tolerations": [
                {"key": "node-role.kubernetes.io/master", "effect": "NoSchedule"},
                {"key": "CriticalAddonsOnly", "operator": "Exists"},
                {
                    "key": "node.kubernetes.io/not-ready",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300,
                },
                {
                    "key": "node.kubernetes.io/unreachable",
                    "operator": "Exists",
                    "effect": "NoExecute",
                    "tolerationSeconds": 300,
                },
            ],
            "priorityClassName": "system-cluster-critical",
            "priority": 2000000000,
            "enableServiceLinks": True,
        },
        "status": {
            "phase": "Running",
            "conditions": [],
            "hostIP": "172.27.75.196",
            "podIP": "10.1.1.9",
            "startTime": "2019-07-08T22:22:41Z",
            "containerStatuses": [],
            "qosClass": "Guaranteed",
        },
    }


@pytest.fixture
def pod_containers():
    return [
        {
            "name": "grafana",
            "state": {"running": {"startedAt": "2019-07-29T08:34:28Z"}},
            "lastState": {
                "terminated": {
                    "exitCode": 255,
                    "reason": "Unknown",
                    "startedAt": "2019-07-29T07:59:31Z",
                    "finishedAt": "2019-07-29T08:34:09Z",
                    "containerID": "containerd://401fe3214c6b2d170ca376aecf1e8eba96ba250b7e20631c1b3358aef3506d85",
                }
            },
            "ready": True,
            "restartCount": 15,
            "image": "k8s.gcr.io/heapster-grafana-amd64:v4.4.3",
            "imageID": "k8s.gcr.io/heapster-grafana-amd64@sha256:4a472eb4df03f4f557d80e7c6b903d9c8fe31493108b99fbd6da6540b5448d70",
            "containerID": "containerd://fa28c5406867a4d133a89bad91fb5dd462d13e440e9c12fee680bbad8699156f",
        },
        {
            "name": "influxdb",
            "state": {"running": {"startedAt": "2019-07-29T08:34:27Z"}},
            "lastState": {
                "terminated": {
                    "exitCode": 255,
                    "reason": "Unknown",
                    "startedAt": "2019-07-29T07:59:30Z",
                    "finishedAt": "2019-07-29T08:34:09Z",
                    "containerID": "containerd://5d797bdc758de304161e5078b650cc95a22dc619dedc80ead9da04a4cf367316",
                }
            },
            "ready": True,
            "restartCount": 17,
            "image": "k8s.gcr.io/heapster-influxdb-amd64:v1.3.3",
            "imageID": "k8s.gcr.io/heapster-influxdb-amd64@sha256:f433e331c1865ad87bc5387589965528b78cd6b1b2f61697e589584d690c1edd",
            "containerID": "containerd://54545d7e41d8a45a4b16ea0f005767574998564885714e2b8552a8df74b86fa0",
        },
    ]


@pytest.fixture
def pod_ready():
    return [
        {
            "type": "Initialized",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:41Z",
        },
        {
            "type": "Ready",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "ContainersReady",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "PodScheduled",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:38Z",
        },
    ]


@pytest.fixture
def pod_not_ready():
    return [
        {
            "type": "Initialized",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:41Z",
        },
        {
            "type": "Ready",
            "status": "False",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "ContainersReady",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "PodScheduled",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:38Z",
        },
    ]


@pytest.fixture
def pod_condition_other():
    return [
        {
            "type": "Initialized",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:41Z",
        },
        {
            "type": "Ready",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "ContainersReady",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "PodScheduled",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:38Z",
        },
        {
            "type": "SomethingBad",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:38Z",
        },
    ]


@pytest.fixture
def pod_containers_not_ready():
    return [
        {
            "type": "Initialized",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:41Z",
        },
        {
            "type": "Ready",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "ContainersReady",
            "status": "False",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-29T08:34:28Z",
        },
        {
            "type": "PodScheduled",
            "status": "True",
            "lastProbeTime": None,
            "lastTransitionTime": "2019-07-08T22:22:38Z",
        },
    ]


@pytest.fixture
def pod_full(pod_base, pod_ready, pod_containers):
    pod_base["status"]["conditions"] = pod_ready
    pod_base["status"]["containerStatuses"] = pod_containers
    return pod_base


@pytest.fixture
def deployment_base():
    return {
        "metadata": {
            "name": "coredns",
            "namespace": "kube-system",
            "selfLink": "/apis/apps/v1/namespaces/kube-system/deployments/coredns",
            "uid": "f021d1a8-6c1e-49f6-90c2-2a0177e5f1c8",
            "resourceVersion": "176382",
            "generation": 1,
            "creationTimestamp": "2019-07-08T22:22:28Z",
            "labels": {
                "addonmanager.kubernetes.io/mode": "Reconcile",
                "k8s-app": "kube-dns",
                "kubernetes.io/cluster-service": "true",
                "kubernetes.io/name": "CoreDNS",
            },
            "annotations": {
                "deployment.kubernetes.io/revision": "1",
                "kubectl.kubernetes.io/last-applied-configuration": '{"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"Reconcile","k8s-app":"kube-dns","kubernetes.io/cluster-service":"true","kubernetes.io/name":"CoreDNS"},"name":"coredns","namespace":"kube-system"},"spec":{"selector":{"matchLabels":{"k8s-app":"kube-dns"}},"strategy":{"rollingUpdate":{"maxSurge":"10%","maxUnavailable":0},"type":"RollingUpdate"},"template":{"metadata":{"annotations":{"scheduler.alpha.kubernetes.io/critical-pod":""},"labels":{"k8s-app":"kube-dns"}},"spec":{"containers":[{"args":["-conf","/etc/coredns/Corefile"],"image":"coredns/coredns:1.5.0","imagePullPolicy":"IfNotPresent","livenessProbe":{"failureThreshold":5,"httpGet":{"path":"/health","port":8080,"scheme":"HTTP"},"initialDelaySeconds":60,"successThreshold":1,"timeoutSeconds":5},"name":"coredns","ports":[{"containerPort":53,"name":"dns","protocol":"UDP"},{"containerPort":53,"name":"dns-tcp","protocol":"TCP"},{"containerPort":9153,"name":"metrics","protocol":"TCP"}],"readinessProbe":{"httpGet":{"path":"/ready","port":8181,"scheme":"HTTP"}},"resources":{"limits":{"memory":"170Mi"},"requests":{"cpu":"100m","memory":"70Mi"}},"securityContext":{"allowPrivilegeEscalation":false,"capabilities":{"add":["NET_BIND_SERVICE"],"drop":["all"]},"readOnlyRootFilesystem":true},"volumeMounts":[{"mountPath":"/etc/coredns","name":"config-volume","readOnly":true}]}],"dnsPolicy":"Default","priorityClassName":"system-cluster-critical","serviceAccountName":"coredns","tolerations":[{"key":"CriticalAddonsOnly","operator":"Exists"}],"volumes":[{"configMap":{"items":[{"key":"Corefile","path":"Corefile"}],"name":"coredns"},"name":"config-volume"}]}}}}\n',
            },
        },
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"k8s-app": "kube-dns"}},
            "template": {
                "metadata": {
                    "creationTimestamp": None,
                    "labels": {"k8s-app": "kube-dns"},
                    "annotations": {"scheduler.alpha.kubernetes.io/critical-pod": ""},
                },
                "spec": {
                    "volumes": [
                        {
                            "name": "config-volume",
                            "configMap": {
                                "name": "coredns",
                                "items": [{"key": "Corefile", "path": "Corefile"}],
                                "defaultMode": 420,
                            },
                        }
                    ],
                    "containers": [
                        {
                            "name": "coredns",
                            "image": "coredns/coredns:1.5.0",
                            "args": ["-conf", "/etc/coredns/Corefile"],
                            "ports": [
                                {"name": "dns", "containerPort": 53, "protocol": "UDP"},
                                {
                                    "name": "dns-tcp",
                                    "containerPort": 53,
                                    "protocol": "TCP",
                                },
                                {
                                    "name": "metrics",
                                    "containerPort": 9153,
                                    "protocol": "TCP",
                                },
                            ],
                            "resources": {
                                "limits": {"memory": "170Mi"},
                                "requests": {"cpu": "100m", "memory": "70Mi"},
                            },
                            "volumeMounts": [
                                {
                                    "name": "config-volume",
                                    "readOnly": True,
                                    "mountPath": "/etc/coredns",
                                }
                            ],
                            "livenessProbe": {
                                "httpGet": {
                                    "path": "/health",
                                    "port": 8080,
                                    "scheme": "HTTP",
                                },
                                "initialDelaySeconds": 60,
                                "timeoutSeconds": 5,
                                "periodSeconds": 10,
                                "successThreshold": 1,
                                "failureThreshold": 5,
                            },
                            "readinessProbe": {
                                "httpGet": {
                                    "path": "/ready",
                                    "port": 8181,
                                    "scheme": "HTTP",
                                },
                                "timeoutSeconds": 1,
                                "periodSeconds": 10,
                                "successThreshold": 1,
                                "failureThreshold": 3,
                            },
                            "terminationMessagePath": "/dev/termination-log",
                            "terminationMessagePolicy": "File",
                            "imagePullPolicy": "IfNotPresent",
                            "securityContext": {
                                "capabilities": {
                                    "add": ["NET_BIND_SERVICE"],
                                    "drop": ["all"],
                                },
                                "readOnlyRootFilesystem": True,
                                "allowPrivilegeEscalation": False,
                            },
                        }
                    ],
                    "restartPolicy": "Always",
                    "terminationGracePeriodSeconds": 30,
                    "dnsPolicy": "Default",
                    "serviceAccountName": "coredns",
                    "serviceAccount": "coredns",
                    "securityContext": {},
                    "schedulerName": "default-scheduler",
                    "tolerations": [
                        {"key": "CriticalAddonsOnly", "operator": "Exists"}
                    ],
                    "priorityClassName": "system-cluster-critical",
                },
            },
            "strategy": {
                "type": "RollingUpdate",
                "rollingUpdate": {"maxUnavailable": 0, "maxSurge": "10%"},
            },
            "revisionHistoryLimit": 10,
            "progressDeadlineSeconds": 600,
        },
        "status": {
            "observedGeneration": 1,
        },
    }


@pytest.fixture
def deployment_replicas_minimal():
    return {
        "replicas": 1,
        "updatedReplicas": 1,
        "readyReplicas": 1,
        "availableReplicas": 1
    }


@pytest.fixture
def deployment_replicas_degraded():
    return {
        "replicas": 2,
        "updatedReplicas": 1,
        "readyReplicas": 1,
        "availableReplicas": 2
    }


@pytest.fixture
def deployment_conditions():
    return [
        {
            "type": "Progressing",
            "status": "True",
            "lastUpdateTime": "2019-07-08T22:23:02Z",
            "lastTransitionTime": "2019-07-08T22:22:28Z",
            "reason": "NewReplicaSetAvailable",
            "message": 'ReplicaSet "coredns-f7867546d" has successfully progressed.',
        },
        {
            "type": "Available",
            "status": "True",
            "lastUpdateTime": "2019-07-29T08:34:31Z",
            "lastTransitionTime": "2019-07-29T08:34:31Z",
            "reason": "MinimumReplicasAvailable",
            "message": "Deployment has minimum availability.",
        },
    ]


@pytest.fixture
def deployment_full(deployment_base, deployment_conditions, deployment_replicas_minimal):
    deployment_base["status"]["conditions"] = deployment_conditions
    deployment_base["status"].update(deployment_replicas_minimal)
    return deployment_base


@pytest.fixture
def ignore_none():
    return []


@pytest.fixture
def ignore_all_node(node_base):
    return [node_base["metadata"]["name"]]


@pytest.fixture
def ignore_all_deployment(deployment_base):
    return [deployment_base["metadata"]["name"]]


@pytest.fixture
def ignore_all_pod(pod_base):
    return [pod_base["metadata"]["name"]]
