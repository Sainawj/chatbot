import secrets

def generate_flask_secret_key():
    """Generates a random Flask secret key."""
    secret_key = secrets.token_hex(32)  # 32 bytes = 64-character hex string
    print("Your generated Flask secret key:")
    print(secret_key)
    return secret_key

if __name__ == "__main__":
    generate_flask_secret_key()

