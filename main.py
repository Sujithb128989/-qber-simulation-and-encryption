import os
import glob
import base64
import secrets
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from cryptography.fernet import Fernet

def simulate_quantum_channel(noise_probability):
    # Create a basic quantum circuit with 1 qubit
    qc = QuantumCircuit(1, 1)
    qc.x(0) # Prepare the qubit in the '1' state
    
    # Inject physical noise to simulate a real-world quantum channel
    noise_model = NoiseModel()
    if noise_probability > 0:
        error = depolarizing_error(noise_probability, 1)
        noise_model.add_all_qubit_quantum_error(error, ['x', 'id'])
    
    # Measure the qubit
    qc.measure(0, 0) 
    
    # Run the simulation 1000 times to get an average
    simulator = AerSimulator(noise_model=noise_model)
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1000).result()
    
    # Calculate the Quantum Bit Error Rate (QBER)
    counts = result.get_counts()
    errors = counts.get('0', 0) # If we sent a '1', any '0' measured is an error
    return errors / 1000.0

def generate_graph_and_key():
    print("[*] Simulating Quantum Channel and generating QBER graph...")
    
    # Test noise levels from 0% up to 25%
    noise_levels = np.linspace(0, 0.25, 10)
    qber_results = [simulate_quantum_channel(p) for p in noise_levels]

    # Plot the results and save the chart for the assignment
    plt.figure(figsize=(8, 5))
    plt.plot(noise_levels * 100, np.array(qber_results) * 100, marker='o', color='red', linestyle='dashed')
    plt.title('Quantum Bit Error Rate (QBER) vs Physical Channel Noise')
    plt.xlabel('Simulated Channel Noise (%)')
    plt.ylabel('QBER (%)')
    plt.axhline(y=11, color='black', linestyle='-', label='11% Security Threshold')
    plt.legend()
    plt.grid(True)
    plt.savefig('noise_correlation_graph.png')
    print("[+] Graph saved successfully as 'noise_correlation_graph.png'.")

    # Generate a standard AES key to simulate the final quantum-secured password
    raw_key = secrets.token_hex(32)
    fernet_key = base64.urlsafe_b64encode(bytes.fromhex(raw_key))
    print("[+] Quantum-safe key generated for video encryption.")
    return fernet_key

def process_videos(input_dir, key):
    # Setup output folders
    enc_dir = "encrypted_videos"
    dec_dir = "decrypted_videos"
    os.makedirs(enc_dir, exist_ok=True)
    os.makedirs(dec_dir, exist_ok=True)

    # Search the folder for common video formats automatically
    video_files = []
    for ext in ('*.mp4', '*.avi', '*.mov'):
        video_files.extend(glob.glob(os.path.join(input_dir, ext)))

    if not video_files:
        print(f"[!] Error: No video files (.mp4, .avi, .mov) found in '{input_dir}'.")
        return

    # Initialize the encryption tool using the generated key
    f = Fernet(key)
    print(f"\n[*] Found {len(video_files)} video(s). Starting batch encryption and decryption...")

    for file_path in video_files:
        filename = os.path.basename(file_path)
        enc_path = os.path.join(enc_dir, filename + ".enc")
        dec_path = os.path.join(dec_dir, "UNLOCKED_" + filename)
        
        try:
            # 1. Read and encrypt the original video file
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)
            
            # 2. Save the scrambled data as a .enc file
            with open(enc_path, 'wb') as file:
                file.write(encrypted_data)
                
            # 3. Read the encrypted file and decrypt it back to normal
            with open(enc_path, 'rb') as file:
                locked_data = file.read()
            decrypted_data = f.decrypt(locked_data)
            
            # 4. Save the playable video to prove the pipeline works
            with open(dec_path, 'wb') as file:
                file.write(decrypted_data)
                
            print(f"  -> Successfully processed: {filename}")
        except Exception as e:
            print(f"  [!] Failed to process {filename}: {e}")

    print("\n[+] Batch processing complete. Check 'encrypted_videos' and 'decrypted_videos' folders.")

if __name__ == "__main__":
    input_folder = "input_videos"
    
    # Make sure the input folder exists before running the main logic
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"[!] Created '{input_folder}' folder. Please place your videos inside and run the script again.")
    else:
        # Run the full pipeline
        generated_key = generate_graph_and_key()
        process_videos(input_folder, generated_key)