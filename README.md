# SecureSenseChain Simulation

This repository contains the Python simulation code for the research paper, "SecureSenseChain: A Dynamic Trust-Aware Blockchain Framework for Energy-Efficient IoT Sensor Networks".

The simulation models and evaluates the performance of the proposed SecureSenseChain framework against two baseline protocols: a simplified Proof-of-Work (PoW) and a LEACH-like clustering protocol.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SuttA-MNNIT/SecureSenseChain.git
    cd SecureSenseChain
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

To run the complete simulation (including all 30 runs, averaging, and generating outputs), execute the `main` module from the top-level project directory:

```bash
python -m BlockWSN.main
Output
The script will produce the following outputs in the simulation_results/ directory:
energy_comparison.pdf: A plot of energy consumption per round.
latency_comparison.pdf: A plot of latency per round.
trust_comparison.pdf: A plot of the average trust score of non-malicious nodes.
detection_comparison.pdf: A plot of the malicious node detection rate.
simulation_results.csv: A CSV file with the final, averaged performance metrics.
The console will display progress bars and a summary of the final results upon completion.
