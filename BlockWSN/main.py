# BlockWSN/main.py
"""
Main entry point for the SecureSenseChain simulation.

This script orchestrates the entire simulation process:
1. Initializes the network graph.
2. Runs simulations for SecureSenseChain, PoW, and LEACH protocols over multiple runs.
3. Aggregates the results for statistical analysis.
4. Generates output plots and a summary CSV file.
"""

import logging
import numpy as np
from tqdm import tqdm
from . import config
from .graph_utils import initialize_graph
from .simulation import securesensechain, pow_simulation, leach_simulation
from .visualization import plot_results, create_comparison_table

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def run_all_simulations() -> None:
    """
    Runs all simulation protocols, aggregates results, and generates outputs.
    """
    all_results = {
        'ssc': {'energy': [], 'latency': [], 'trust': [], 'detection': []},
        'pow': {'energy': [], 'latency': [], 'trust': [], 'detection': []},
        'leach': {'energy': [], 'latency': [], 'trust': [], 'detection': []},
    }

    for run in tqdm(range(config.NUM_RUNS), desc="Overall Simulation Progress"):
        logging.info(f"--- Starting Run {run + 1}/{config.NUM_RUNS} ---")
        G = initialize_graph(seed=run)
        
        logging.info("Running SecureSenseChain...")
        ssc_e, ssc_l, ssc_t, ssc_d = securesensechain(G.copy())
        all_results['ssc']['energy'].append(ssc_e)
        all_results['ssc']['latency'].append(ssc_l)
        all_results['ssc']['trust'].append(ssc_t)
        all_results['ssc']['detection'].append(ssc_d)
        
        logging.info("Running PoW Baseline...")
        pow_e, pow_l, pow_t, pow_d = pow_simulation(G.copy())
        all_results['pow']['energy'].append(pow_e)
        all_results['pow']['latency'].append(pow_l)
        
        logging.info("Running LEACH Baseline...")
        leach_e, leach_l, leach_t, leach_d = leach_simulation(G.copy())
        all_results['leach']['energy'].append(leach_e)
        all_results['leach']['latency'].append(leach_l)
        all_results['leach']['trust'].append(leach_t)
        all_results['leach']['detection'].append(leach_d)

    logging.info("--- Aggregating Results ---")
    mean_results = {}
    for protocol, metrics in all_results.items():
        mean_results[protocol] = {}
        for metric, data in metrics.items():
            mean_results[protocol][metric] = np.mean(data, axis=0)

    plot_results(all_results, config.OUTPUT_DIR)
    create_comparison_table(mean_results, config.OUTPUT_DIR)
    
    logging.info("--- Simulation Complete ---")

if __name__ == '__main__':
    run_all_simulations()