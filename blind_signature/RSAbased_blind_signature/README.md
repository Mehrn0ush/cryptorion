# RSA-Based Blind Signature Implementation

**⚠️ EDUCATIONAL PURPOSE ONLY ⚠️**

This directory contains a complete implementation of RSA-based blind signatures developed **exclusively for educational and research purposes**. This implementation is designed to help students, researchers, and cryptography enthusiasts understand the concepts and mechanics of blind signature schemes.

**Important Notice:**
- This code is **NOT intended for production use**
- It is **NOT suitable for real-world cryptographic applications**
- It serves as a **learning tool** to demonstrate blind signature concepts
- Use only in **educational environments** and **controlled research settings**

This cryptographic primitive allows a signer to sign a message without knowing its content. It's particularly useful in privacy-preserving applications like anonymous voting systems, digital cash, and privacy-preserving authentication.

## Overview

Blind signatures enable a user (message owner) to obtain a signature on a message from a signer without revealing the actual message content to the signer. The process involves two main phases:

1. **Blinding Phase**: The message owner blinds the message using a random factor
2. **Unblinding Phase**: The message owner unblinds the signature to obtain the final signature

## Theory

### Mathematical Foundation

The RSA blind signature scheme is based on the RSA cryptosystem and works as follows:

1. **Key Generation**: Signer generates RSA key pair `(e, N)` (public) and `(d, N)` (private)
2. **Blinding**: Message owner computes `m' = m * r^e mod N` where:
   - `m` is the hash of the original message
   - `r` is a random blinding factor coprime with `N`
   - `e` is the signer's public exponent
3. **Signing**: Signer computes `s' = (m')^d mod N`
4. **Unblinding**: Message owner computes `s = s' * r^(-1) mod N`
5. **Verification**: Anyone can verify using `s^e mod N == m mod N`

### Security Properties

- **Blindness**: The signer cannot learn anything about the original message
- **Unforgeability**: Only the signer can create valid signatures
- **Unlinkability**: The signer cannot link a signature to the original blinded message

## Files

- `message_owner.py` - Implementation of the message owner's role in the blind signature protocol
- `signer.py` - Implementation of the signer's role in the blind signature protocol
- `README.md` - This documentation file

## Requirements

```bash
pip install pycryptodome
```

## Usage

### Step 1: Message Owner Creates Blinded Message

```bash
python message_owner.py
```

This will:
- Generate RSA keys (in a real scenario, the signer would have persistent keys)
- Create a blinded message from the original message
- Save the blinded data to `blind_data.json`
- Save the signer's private key to `signer_private_key.json`

### Step 2: Signer Signs the Blinded Message

```bash
python signer.py
```

This will:
- Load the private key and blinded message
- Sign the blinded message
- Save the blind signature to `blind_signature.json`

### Step 3: Message Owner Unblinds the Signature

```bash
python message_owner.py phase2
```

This will:
- Load the blind signature and original blinding factor
- Unblind the signature to obtain the final signature
- Verify the signature against the original message

## Example Output

```
=== Message Owner Phase 1: Create Blinded Message ===
Original message: This is my secret vote: Candidate A

Blinding complete. Results:
Blinded message: 91469945880187201036570024167186306780430775206952917833545151507508447532767911681002718753654208396759846872064347730292832499727087368646366264434274357944230061692475364686830686281890976464159853693958638198238229025643692589657838277001031472006190507167685972042330856645905888152049891792810632608577
Blinding factor r: 84856476875336648264836932171416162361719177432334227812537726182795434543137227528041368797516727710618443183303127281827729239299811580703316870859978475739321086410287859396155922460070553416964967453135951473276948656907493334521423884241273313951337828008311463598387194119159067307551384073457956957584 (secret)
Original hash: 84677053352968143520765055090150892877387638760921596052364781474031647437045 (for reference)

Saved blind_data.json for signer to process
Note: The blinding factor r is stored locally for phase 2

=== Signer Process ===
Using RSA keys:
Public key (e, N): (66260322091908700624734226604842386394357927963506884938237471106240546407729560868690479328113983006941123296879733443253786464319726890263535799837267311413093673393666769447010177687093220009138698431617741950652711977845125601539973438014473190533919501706377628476676877862335248196258506998657067223393, 145389806111471156851587217389900745852652856734443240866387744204154502809808900182515332252799186565083045316312009196147160958622001513566403700078176928831118310937019610133234086435284423677135005050724120408716004026659686380246781556155519091227597209304137664960951698495555230649323435685551895730619)
Private key (d, N): (hidden)

Received blinded message: 91469945880187201036570024167186306780430775206952917833545151507508447532767911681002718753654208396759846872064347730292832499727087368646366264434274357944230061692475364686830686281890976464159853693958638198238229025643692589657838277001031472006190507167685972042330856645905888152049891792810632608577

Created blind signature: 118076841185937756492189402057273857391622029270557201741392350053628628166443546798041241839284355314354840554663945581628633045168137471177298488176893612899210946358829263050083357414511553312827998642044856483938238254883571076000643733122253686301264720497369358742721590582631703291996896974228574907765

Saved blind_signature.json for message owner to process

=== Message Owner Phase 2: Unblind Signature ===
Received blind signature: 118076841185937756492189402057273857391622029270557201741392350053628628166443546798041241839284355314354840554663945581628633045168137471177298488176893612899210946358829263050083357414511553312827998642044856483938238254883571076000643733122253686301264720497369358742721590582631703291996896974228574907765

Unblinded signature: 53528245560290481599823598178331782751321867690075906156503781181499814353808585682473118983258901072274314187120433007690837374888861043209747674316514141996635350609700837968920922200178587767078238170189348339503361269995107655941590020509794243452960720515643186183114613034531296461905246946548050763163

Verification results:
Signature is valid: True
```

## Code Structure and Methods

### MessageOwner Class

The `MessageOwner` class handles the message blinding, unblinding, and verification processes:

```python
class MessageOwner:
    def __init__(self, signer_public_key):
        """Initialize with signer's public key (e, N)"""
    
    def blind_message(self, message, r=None):
        """Blind a message using RSA blind signature scheme"""
    
    def unblind_signature(self, blinded_signature, r):
        """Unblind a signature using the original blinding factor"""
    
    def verify(self, message, signature):
        """Verify a signature against a message"""
```

### Signer Class

The `Signer` class handles the signing of blinded messages:

```python
class Signer:
    def __init__(self, private_key):
        """Initialize with private key (d, N)"""
    
    def sign_blinded(self, blinded_message):
        """Sign a blinded message"""
```

### Utility Functions

```python
def generate_rsa_keys(key_size=1024):
    """Generate RSA key pair for blind signature scheme"""
```

### Helper Methods (Internal)

The `MessageOwner` class also includes internal helper methods:
- `_gcd(a, b)`: Calculates greatest common divisor
- `_modinv(a, m)`: Calculates modular multiplicative inverse
- `_egcd(a, b)`: Extended Euclidean algorithm

## Security Considerations

**⚠️ EDUCATIONAL IMPLEMENTATION LIMITATIONS ⚠️**

This implementation has several limitations that make it unsuitable for production use:

1. **Key Size**: This implementation uses 1024-bit RSA keys for demonstration purposes only. In production, use at least 2048-bit keys.

2. **Random Number Generation**: The blinding factor `r` must be cryptographically secure and coprime with `N`. This implementation uses basic random generation for educational clarity.

3. **Hash Function**: The implementation uses SHA-256 for message hashing, which is appropriate for educational purposes.

4. **Key Management**: In a real system, the signer should have persistent keys and proper key management. This implementation generates keys on-the-fly for simplicity.

5. **Error Handling**: Limited error handling for educational clarity - production systems require robust error handling.

6. **Side-Channel Protection**: No protection against timing attacks or other side-channel vulnerabilities.

**For Production Use:** Please use established cryptographic libraries and implementations that have been thoroughly audited and tested.

## Applications

- **Anonymous Voting**: Voters can cast ballots without revealing their choices
- **Digital Cash**: Users can spend digital currency without being tracked
- **Privacy-Preserving Authentication**: Users can prove identity without revealing personal information
- **Anonymous Credentials**: Users can prove possession of credentials without revealing identity

## Limitations

- **Computational Overhead**: Blind signatures require additional cryptographic operations
- **Key Management**: Requires secure key generation and storage
- **Protocol Complexity**: More complex than standard digital signatures

## References

- Chaum, D. (1983). "Blind signatures for untraceable payments"
- Rivest, R. L., Shamir, A., & Adleman, L. (1978). "A method for obtaining digital signatures and public-key cryptosystems"

## Educational Use Guidelines

### Intended Audience
- **Students** learning cryptography and digital signature schemes
- **Researchers** studying blind signature protocols
- **Educators** teaching cryptographic concepts
- **Hobbyists** interested in understanding privacy-preserving technologies

### Learning Objectives
This implementation helps learners understand:
- The mathematical foundations of RSA blind signatures
- The step-by-step process of blinding, signing, and unblinding
- The security properties of blind signature schemes
- Practical implementation considerations

### Recommended Learning Path
1. Read the theoretical background in the "Theory" section
2. Study the mathematical formulas and understand each step
3. Run the example code to see the protocol in action
4. Experiment with different messages and parameters
5. Explore the code to understand the implementation details

## License

This implementation is provided **exclusively for educational and research purposes**. 

**⚠️ DISCLAIMER ⚠️**
- This code is provided "as is" without any warranties
- The authors are not responsible for any misuse of this code
- This implementation is NOT suitable for production environments
- Users should not rely on this code for any security-critical applications
