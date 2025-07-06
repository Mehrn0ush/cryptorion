
# message_owner.py
# 
# ⚠️ IMPORTANT: This is a "blinded signing" demonstration, NOT a true blind signature scheme.
# 
# What this demonstrates:
# - Hiding a message from the signer during signing
# - Private verification using a secret blinding factor
# 
# What this does NOT provide:
# - Public verifiability (requires secret blinding factor)
# - True unlinkability (signer could link if blinding factor is revealed)
# - Mathematical unblinding transformation
#
# For true blind signatures, consider RSA-based schemes or research-level lattice approaches.

import random
import json
from Crypto.Hash import SHA256
from dilithium import Dilithium

class MessageOwner:
    def __init__(self, signer_public_key):
        self.signer_public_key = signer_public_key
        # Use the same parameter set as the signer
        from signer import DILITHIUM_PARAMS
        self.dilithium = Dilithium(parameter_set=DILITHIUM_PARAMS)

    def blind_message(self, message, r=None):
        """
        Create a blinded message by concatenating hash(message) with blinding factor r.
        
        LIMITATION: This is a simple concatenation approach, not a mathematical blinding.
        In true blind signatures, blinding would involve mathematical transformations.
        """
        if isinstance(message, str):
            message = message.encode()
        
        h = SHA256.new(message)
        m = h.digest()
        
        if r is None:
            r = random.randbytes(32)  # 256-bit random blinding factor
        
        # Simple concatenation - NOT a proper mathematical blinding
        blinded = m + r  # Concatenate hash with blinding factor
        
        return {
            'blinded_msg': blinded.hex(),
            'r': r.hex(),
            'original_message': message.hex(),
            'message_hash': m.hex()
        }

    def unblind_signature(self, blinded_signature, r):
        """
        LIMITATION: This does NOT perform mathematical unblinding.
        In true blind signatures, this would transform the signature mathematically.
        Here, we just return the signature as-is.
        """
        # No mathematical transformation - this is the key limitation
        return blinded_signature

    def verify_blind_signature(self, original_message, signature, r):
        """
        Private verification - requires the secret blinding factor r.
        
        LIMITATION: This is NOT public verification. A true blind signature
        would be verifiable by anyone using only the public key and original message.
        """
        if isinstance(original_message, str):
            original_message = original_message.encode()
        if isinstance(r, str):
            r = bytes.fromhex(r)
        if isinstance(signature, str):
            signature = bytes.fromhex(signature)
        
        # Reconstruct the blinded message (requires secret r)
        h = SHA256.new(original_message)
        m = h.digest()
        blinded_message = m + r
        
        # Verify against the blinded message, not the original
        try:
            return self.dilithium.verify(self.signer_public_key, blinded_message, signature)
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    def verify(self, message, signature):
        """
        Standard verification - will fail for our "blind" signatures
        because they're actually signatures on the blinded message.
        """
        if isinstance(message, str):
            message = message.encode()
        
        try:
            return self.dilithium.verify(self.signer_public_key, message, signature)
        except Exception as e:
            print(f"Verification error: {e}")
            return False

def run_message_owner_phase1():
    # Load the signer's public key (should be provided by the signer)
    try:
        with open('signer_public_key.json', 'r') as f:
            key_data = json.load(f)
            public_key = key_data['public_key']
    except FileNotFoundError:
        print("Error: signer_public_key.json not found!")
        print("Please run 'python signer.py setup' first to generate signer keys.")
        return
    
    owner = MessageOwner(public_key)
    original_message = "This is my secret vote: Candidate A"
    
    print("\n=== Message Owner Phase 1: Create Blinded Message ===")
    print(f"Original message: {original_message}")
    
    # Create blinded message
    blind_data = owner.blind_message(original_message)
    
    print("\nBlinding complete. Results:")
    print(f"Blinded message: {blind_data['blinded_msg']}")
    print(f"Blinding factor r: {blind_data['r']} (secret)")
    print(f"Original message: {blind_data['original_message']} (for reference)")
    
    # Save to file to pass to signer
    with open('blind_data.json', 'w') as f:
        json.dump({
            'blinded_msg': blind_data['blinded_msg'],
            'public_key': public_key,
            '_secret_r': blind_data['r'],
            '_original_message': blind_data['original_message']
        }, f)
    
    print("\nSaved blind_data.json for signer to process")
    print("Note: The blinding factor r is stored locally for phase 2")

def run_message_owner_phase2():
    # Load original blind data
    with open('blind_data.json', 'r') as f:
        blind_data = json.load(f)
        r = bytes.fromhex(blind_data['_secret_r'])
        public_key = bytes.fromhex(blind_data['public_key'])
        original_message_hex = blind_data['_original_message']
    
    # Load the signature from signer
    with open('blind_signature.json', 'r') as f:
        signature_data = json.load(f)
        blind_signature = bytes.fromhex(signature_data['blind_signature'])
    
    owner = MessageOwner(public_key)
    
    print("\n=== Message Owner Phase 2: Unblind Signature ===")
    print(f"Received blind signature: {blind_signature.hex()}")
    
    # Unblind the signature
    final_signature = owner.unblind_signature(blind_signature, r)
    print(f"\nFinal signature: {final_signature.hex()}")
    
    # Verification
    original_message = bytes.fromhex(original_message_hex)
    is_valid = owner.verify_blind_signature(original_message, final_signature, r)
    print("\nValidation results:")
    print(f"Signature is valid: {is_valid}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "phase2":
        run_message_owner_phase2()
    else:
        run_message_owner_phase1()