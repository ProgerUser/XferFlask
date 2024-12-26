import base64
import hashlib
import hmac
from datetime import datetime
from urllib.parse import unquote

m_ApplicationSecret = '3o39NbVH3EpIAEAC9LQpwkZHnLXvOoZ1BNKmU1TsG5D2aJtjjMc8gNJCKOz2XTo6IRmGveJ+3pq+OoT1'
m_ApplicationId = '568B3EB669860F18383B'


def add_authorization_to_request(request):
    request.headers['Date'] = datetime.utcnow()
    representation = to_string_representation(request)
    signature = base64.b64encode(
        hmac.new(m_ApplicationSecret.encode(), representation.encode(), hashlib.sha256).digest()).decode()

    parameter = f"UNIHMAC {m_ApplicationId}:{signature}"
    request.headers['Authorization'] = parameter


def to_string_representation(request):
    result = []
    result.append(request.method.upper())
    result.append(base64.b64encode(request.content.headers.get('Content-MD5',
                                                               b'')).decode() if request.content and request.content.headers and 'Content-MD5' in request.content.headers else "")
    result.append(
        request.headers.get('Date').strftime("%a, %d %b %Y %H:%M:%S GMT") if 'Date' in request.headers else "")
    result.append(unquote(request.request_uri.path_and_query).lower())

    x_bank_headers = {k: v for k, v in request.headers.items() if k.lower().startswith("x-{bank}-")}
    for key in sorted(x_bank_headers.keys(), key=lambda k: k.lower()):
        for value in x_bank_headers[key]:
            result.append(value)

    return '\n'.join(result)


def hmac_sha256_hash(message, key_base64_string, encoding='utf-8'):
    key = base64.b64decode(key_base64_string)
    return hmac.new(key, message.encode(encoding), hashlib.sha256).digest()
