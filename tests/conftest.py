import pytest


@pytest.fixture
def meta():
    return dict(kind="test_kind", name="test_name")


@pytest.fixture
def node_ready():
    return [
        {'type': 'MemoryPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientMemory',
         'message': 'kubelet has sufficient memory available'},
        {'type': 'DiskPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasNoDiskPressure',
         'message': 'kubelet has no disk pressure'},
        {'type': 'PIDPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientPID',
         'message': 'kubelet has sufficient PID available'},
        {'type': 'Ready', 'status': 'True', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-29T08:34:34Z', 'reason': 'KubeletReady',
         'message': 'kubelet is posting ready status. AppArmor enabled'}
    ]


@pytest.fixture
def node_not_ready():
    return [
        {'type': 'MemoryPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientMemory',
         'message': 'kubelet has sufficient memory available'},
        {'type': 'DiskPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasNoDiskPressure',
         'message': 'kubelet has no disk pressure'},
        {'type': 'PIDPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientPID',
         'message': 'kubelet has sufficient PID available'},
        {'type': 'Ready', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-29T08:34:34Z', 'reason': 'KubeletReady',
         'message': 'kubelet is posting ready status. AppArmor enabled'}
    ]


@pytest.fixture
def node_memory_pressure():
    return [
        {'type': 'MemoryPressure', 'status': 'True', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientMemory',
         'message': 'kubelet has sufficient memory available'},
        {'type': 'DiskPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasNoDiskPressure',
         'message': 'kubelet has no disk pressure'},
        {'type': 'PIDPressure', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-03T09:25:48Z', 'reason': 'KubeletHasSufficientPID',
         'message': 'kubelet has sufficient PID available'},
        {'type': 'Ready', 'status': 'False', 'lastHeartbeatTime': '2019-07-30T14:06:15Z',
         'lastTransitionTime': '2019-07-29T08:34:34Z', 'reason': 'KubeletReady',
         'message': 'kubelet is posting ready status. AppArmor enabled'}
    ]


@pytest.fixture
def node_base():
    return {'metadata': {'name': 'goris', 'selfLink': '/api/v1/nodes/goris', 'uid': '64d90ab1-5f4b-4fa2-8cf2-e733560f8d52',
                      'resourceVersion': '305709', 'creationTimestamp': '2019-07-03T09:25:48Z',
                      'labels': {'beta.kubernetes.io/arch': 'amd64', 'beta.kubernetes.io/os': 'linux',
                                 'kubernetes.io/arch': 'amd64', 'kubernetes.io/hostname': 'goris',
                                 'kubernetes.io/os': 'linux', 'microk8s.io/cluster': 'true'},
                      'annotations': {'node.alpha.kubernetes.io/ttl': '0',
                                      'volumes.kubernetes.io/controller-managed-attach-detach': 'true'}}, 'spec': {},
         'status': {
             'capacity': {'cpu': '8', 'ephemeral-storage': '489703416Ki', 'hugepages-1Gi': '0', 'hugepages-2Mi': '0',
                          'memory': '16181888Ki', 'pods': '110'},
             'allocatable': {'cpu': '8', 'ephemeral-storage': '488654840Ki', 'hugepages-1Gi': '0', 'hugepages-2Mi': '0',
                             'memory': '16079488Ki', 'pods': '110'}, 'conditions': [],
             'addresses': [{'type': 'InternalIP', 'address': '172.27.75.196'},
                           {'type': 'Hostname', 'address': 'goris'}],
             'daemonEndpoints': {'kubeletEndpoint': {'Port': 10250}},
             'nodeInfo': {'machineID': '991c63bd7f3a443fb923ba1b0fb0995f',
                          'systemUUID': '22c617cc-23e3-11b2-a85c-ee76da7e66ad',
                          'bootID': '90399b5a-ce60-4767-8655-56d1853e5c78', 'kernelVersion': '4.18.0-25-generic',
                          'osImage': 'Ubuntu 18.10', 'containerRuntimeVersion': 'containerd://1.2.5',
                          'kubeletVersion': 'v1.15.0', 'kubeProxyVersion': 'v1.15.0', 'operatingSystem': 'linux',
                          'architecture': 'amd64'}, 'images': [{'names': [
                 'k8s.gcr.io/heapster-grafana-amd64@sha256:4a472eb4df03f4f557d80e7c6b903d9c8fe31493108b99fbd6da6540b5448d70',
                 'k8s.gcr.io/heapster-grafana-amd64:v4.4.3'], 'sizeBytes': 51566280}, {'names': [
                 'k8s.gcr.io/kubernetes-dashboard-amd64@sha256:0ae6b69432e78069c5ce2bcde0fe409c5c4d6f0f4d9cd50a17974fea38898747',
                 'k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1'], 'sizeBytes': 44907311}, {'names': [
                 'k8s.gcr.io/heapster-amd64@sha256:59fb34ffd902282d06fcc940a906df9787edf78651743f4c8c4abf8b3468c0e9',
                 'k8s.gcr.io/heapster-amd64:v1.5.2'], 'sizeBytes': 20088732}, {'names': [
                 'docker.io/coredns/coredns@sha256:e83beb5e43f8513fa735e77ffc5859640baea30a882a11cc75c4c3244a737d3c',
                 'docker.io/coredns/coredns:1.5.0'], 'sizeBytes': 13341835}, {'names': [
                 'docker.io/cdkbot/addon-resizer-amd64@sha256:a5ff31fb60d32e02780441fc81bc91dd549097d6afeef3c6decb6005289795af',
                 'docker.io/cdkbot/addon-resizer-amd64:1.8.1'], 'sizeBytes': 8343051}, {'names': [
                 'k8s.gcr.io/heapster-influxdb-amd64@sha256:f433e331c1865ad87bc5387589965528b78cd6b1b2f61697e589584d690c1edd',
                 'k8s.gcr.io/heapster-influxdb-amd64:v1.3.3'], 'sizeBytes': 4748077}, {'names': [
                 'k8s.gcr.io/pause@sha256:f78411e19d84a252e53bff71a4407a5686c46983a2c2eeed83929b888179acea',
                 'k8s.gcr.io/pause:3.1'], 'sizeBytes': 317164}]}}


@pytest.fixture
def node_full(node_base, node_ready):
    node_base["status"]["conditions"] = node_ready
    return node_base
