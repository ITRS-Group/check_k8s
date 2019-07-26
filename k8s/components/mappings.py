from .pod import check_pods
from .deployment import check_deployments
from .node import check_nodes


# Purpose
# -------
# 1) Provides an enum for Argparse "Resource choices".
# 2) Resolves how to obtain health data and how to process it.

MAPPINGS = dict(
    # resource_name, (check_func, is_core)
    pods=(check_pods, True),
    nodes=(check_nodes, True),
    deployments=(check_deployments, False)
)
