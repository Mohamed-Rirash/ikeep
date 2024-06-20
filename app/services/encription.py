import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


def encrypt_data(data: str, public_key: str) -> str:
    public_key_obj = serialization.load_pem_public_key(
        public_key.encode('utf-8'),
        backend=default_backend()
    )
    encrypted_data = public_key_obj.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_data(encrypted_data: str, private_key: str) -> str:
    private_key_obj = serialization.load_pem_private_key(
        private_key.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    decrypted_data = private_key_obj.decrypt(
        encrypted_data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode('utf-8')
