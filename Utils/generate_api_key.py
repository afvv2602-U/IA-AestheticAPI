import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

# Generar una clave API
api_key = generate_api_key()
print(f'Your API key: {api_key}')
