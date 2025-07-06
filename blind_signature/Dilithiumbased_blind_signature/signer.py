# signer.py

import json
import os
from dilithium import Dilithium

# Complete parameter set for Dilithium2 - using correct parameter names
DILITHIUM_PARAMS = {
    "n": 256,
    "q": 8380417,
    "k": 4,
    "l": 4,
    "eta": 2,
    "tau": 39,
    "gamma_1": 1 << 17,  # Fixed: gamma1 -> gamma_1
    "gamma_2": (8380417-1)//88,  # Fixed: gamma2 -> gamma_2
    "d": 13,
    "omega": 80,
    "eta_bound": 15  # Fixed: using correct value from DEFAULT_PARAMETERS
}

def generate_dilithium_keys():
    # Generate Dilithium key pair with default parameters
    dilithium = Dilithium(parameter_set=DILITHIUM_PARAMS)
    # Generate a random key seed
    key_seed = os.urandom(32)  # 256-bit random seed
    pk, sk = dilithium.keygen(key_seed)
    return pk, sk

def setup_signer_keys():
    """Generate and save signer keys - this should be run once by the signer"""
    print("=== Generating Signer Keys ===")
    pk, sk = generate_dilithium_keys()
    
    # Save keys
    with open('signer_public_key.json', 'w') as f:
        json.dump({'public_key': pk.hex()}, f)
    
    with open('signer_private_key.json', 'w') as f:
        json.dump({'private_key': sk.hex()}, f)
    
    print(f"Public key: {pk.hex()}")
    print("Keys saved to signer_public_key.json and signer_private_key.json")
    return pk, sk

class Signer:
    def __init__(self, private_key):
        self.private_key = private_key
        self.dilithium = Dilithium(parameter_set=DILITHIUM_PARAMS)

    def sign_blinded(self, blinded_message):
        # Convert hex string back to bytes if needed
        if isinstance(blinded_message, str):
            blinded_message = bytes.fromhex(blinded_message)
        
        # Sign the blinded message using sign_with_input
        signature = self.dilithium.sign_with_input(self.private_key, blinded_message)
        return signature

def run_signer():
    print("\n=== Signer Process ===")
    
    # Load the private key
    with open('signer_private_key.json', 'r') as f:
        key_data = json.load(f)
        private_key = bytes.fromhex(key_data['private_key'])
    
    print("Using Dilithium keys")
    
    # Load the blinded message from file
    with open('blind_data.json', 'r') as f:
        data = json.load(f)
        blinded_msg = data['blinded_msg']
    
    print(f"\nReceived blinded message: {blinded_msg}")
    
    # Sign the blinded message
    signer = Signer(private_key)
    blind_signature = signer.sign_blinded(blinded_msg)
    print(f"\nCreated blind signature: {blind_signature.hex()}")
    
    # Save the blind signature
    with open('blind_signature.json', 'w') as f:
        json.dump({'blind_signature': blind_signature.hex()}, f)
    
    print("\nSaved blind_signature.json for message owner to process")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_signer_keys()
    else:
        run_signer()