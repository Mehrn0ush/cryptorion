import random
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256

class MessageOwner:
    def __init__(self, signer_public_key):
        self.e, self.N = signer_public_key

    def blind_message(self, message, r=None):
        if isinstance(message, str):
            message = message.encode()
        
        h = SHA256.new(message)
        m = bytes_to_long(h.digest())
        
        if r is None:
            while True:
                r = random.randint(2, self.N - 1)
                if self._gcd(r, self.N) == 1:
                    break
        
        blinded = (m * pow(r, self.e, self.N)) % self.N
        return {
            'blinded_msg': blinded,
            'r': r,
            'original_hash': m
        }

    def unblind_signature(self, blinded_signature, r):
        r_inv = self._modinv(r, self.N)
        return (blinded_signature * r_inv) % self.N

    def verify(self, message, signature):
        if isinstance(message, str):
            message = message.encode()
        
        h = SHA256.new(message)
        m = bytes_to_long(h.digest())
        return pow(signature, self.e, self.N) == m % self.N

    @staticmethod
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def _modinv(a, m):
        g, x, y = MessageOwner._egcd(a, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist")
        return x % m

    @staticmethod
    def _egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = MessageOwner._egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def run_message_owner_phase1():
    # Generate keys once and reuse them
    from signer import generate_rsa_keys
    public_key, private_key = generate_rsa_keys()
    
    owner = MessageOwner(public_key)
    original_message = "This is my secret vote: Candidate A"
    
    print("\n=== Message Owner Phase 1: Create Blinded Message ===")
    print(f"Original message: {original_message}")
    
    # Create blinded message
    blind_data = owner.blind_message(original_message)
    
    print("\nBlinding complete. Results:")
    print(f"Blinded message: {blind_data['blinded_msg']}")
    print(f"Blinding factor r: {blind_data['r']} (secret)")
    print(f"Original hash: {blind_data['original_hash']} (for reference)")
    
    # Save to file to pass to signer
    with open('blind_data.json', 'w') as f:
        json.dump({
            'blinded_msg': blind_data['blinded_msg'],
            'public_key': public_key,
            '_secret_r': blind_data['r'],
            '_original_hash': blind_data['original_hash']
        }, f)
    
    # Also save the private key for the signer to use (in real world, signer would have its own key)
    with open('signer_private_key.json', 'w') as f:
        json.dump({'private_key': private_key}, f)
    
    print("\nSaved blind_data.json for signer to process")
    print("Note: The blinding factor r is stored locally for phase 2")

def run_message_owner_phase2():
    # Load our original blind data
    with open('blind_data.json', 'r') as f:
        blind_data = json.load(f)
        r = blind_data['_secret_r']
        public_key = blind_data['public_key']
    
    # Load the signature from signer
    with open('blind_signature.json', 'r') as f:
        signature_data = json.load(f)
        blind_signature = signature_data['blind_signature']
    
    owner = MessageOwner(public_key)
    
    print("\n=== Message Owner Phase 2: Unblind Signature ===")
    print(f"Received blind signature: {blind_signature}")
    
    # Unblind the signature
    final_signature = owner.unblind_signature(blind_signature, r)
    print(f"\nUnblinded signature: {final_signature}")
    
    # Verification
    original_message = "This is my secret vote: Candidate A"
    is_valid = owner.verify(original_message, final_signature)
    print("\nVerification results:")
    print(f"Signature is valid: {is_valid}")
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "phase2":
        run_message_owner_phase2()
    else:
        run_message_owner_phase1()