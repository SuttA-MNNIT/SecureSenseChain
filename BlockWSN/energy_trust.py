# BlockWSN/energy_trust.py
"""
Functions for calculating energy consumption and updating trust scores.
"""

from . import config

def compute_energy_tx(dist: float) -> float:
    """Calculates the energy to transmit a packet over a given distance."""
    return config.E_ELEC * config.PACKET_SIZE + config.E_AMP * config.PACKET_SIZE * (dist**2)

def compute_energy_agg(num_packets: int) -> float:
    """Calculates the energy to aggregate data from multiple packets."""
    return num_packets * config.E_DA * config.PACKET_SIZE

def update_trust(node_data: dict, reputation: float, current_trust: float, current_round: int) -> float:
    """
    Updates a node's trust score based on behavior using a dynamic weighting factor.

    Args:
        node_data (dict): The dictionary of attributes for the node.
        reputation (float): The reputation score from the current round's interaction.
        current_trust (float): The node's trust score from the previous round.
        current_round (int): The current simulation round, used for dynamic alpha.

    Returns:
        float: The updated trust score, bounded between 0.0 and 1.0.
    """
    progress = current_round / config.MAX_ROUNDS
    alpha = config.ALPHA_START - (config.ALPHA_START - config.ALPHA_END) * progress
    trust = alpha * current_trust + (1 - alpha) * reputation
    
    if node_data["malicious"]:
        trust *= 0.8
    elif not node_data["malicious"] and node_data["energy"] > 0.1:
        trust = min(0.99, trust + 0.02)

    return max(0.0, min(1.0, trust))