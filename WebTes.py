import hmac
import hashlib

def hmac_sha256(key, message):
  return hmac.new(
    key.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256
  ).hexdigest()

def main():
  secret_key = "YOUR_SECRET_KEY"
  content = "YOUR_CONTENT"
  hashed = hmac_sha256(secret_key, content)
  print(hashed)