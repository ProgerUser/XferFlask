import base64
import hashlib
import hmac
import http.client
import json
import linecache
import ssl
import sys
import time
import urllib

import simplejson as json
from flask import Flask
from flask import jsonify

import genAuth

app = Flask(__name__)


@app.route('/uni/bankdeposit', methods=['GET'])
def bankdeposit():
    try:
        conn = http.client.HTTPSConnection("slt-test.api.unistream.com", context=ssl._create_unverified_context())

        payload = {

        }

        authData = get_auth_http_header(app_id='568B3EB669860F18383B',
                                        app_secret='3o39NbVH3EpIAEAC9LQpwkZHnLXvOoZ1BNKmU1TsG5D2aJtjjMc8gNJCKOz2XTo6IRmGveJ+3pq+OoT1',
                                        path_and_query='v2/bankdeposit/595425?pageSize=20&page=1',
                                        request_method='GET',
                                        headers='',
                                        payload=payload);

        print(authData)

        conn.request("GET", "v2/bankdeposit/595425?pageSize=20&page=1", payload, authData)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        responseObject = json.loads(response.text)
        conn.close()
    except Exception as e:
        return jsonify({'Exception': str(PrintException())})
    return responseObject


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


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
        'Authorization': f'UNIHMAC {app_id}:{request_hash}',
        'Date': date,
        'Content-MD5': content_md5
    }


@app.route('/xfer/tst', methods=['GET'])
def xferTst():
    try:
        return jsonify({'MSG': 'Message'})

    except Exception as e:
        return jsonify({'MSG': 'Message'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
