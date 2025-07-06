import json
from Crypto.Util.number import getPrime, inverse

def generate_rsa_keys(key_size=1024):
    e = 65537
    p = getPrime(key_size // 2)
    q = getPrime(key_size // 2)
    N = p * q
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    return (e, N), (d, N)

class Signer:
    def __init__(self, private_key):
        self.d, self.N = private_key

    def sign_blinded(self, blinded_message):
        return pow(blinded_message, self.d, self.N)

def run_signer():
    print("\n=== Signer Process ===")
    
    # Load the private key (in real world, signer would have its own persistent key)
    with open('signer_private_key.json', 'r') as f:
        key_data = json.load(f)
        private_key = key_data['private_key']
    
    print("Using RSA keys:")
    print(f"Public key (e, N): ({private_key[0]}, {private_key[1]})")
    print(f"Private key (d, N): (hidden)")
    
    # Load the blinded message from file
    with open('blind_data.json', 'r') as f:
        data = json.load(f)
        blinded_msg = data['blinded_msg']
    
    print(f"\nReceived blinded message: {blinded_msg}")
    
    # Sign the blinded message
    signer = Signer(private_key)
    blind_signature = signer.sign_blinded(blinded_msg)
    print(f"\nCreated blind signature: {blind_signature}")
    
    # Save the blind signature
    with open('blind_signature.json', 'w') as f:
        json.dump({'blind_signature': blind_signature}, f)
    
    print("\nSaved blind_signature.json for message owner to process")
if __name__ == "__main__":
    run_signer()