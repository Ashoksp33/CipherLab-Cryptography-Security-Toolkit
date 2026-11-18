"""RSA Public-Key Cryptography and Digital Signature Tool.

Implements:
- 2048-bit RSA key pair generation with PEM serialization
- Encryption and decryption using OAEP (SHA-256 padding)
- Digital signatures (PSS + SHA-256) and verification
- Strict message-size enforcement for OAEP padding
"""

import base64
from typing import Tuple, Union

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)

# 2048-bit key = 256 bytes. OAEP with SHA-256 consumes 2 * 32 + 2 = 66 bytes.
MAX_OAEP_PLAINTEXT_BYTES = 256 - (2 * 32 + 2)  # 190 bytes


def generate_key_pair() -> Tuple[str, str]:
    """Generate a new 2048-bit RSA key pair.

    Returns:
        Tuple of (private_key_pem, public_key_pem) as strings.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    ).decode("utf-8")

    public_pem = private_key.public_key().public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    return private_pem, public_pem


def encrypt(message: Union[str, bytes], public_key_pem: str) -> str:
    """Encrypt a message using RSA-OAEP with SHA-256 and the recipient's public key.

    Args:
        message: Plaintext string or bytes.
        public_key_pem: Public key in PEM format.

    Returns:
        Base64-encoded ciphertext string.

    Raises:
        ValueError: If message is empty, exceeds 190 bytes, or key is invalid.
    """
    if not message:
        raise ValueError("Input message cannot be empty.")
    if not public_key_pem or not public_key_pem.strip():
        raise ValueError("Public key PEM cannot be empty.")

    msg_bytes = message.encode("utf-8") if isinstance(message, str) else message
    if len(msg_bytes) > MAX_OAEP_PLAINTEXT_BYTES:
        raise ValueError(
            f"Message size ({len(msg_bytes)} bytes) exceeds the maximum limit "
            f"of {MAX_OAEP_PLAINTEXT_BYTES} bytes for 2048-bit RSA with OAEP-SHA256 padding. "
            "For larger messages, use hybrid encryption (AES key encrypted with RSA)."
        )

    try:
        public_key = load_pem_public_key(public_key_pem.encode("utf-8"))
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise ValueError("Provided key is not an RSA public key.")
    except Exception as e:
        raise ValueError(f"Invalid public key PEM: {str(e)}")

    try:
        ciphertext = public_key.encrypt(
            msg_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return base64.b64encode(ciphertext).decode("utf-8")
    except Exception as e:
        raise ValueError(f"RSA encryption failed: {str(e)}")


def decrypt(ciphertext_b64: str, private_key_pem: str) -> str:
    """Decrypt base64-encoded ciphertext using RSA-OAEP and the private key.

    Args:
        ciphertext_b64: Base64-encoded ciphertext string.
        private_key_pem: Private key in PEM format.

    Returns:
        Decrypted plaintext string.

    Raises:
        ValueError: If decryption fails or inputs are invalid.
    """
    if not ciphertext_b64 or not ciphertext_b64.strip():
        raise ValueError("Ciphertext cannot be empty.")
    if not private_key_pem or not private_key_pem.strip():
        raise ValueError("Private key PEM cannot be empty.")

    try:
        ciphertext = base64.b64decode(ciphertext_b64.strip(), validate=True)
    except Exception:
        raise ValueError("Invalid base64 ciphertext.")

    try:
        private_key = load_pem_private_key(
            private_key_pem.encode("utf-8"),
            password=None,
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise ValueError("Provided key is not an RSA private key.")
    except Exception as e:
        raise ValueError(f"Invalid private key PEM: {str(e)}")

    try:
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext_bytes.decode("utf-8")
    except Exception:
        raise ValueError("RSA decryption failed: wrong private key or corrupted ciphertext.")


def sign(message: Union[str, bytes], private_key_pem: str) -> str:
    """Digitally sign a message using RSA-PSS with SHA-256.

    Args:
        message: String or bytes to sign.
        private_key_pem: Signer's private key in PEM format.

    Returns:
        Base64-encoded digital signature string.

    Raises:
        ValueError: If message or private key is invalid.
    """
    if not message:
        raise ValueError("Message to sign cannot be empty.")
    if not private_key_pem or not private_key_pem.strip():
        raise ValueError("Private key PEM cannot be empty.")

    msg_bytes = message.encode("utf-8") if isinstance(message, str) else message

    try:
        private_key = load_pem_private_key(
            private_key_pem.encode("utf-8"),
            password=None,
        )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise ValueError("Provided key is not an RSA private key.")
    except Exception as e:
        raise ValueError(f"Invalid private key PEM: {str(e)}")

    try:
        signature = private_key.sign(
            msg_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(signature).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Signing failed: {str(e)}")


def verify(
    message: Union[str, bytes],
    signature_b64: str,
    public_key_pem: str,
) -> bool:
    """Verify an RSA-PSS digital signature.

    Args:
        message: Original message string or bytes.
        signature_b64: Base64-encoded signature.
        public_key_pem: Signer's public key in PEM format.

    Returns:
        True if signature is valid; False otherwise. Never crashes or raises.
    """
    if not message or not signature_b64 or not public_key_pem:
        return False

    msg_bytes = message.encode("utf-8") if isinstance(message, str) else message

    try:
        signature = base64.b64decode(signature_b64.strip(), validate=True)
        public_key = load_pem_public_key(public_key_pem.encode("utf-8"))
        if not isinstance(public_key, rsa.RSAPublicKey):
            return False

        public_key.verify(
            signature,
            msg_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, Exception):
        return False
