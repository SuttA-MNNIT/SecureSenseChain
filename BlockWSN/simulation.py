# BlockWSN/simulation.py
"""
Core simulation logic for SecureSenseChain, PoW, and LEACH protocols.
"""

import numpy as np
import time
import networkx as nx
from . import config
from .energy_trust import compute_energy_tx, compute_energy_agg, update_trust
from .graph_utils import form_clusters
from .consensus import hdpoa_consensus

SimResults = tuple[list[float], list[float], list[float], list[float]]

def securesensechain(G: nx.Graph) -> SimResults:
    """Simulates the SecureSenseChain protocol."""
    energy_consumed, latencies, trust_accuracies, detection_rates = [], [], [], []
    total_malicious = sum(1 for n, d in G.nodes(data=True) if d.get('malicious', False))
    
    for r in range(config.MAX_ROUNDS):
        start_time = time.time()
        round_energy = 0
        correctly_detected = 0
        clusters = form_clusters(G)
        
        for gateway, sensors in clusters.items():
            if not sensors or G.nodes[gateway]["energy"] <= 0:
                continue

            agg_energy = compute_energy_agg(len(sensors))
            if G.nodes[gateway]["energy"] > agg_energy:
                G.nodes[gateway]["energy"] -= agg_energy
                round_energy += agg_energy

            for sensor in sensors:
                if G.nodes[sensor]["energy"] <= 0:
                    continue
                
                dist = np.linalg.norm(np.array(G.nodes[sensor]["pos"]) - np.array(G.nodes[gateway]["pos"]))
                tx_energy = compute_energy_tx(dist)
                if G.nodes[sensor]["energy"] > tx_energy:
                    G.nodes[sensor]["energy"] -= tx_energy
                    round_energy += tx_energy

                node_data = G.nodes[sensor]
                is_malicious = node_data["malicious"]
                behaves_maliciously = is_malicious and (np.random.rand() < config.MALICIOUS_BEHAVIOR_PROB)
                
                reputation = config.REPUTATION_PENALTY if behaves_maliciously else config.REPUTATION_REWARD
                node_data["trust"] = update_trust(node_data, reputation, node_data["trust"], r)
                
                if node_data["trust"] < config.TRUST_THRESHOLD and is_malicious:
                    correctly_detected += 1
        
        if r % 10 == 0:
            trusted_validators = hdpoa_consensus(G)
            for validator in trusted_validators:
                if G.nodes[validator]["energy"] > config.ENERGY_CONSENSUS_VALIDATOR:
                    G.nodes[validator]["energy"] -= config.ENERGY_CONSENSUS_VALIDATOR
                    round_energy += config.ENERGY_CONSENSUS_VALIDATOR

        latency = time.time() - start_time + 0.00085
        energy_consumed.append(round_energy)
        latencies.append(latency)
        non_malicious_trusts = [d["trust"] for n, d in G.nodes(data=True) if not d["malicious"] and n.startswith("S")]
        trust_accuracies.append(np.mean(non_malicious_trusts) if non_malicious_trusts else 0)
        detection_rates.append(correctly_detected / max(total_malicious, 1))
        
    return energy_consumed, latencies, trust_accuracies, detection_rates

def pow_simulation(G: nx.Graph) -> SimResults:
    """Simulates a simplified PoW baseline protocol."""
    energy_consumed, latencies = [], []
    
    for r in range(config.MAX_ROUNDS):
        start_time = time.time()
        round_energy = 0
        active_nodes = [n for n, d in G.nodes(data=True) if d["energy"] > 0]
        
        if not active_nodes:
            energy_consumed.append(0)
            latencies.append(time.time() - start_time + 0.05)
            continue
            
        num_miners = int(len(active_nodes) * config.POW_MINERS_RATIO)
        miners = np.random.choice(active_nodes, size=max(1, num_miners), replace=False)
        
        for node_id in miners:
            mining_energy = compute_energy_tx(config.AREA_SIZE / 2) * config.POW_ENERGY_INTENSITY_FACTOR
            if G.nodes[node_id]["energy"] > mining_energy:
                G.nodes[node_id]["energy"] -= mining_energy
                round_energy += mining_energy
        
        latency = time.time() - start_time + 0.05
        energy_consumed.append(round_energy)
        latencies.append(latency)

    return energy_consumed, latencies, [0] * config.MAX_ROUNDS, [0] * config.MAX_ROUNDS

def leach_simulation(G: nx.Graph) -> SimResults:
    """Simulates a LEACH protocol baseline with a simple trust model."""
    energy_consumed, latencies, trust_accuracies, detection_rates = [], [], [], []
    total_malicious = sum(1 for n, d in G.nodes(data=True) if d.get('malicious', False))

    for r in range(config.MAX_ROUNDS):
        start_time = time.time()
        round_energy = 0
        correctly_detected = 0
        clusters = form_clusters(G)
        
        for gateway, sensors in clusters.items():
            if not sensors or G.nodes[gateway]["energy"] <= 0:
                continue

            agg_energy = compute_energy_agg(len(sensors))
            if G.nodes[gateway]["energy"] > agg_energy:
                G.nodes[gateway]["energy"] -= agg_energy
                round_energy += agg_energy

            for sensor in sensors:
                if G.nodes[sensor]["energy"] <= 0:
                    continue
                
                dist = np.linalg.norm(np.array(G.nodes[sensor]["pos"]) - np.array(G.nodes[gateway]["pos"]))
                tx_energy = compute_energy_tx(dist)
                if G.nodes[sensor]["energy"] > tx_energy:
                    G.nodes[sensor]["energy"] -= tx_energy
                    round_energy += tx_energy

                node_data = G.nodes[sensor]
                is_malicious = node_data["malicious"]
                behaves_maliciously = is_malicious and (np.random.rand() < config.MALICIOUS_BEHAVIOR_PROB)
                reputation = 0.2 if behaves_maliciously else 0.8
                node_data["trust"] = 0.7 * node_data["trust"] + 0.3 * reputation
                
                if node_data["trust"] < 0.5 and is_malicious:
                    correctly_detected += 1
        
        latency = time.time() - start_time + 0.005
        energy_consumed.append(round_energy)
        latencies.append(latency)
        non_malicious_trusts = [d["trust"] for n, d in G.nodes(data=True) if not d["malicious"] and n.startswith("S")]
        trust_accuracies.append(np.mean(non_malicious_trusts) if non_malicious_trusts else 0)
        detection_rates.append(correctly_detected / max(total_malicious, 1))
        
    return energy_consumed, latencies, trust_accuracies, detection_rates