# BlockWSN/consensus.py
"""
Implements the HDPoA consensus mechanism.
"""

import networkx as nx
from . import config

def hdpoa_consensus(G: nx.Graph) -> list[str]:
    """
    Performs the Hybrid Dynamic Proof-of-Authority consensus.
    
    Selects gateway nodes as validators only if their trust score meets
    or exceeds the defined TRUST_THRESHOLD.
    
    Args:
        G (nx.Graph): The current state of the network graph.

    Returns:
        list[str]: A list of trusted gateway node IDs eligible to validate a block.
    """
    trusted_validators = []
    for i in range(config.NUM_GATEWAYS):
        gateway_id = f"G{i}"
        if G.has_node(gateway_id):
            node_data = G.nodes[gateway_id]
            if node_data["energy"] > 0 and node_data["trust"] >= config.TRUST_THRESHOLD:
                trusted_validators.append(gateway_id)
                
    return trusted_validators