import secrets

# Generate a random byte string (e.g., 256 bits)
secret_key_bytes = secrets.token_bytes(32)

# Convert bytes to string using hex encoding
secret_key = secrets.token_hex(32)

print(secret_key)