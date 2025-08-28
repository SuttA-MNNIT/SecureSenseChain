# BlockWSN/visualization.py
"""
Functions for plotting simulation results and creating a summary table.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import logging

def plot_results(all_results: dict, output_dir: str) -> None:
    """
    Generates and saves a separate, high-quality PDF for each metric.

    Args:
        all_results (dict): A nested dictionary containing the results from all simulation runs.
        output_dir (str): The directory where the output plots will be saved.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    protocols = {
        'ssc': {'label': 'SecureSenseChain', 'color': 'blue', 'style': '-'},
        'pow': {'label': 'PoW', 'color': 'red', 'style': '--'},
        'leach': {'label': 'LEACH', 'color': 'green', 'style': '-.'}
    }
    
    metrics_to_plot = [
        {'title': 'Energy Consumption Comparison', 'ylabel': 'Energy (J)', 'metric': 'energy'},
        {'title': 'Transaction Latency Comparison', 'ylabel': 'Latency (s)', 'metric': 'latency'},
        {'title': 'Average Trust Score of Non-Malicious Nodes', 'ylabel': 'Trust Score', 'metric': 'trust'},
        {'title': 'Malicious Node Detection Rate', 'ylabel': 'Detection Rate', 'metric': 'detection'}
    ]
    
    for plot_info in metrics_to_plot:
        fig, ax = plt.subplots(figsize=(10, 7))
        metric = plot_info['metric']
        
        for proto_key, proto_info in protocols.items():
            if proto_key == 'pow' and metric in ['trust', 'detection']:
                continue

            data = np.array(all_results[proto_key][metric])
            mean = np.mean(data, axis=0)
            std = np.std(data, axis=0)
            
            ax.plot(mean, label=proto_info['label'], color=proto_info['color'], linestyle=proto_info['style'], linewidth=2.5)
            ax.fill_between(range(len(mean)), mean - std, mean + std, color=proto_info['color'], alpha=0.15)
        
        ax.set_title(plot_info['title'], fontsize=18, fontweight='bold')
        ax.set_xlabel("Round", fontsize=14)
        ax.set_ylabel(plot_info['ylabel'], fontsize=14)
        ax.legend(fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        if metric in ['trust', 'detection']:
            ax.set_ylim(0, 1.1)
        
        output_filename = f"{metric}_comparison.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        logging.info(f"High-quality plot saved to {output_path}")
        plt.close(fig)

def create_comparison_table(mean_results: dict, output_dir: str) -> None:
    """
    Creates and saves a CSV summary of the final averaged metrics.

    Args:
        mean_results (dict): A dictionary with the mean results for each protocol.
        output_dir (str): The directory where the output CSV will be saved.
    """
    metrics = {
        "Method": ["SecureSenseChain", "PoW", "LEACH"],
        "Avg Energy (J)": [
            np.mean(mean_results['ssc']['energy']),
            np.mean(mean_results['pow']['energy']),
            np.mean(mean_results['leach']['energy'])
        ],
        "Avg Latency (s)": [
            np.mean(mean_results['ssc']['latency']),
            np.mean(mean_results['pow']['latency']),
            np.mean(mean_results['leach']['latency'])
        ],
        "Avg Trust Accuracy": [np.mean(mean_results['ssc']['trust']), "N/A", np.mean(mean_results['leach']['trust'])],
        "Avg Detection Rate": [np.mean(mean_results['ssc']['detection']), "N/A", np.mean(mean_results['leach']['detection'])]
    }
    
    df = pd.DataFrame(metrics)
    
    for col in ["Avg Energy (J)", "Avg Latency (s)"]:
        df[col] = df[col].apply(lambda x: f"{x:.6f}" if isinstance(x, (int, float)) else x)
    for col in ["Avg Trust Accuracy", "Avg Detection Rate"]:
         df[col] = df[col].apply(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)

    logging.info("\n--- Simulation Results Summary ---")
    logging.info(df.to_string(index=False))
    
    table_path = os.path.join(output_dir, "simulation_results.csv")
    df.to_csv(table_path, index=False)
    logging.info(f"Comparison table saved to {table_path}")