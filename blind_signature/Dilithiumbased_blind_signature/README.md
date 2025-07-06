# Dilithium-Based Blinded Signing Demonstration

## 📖 Overview

This project demonstrates a **blinded signing** process using the Dilithium post-quantum signature scheme. It shows how to hide a message from a signer during the signing process, providing educational insights into privacy-preserving cryptographic concepts.

## ⚠️ Important Disclaimer

**This is NOT a true blind signature scheme.** This implementation demonstrates **blinded signing** rather than cryptographic blind signatures. It shows how to hide a message from a signer during signing, but does not achieve the full properties of cryptographic blind signatures.

### What This Demonstrates ✅
- **Message Hiding**: The signer cannot see the original message during signing
- **Private Verification**: The message owner can verify the signature using their secret blinding factor
- **Cryptographic Security**: Uses Dilithium, a post-quantum secure signature scheme
- **Educational Value**: Understanding message blinding concepts and Dilithium usage

### What This Does NOT Provide ❌
- **Public Verifiability**: The signature cannot be verified by third parties without the secret blinding factor
- **Proper Unblinding**: No mathematical transformation from blinded to unblinded signature
- **True Unlinkability**: The signer could potentially link signatures if the blinding factor is revealed
- **Standard Blind Signature Properties**: This is not suitable for applications requiring true blind signatures

## 🔧 Technical Implementation

### Architecture
```
Message Owner                    Signer
     |                             |
     | 1. Generate Keys            |
     |<----------------------------|
     |                             |
     | 2. Blind Message            |
     |---------------------------->|
     |                             |
     | 3. Sign Blinded Message     |
     |<----------------------------|
     |                             |
     | 4. Unblind & Verify         |
     | (Private Verification)      |
```

### Blinding Process
```python
# Original message: "This is my secret vote: Candidate A"
# Message hash: SHA256(message)
# Blinding factor: random 256-bit value
# Blinded message: hash(message) || blinding_factor
```

### Key Components

#### 1. **Message Owner** (`message_owner.py`)
- Generates blinding factors
- Creates blinded messages
- Performs private verification
- Manages the complete blinded signing workflow

#### 2. **Signer** (`signer.py`)
- Generates Dilithium key pairs
- Signs blinded messages without seeing original content
- Provides public key for verification

#### 3. **Dilithium Integration**
- Uses Dilithium2 parameter set
- Post-quantum secure signature scheme
- Lattice-based cryptography

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.9+ (for random.randbytes)
python --version

# Required packages
pip install dilithium pycryptodome
```

### Step-by-Step Execution

#### 1. Generate Signer Keys
```bash
python signer.py setup
```
**Output**: Creates `signer_public_key.json` and `signer_private_key.json`

#### 2. Create Blinded Message
```bash
python message_owner.py
```
**Output**: Creates `blind_data.json` with blinded message

#### 3. Sign the Blinded Message
```bash
python signer.py
```
**Output**: Creates `blind_signature.json` with signature

#### 4. Unblind and Verify
```bash
python message_owner.py phase2
```
**Output**: Private verification result

## 📁 File Structure

```
Dilithiumbased_blind_signature/
├── message_owner.py          # Message owner implementation
├── signer.py                 # Signer implementation
├── README.md                 # This file
├── signer_public_key.json    # Generated public key
├── signer_private_key.json   # Generated private key (keep secret!)
├── blind_data.json          # Blinded message data
└── blind_signature.json     # Signature on blinded message
```

## 🔍 Code Walkthrough

### Key Functions

#### Message Blinding
```python
def blind_message(self, message, r=None):
    """
    Create blinded message by concatenating hash(message) with blinding factor.
    LIMITATION: Simple concatenation, not mathematical blinding.
    """
    h = SHA256.new(message)
    m = h.digest()
    blinded = m + r  # Concatenation approach
    return {'blinded_msg': blinded.hex(), 'r': r.hex()}
```

#### Private Verification
```python
def verify_blind_signature(self, original_message, signature, r):
    """
    Private verification - requires secret blinding factor r.
    LIMITATION: Not publicly verifiable.
    """
    # Reconstruct blinded message (requires secret r)
    blinded_message = hash(original_message) + r
    return verify(public_key, blinded_message, signature)
```

## 🛡️ Security Analysis

### What's Secure
- **Dilithium Signatures**: Post-quantum secure
- **Message Hiding**: Signer cannot see original message
- **Cryptographic Randomness**: Proper blinding factor generation

### Limitations
- **No Public Verification**: Requires secret blinding factor
- **No Unlinkability**: Signer could link if blinding factor revealed
- **No Mathematical Unblinding**: No transformation to original message signature

### Why These Limitations Exist
1. **Dilithium Design**: Lattice-based signatures lack multiplicative properties needed for blind signatures
2. **No Unblinding Transformation**: Unlike RSA, no mathematical way to transform signature
3. **Research Area**: Post-quantum blind signatures are still being researched

## 🎯 Use Cases

### Suitable For
- **Educational purposes**: Learning message blinding concepts
- **Private verification scenarios**: Where only message owner needs to verify
- **Dilithium learning**: Understanding post-quantum signature usage
- **Research demonstrations**: Showing limitations of current approaches

### Not Suitable For
- **Anonymous voting systems**: Requires public verification
- **Digital cash**: Needs unlinkability
- **Publicly verifiable credentials**: Requires public verification
- **Production systems**: Missing key blind signature properties

## 🔬 Technical Details

### Dilithium Parameters
```python
DILITHIUM_PARAMS = {
    "n": 256,           # Polynomial degree
    "q": 8380417,       # Modulus
    "k": 4, "l": 4,     # Matrix dimensions
    "eta": 2,           # Noise parameter
    "tau": 39,          # Hamming weight
    "gamma_1": 1 << 17, # Norm bound
    "gamma_2": (8380417-1)//88,  # Norm bound
    "d": 13,            # Binary expansion
    "omega": 80,        # Hamming weight
    "eta_bound": 15     # Noise bound
}
```

### Error Handling
The implementation includes proper error handling for:
- Missing key files
- Invalid signatures
- File I/O errors
- Cryptographic verification failures

## 🚨 Known Issues

### AES256 CTR DRBG Warning
```
Error importing AES256 CTR DRBG. Have you tried installing requirements?
ImportError: No module named 'aes256_ctr_drbg'
Dilithium will work perfectly fine with system randomness
```
**Status**: Harmless warning - Dilithium falls back to system randomness

### Overflow Warning
```
RuntimeWarning: overflow encountered in scalar multiply
```
**Status**: Minor warning in random number generation, doesn't affect functionality

## 🔮 Future Improvements

### Research Directions
1. **True Lattice Blind Signatures**: Implement research-level lattice-based blind signatures
2. **Zero-Knowledge Proofs**: Alternative privacy-preserving approaches
3. **Hybrid Schemes**: Combine classical and post-quantum techniques

### Code Enhancements
1. **Better Error Messages**: More descriptive error handling
2. **Configuration Options**: Parameter customization
3. **Testing Suite**: Comprehensive unit tests
4. **Documentation**: API documentation and examples

## 📚 Further Reading

### Blind Signatures
- [RSA Blind Signatures](https://en.wikipedia.org/wiki/Blind_signature)
- [Chaum's Original Paper](https://link.springer.com/content/pdf/10.1007/3-540-39568-7_2.pdf)

### Dilithium
- [Dilithium Specification](https://pq-crystals.org/dilithium/)
- [NIST PQC Competition](https://csrc.nist.gov/projects/post-quantum-cryptography)

### Post-Quantum Blind Signatures
- [Lattice-Based Blind Signatures](https://eprint.iacr.org/2019/877)
- [Research Survey](https://eprint.iacr.org/2020/1003)

## 🤝 Contributing

This is an educational project. Contributions are welcome for:
- Bug fixes
- Documentation improvements
- Educational enhancements
- Research implementations

## 📄 License

This project is for educational purposes. Please ensure compliance with relevant cryptographic export regulations in your jurisdiction.

## ⚖️ Disclaimer

This software is provided "as is" for educational purposes only. It is not suitable for production use or security-critical applications. Users should understand the limitations and conduct their own security analysis before any deployment.

---

**Note**: This implementation serves as a valuable learning tool for understanding the challenges of implementing blind signatures with post-quantum cryptographic schemes. It clearly demonstrates both the possibilities and limitations of current approaches. 