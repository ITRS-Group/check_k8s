from .pod import check_pods
from .deployment import check_deployments
from .node import check_nodes


# Purpose
# -------
# 1) Provide enum for Argparse "Resource choices"
# 2) Resolve how to obtain and process health data

MAPPINGS = dict(
    # resource_name, (check_func, is_core)
    pods=(check_pods, True),
    nodes=(check_nodes, True),
    deployments=(check_deployments, False),
)
