# BlockWSN/graph_utils.py
"""
Utility functions for creating and managing the network graph.
"""

import networkx as nx
import random
from scipy.spatial import distance
from . import config

def initialize_graph(seed: int) -> nx.Graph:
    """
    Initializes the network graph with sensor and gateway nodes.

    Args:
        seed (int): The random seed for reproducibility.

    Returns:
        nx.Graph: A NetworkX graph object representing the WSN.
    """
    random.seed(seed)
    G = nx.Graph()

    # Create sensor nodes
    sensor_nodes = []
    malicious_indices = set()
    for i in range(config.NUM_SENSORS):
        is_malicious = random.random() < config.MALICIOUS_PROB
        if is_malicious:
            malicious_indices.add(i)
        sensor_nodes.append(
            (f"S{i}", {
                "pos": (random.uniform(0, config.AREA_SIZE), random.uniform(0, config.AREA_SIZE)),
                "energy": config.INITIAL_ENERGY_SENSOR,
                "trust": config.INITIAL_TRUST_SCORE,
                "malicious": is_malicious
            })
        )

    # Ensure the minimum number of malicious nodes
    while len(malicious_indices) < config.MIN_MALICIOUS_NODES:
        i = random.randint(0, config.NUM_SENSORS - 1)
        if i not in malicious_indices:
            sensor_nodes[i][1]["malicious"] = True
            malicious_indices.add(i)

    # Create gateway nodes
    gateway_nodes = [
        (f"G{i}", {
            "pos": (random.uniform(0, config.AREA_SIZE), random.uniform(0, config.AREA_SIZE)),
            "energy": config.INITIAL_ENERGY_GATEWAY,
            "trust": 0.9,
            "malicious": False
        }) for i in range(config.NUM_GATEWAYS)
    ]
    G.add_nodes_from(sensor_nodes + gateway_nodes)

    # Add edges based on communication range
    for n1, d1 in G.nodes(data=True):
        for n2, d2 in G.nodes(data=True):
            if n1 != n2:
                dist = distance.euclidean(d1["pos"], d2["pos"])
                if dist <= config.COMMUNICATION_RANGE:
                    G.add_edge(n1, n2, weight=dist)
    return G

def form_clusters(G: nx.Graph) -> dict:
    """
    Forms clusters by assigning each active sensor to the nearest active gateway.

    Args:
        G (nx.Graph): The current network graph.

    Returns:
        dict: A dictionary where keys are gateway IDs and values are lists of sensor IDs.
    """
    clusters = {f"G{i}": [] for i in range(config.NUM_GATEWAYS)}
    active_sensors = [n for n, d in G.nodes(data=True) if n.startswith("S") and d["energy"] > 0]
    active_gateways = [n for n, d in G.nodes(data=True) if n.startswith("G") and d["energy"] > 0]

    if not active_gateways:
        return clusters

    for sensor in active_sensors:
        distances = {gw: distance.euclidean(G.nodes[sensor]["pos"], G.nodes[gw]["pos"]) for gw in active_gateways}
        closest_gateway = min(distances, key=distances.get)
        clusters[closest_gateway].append(sensor)
            
    return clusters