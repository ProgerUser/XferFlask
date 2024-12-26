import base64
import hashlib
import hmac
import time
import urllib
import requests


def get_auth_http_header(app_id, app_secret, path_and_query, request_method, headers=None, payload=False):
    if headers is None:
        headers = []
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    content_md5 = base64.b64encode(hashlib.md5(payload.encode() if payload else b'').digest()).decode()
    representation_mixture = [
        request_method.upper(),
        content_md5,
        date,
        urllib.parse.unquote(path_and_query).lower(),
    ]
    representation_mixture.extend(headers)
    representation = base64.b64encode('\n'.join(representation_mixture).encode()).decode()
    hmac_sha256 = hmac.new(base64.b64decode(app_secret), base64.b64decode(representation), hashlib.sha256).digest()
    request_hash = base64.b64encode(hmac_sha256).decode()
    return {
        'VERB': request_method,
        'Content-MD5': content_md5,
        'Date': date,
        'PATH-AND-QUERY': path_and_query,
        'X-UNISTREAM-HEADERS': '595425',
        'X-Unistream-Security-PosId': '595425',
        'Authorization': f'UNIHMAC {app_id}:{request_hash}'
    }


def testcon():
    bank_id = '595425'
    verb = 'GET'
    app_id = '568B3EB669860F18383B'
    app_secret = '3o39NbVH3EpIAEAC9LQpwkZHnLXvOoZ1BNKmU1TsG5D2aJtjjMc8gNJCKOz2XTo6IRmGveJ+3pq+OoT1'
    doc_number = 'Passport.RUS.1234012345'
    skip_restriction = False
    page = 1
    rows = 10
    url_b = 'https://slt-test.api.unistream.com'
    method = '/' + ('v2/clients/search?documentNumber=' +
                    doc_number +
                    '&skipRestrictions=' +
                    str(skip_restriction) +
                    '&page=' +
                    str(page) +
                    '&rows=' +
                    str(rows))
    url = url_b + method

    payload = {}

    headers = {
        'VERB': verb,
        'CONTENT-MD5': '',
        'DATE': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()),
        'PATH-AND-QUERY': method,
        'X-UNISTREAM-HEADERS': bank_id
    }

    md5 = get_auth_http_header(app_id=app_id,
                               app_secret=app_secret,
                               path_and_query=method,
                               request_method=verb,
                               headers=headers,
                               payload=False);
    print(str(md5))
    response = requests.request(method="GET", url=url, headers=md5, data=payload)
    print(str(response.text))


md5 = ''
app_id = '568B3EB669860F18383B'
app_secret = '3o39NbVH3EpIAEAC9LQpwkZHnLXvOoZ1BNKmU1TsG5D2aJtjjMc8gNJCKOz2XTo6IRmGveJ+3pq+OoT1'
pngq = '/v2/clients/search?documentNumber=Passport.RUS.1234012345&skipRestrictions=False&page=1&rows=10'
dt = 'Thu, 26 Dec 2024 11:24:33 GMT'
request_method = 'GET'

hmac_sha256 = hmac.new(
    app_secret.encode("utf-8"),
    request_method.upper() + '\n'.encode("utf-8") + md5 + '\n'.encode("utf-8") + '\n'.dt + urllib.parse.unquote(
        pngq).lower() + '595425',
    hashlib.sha256
).hexdigest()

request_hash = base64.b64encode(hmac_sha256).decode()

print(request_hash)

'''"base64(hmac-sha256(APPLICATION_SECRET,
                       to-upper(VERB) + "\n"
                     + CONTENT-MD5 + "\n"
                     + DATE + "\n"
                     + to-lower(url-decode(PATH-AND-QUERY))
                     + X-{BANK}-HEADERS ))
'''

#testcon()
