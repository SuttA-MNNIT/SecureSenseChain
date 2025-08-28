# BlockWSN/config.py
"""
Central configuration file for the SecureSenseChain simulation.

This file contains all the tunable parameters for the simulation, including
network topology, energy models, trust parameters, and output settings.
"""

import os

# --- Simulation Control ---
NUM_RUNS = 30           # Number of times to run the entire simulation for statistical averaging
MAX_ROUNDS = 100        # Number of rounds per simulation run

# --- Network Topology ---
NUM_SENSORS = 100       # Number of sensor nodes
NUM_GATEWAYS = 5        # Number of gateway nodes
AREA_SIZE = 100         # Dimensions of the simulation area (AREA_SIZE x AREA_SIZE)
COMMUNICATION_RANGE = 30 # Maximum distance for a direct edge between nodes

# --- Energy Model Parameters ---
E_ELEC = 50e-9          # Energy for electronics (Tx/Rx) in Joules/bit
E_AMP = 100e-12         # Energy for amplifier (Tx) in Joules/bit/m^2
E_DA = 5e-9             # Energy for data aggregation in Joules/bit
PACKET_SIZE = 4000      # Data packet size in bits
INITIAL_ENERGY_SENSOR = 0.5   # Initial energy for each sensor in Joules
INITIAL_ENERGY_GATEWAY = 2.0  # Initial energy for each gateway in Joules
ENERGY_CONSENSUS_VALIDATOR = 0.0001 # Energy for a validator to participate in one round of consensus

# --- Trust Model and Security Parameters ---
INITIAL_TRUST_SCORE = 0.5
TRUST_THRESHOLD = 0.6   # Threshold below which a node is considered malicious
MALICIOUS_PROB = 0.1    # Probability of a sensor node being malicious at initialization
MIN_MALICIOUS_NODES = 5 # Ensure at least this many malicious nodes exist
MALICIOUS_BEHAVIOR_PROB = 0.4 # Probability a malicious node acts maliciously in a given round

# --- Protocol-Specific Parameters ---
ALPHA_START = 0.8       # Initial weight for historical trust (high reliance on history)
ALPHA_END = 0.4         # Final weight for historical trust (high reliance on recent behavior)
REPUTATION_REWARD = 0.9
REPUTATION_PENALTY = 0.1
POW_MINERS_RATIO = 0.1  # Percentage of nodes actively mining in the PoW simulation
POW_ENERGY_INTENSITY_FACTOR = 50 # Multiplier for the high cost of a PoW operation

# --- Output Configuration ---
OUTPUT_DIR = "simulation_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)