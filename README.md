# QBER Simulation and Encryption

This project simulates a Quantum Key Distribution (QKD) using Qiskit, calculates the Quantum Bit Error Rate (QBER) over different noise levels, and uses the generated key to robustly encrypt and decrypt video files.

## Installation

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/MacOS:
   source venv/bin/activate
   ```
2. Install the required dependencies:
   ```bash
   pip install qiskit qiskit-aer numpy matplotlib cryptography
   ```

## Usage

1. Create a folder named `input_videos` (if it does not exist) and place your `.mp4`, `.avi`, or `.mov` files inside.
2. Run the main script:
   ```bash
   python main.py
   ```

The script will:
1. Simulate a quantum channel and calculate QBER, creating a `noise_correlation_graph.png` chart.
2. Generate a secure key simulating the quantum-secured password.
3. Automatically encrypt all video files in `input_videos/` and save them to `encrypted_videos/`.
4. Decrypt those files back to normal in `decrypted_videos/` to prove the pipeline works.
