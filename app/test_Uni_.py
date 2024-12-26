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
        '595425'
    ]
    data = '\n'.join(representation_mixture)
    representation_mixture.extend(headers)
    representation = base64.b64encode('\n'.join(representation_mixture).encode()).decode()
    hmac_sha256 = hmac.new(base64.b64decode(app_secret), bytes(data, 'utf-8'), hashlib.sha256).digest()
    request_hash = base64.b64encode(hmac_sha256).decode()
    return {
        'VERB': 'GET',
        'Content-MD5': content_md5,
        'Date': date,
        'PATH-AND-QUERY': path_and_query,
        'X-Unistream-Security-PosId': '595425',
        'Authorization': f'UNIHMAC {app_id}:{request_hash}'
    }


def testcon():
    app_id = '568B3EB669860F18383B'
    app_secret = '3o39NbVH3EpIAEAC9LQpwkZHnLXvOoZ1BNKmU1TsG5D2aJtjjMc8gNJCKOz2XTo6IRmGveJ+3pq+OoT1'
    doc_number = '7585863539'  # Номер документа, уникально идентифицирующий документ среди документов того же типа. Например, для уникального номера документа Passport.RUS.1234012345, номер для поиска будет 1234012345 (серия+номер).
    skip_restriction = False  # Пропустить проверку идентифицируемых документов, если установлено значение true
    page = 1  # Номер страницы
    rows = 20  # Количество элементов на странице
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
        'VERB': 'GET',
        'CONTENT-MD5': '',
        'DATE': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()),
        'PATH-AND-QUERY': method,
        'X-Unistream-Security-PosId': '595425'
    }
    md5 = get_auth_http_header(app_id=app_id,
                               app_secret=app_secret,
                               path_and_query=method,
                               request_method='GET',
                               headers=headers,
                               payload=False);
    print(str(md5))
    response = requests.request(method="GET", url=url, headers=md5, data=payload)
    print(str(response.text))


testcon()
