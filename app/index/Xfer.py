import datetime
import decimal
import http.client
import json
import time
import uuid
from base64 import b64encode
import simplejson as json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from flask import Flask
from flask import jsonify
from flask import request
import ssl

app = Flask(__name__)


def curTime():
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%dT%H:%M:%S%z")
    return str(timestamp) + "Z"


def encAES(message):
    # load private key
    with open('C:/XferFlask/app/index/restapikey.key', 'r') as f:
        private_key = RSA.import_key(f.read())

    # hash the message
    digest = SHA256.new(message.encode())

    # sign the digest
    signature = pkcs1_15.new(private_key).sign(digest)

    # base64 encode the signature
    signature_b64 = b64encode(signature).decode('utf-8')
    return signature_b64


@app.route('/xfer/participantlist', methods=['GET'])
def sendParcipiantList():
    try:
        v_requester_id = 10115
        v_timestamp = curTime()

        hs = (str(v_requester_id) +
              v_timestamp)
        print(hs)
        conn = http.client.HTTPSConnection("api.xfer.world", context=ssl._create_unverified_context())

        payload = json.dumps({
            "timestamp": v_timestamp,
            "requesterId": v_requester_id,
            "originatorSignature": encAES(hs)
        })

        headers = {
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/v3/participantlist", payload, headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        responseObject = json.loads(data)
        conn.close()
    except Exception as e:
        return jsonify({'error': str(e)})
    return responseObject


def createORN():
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def convSum(inputNumber):
    decimal_value = decimal.Decimal(inputNumber)
    rounded_number = decimal_value.quantize(decimal.Decimal('0.00'))
    return rounded_number


@app.route('/xfer/check', methods=['POST'])
def xferCheck():
    try:
        data = request.get_json()

        fullName = data['fullName']
        displayName = data['displayName']

        additionalIdentification_address_value = data['additionalIdentification_address_value']
        additionalIdentification_birthday_value = data['additionalIdentification_birthday_value']
        additionalIdentification_passport_value = data['additionalIdentification_passport_value']

        v_originatorReferenceNumber = createORN()
        v_originator_identification_value = data['originator_identification_value']
        v_receiver_identification_value = data['receiver_identification_value']
        v_paymentAmount_amount = data['paymentAmount_amount']
        v_paymentAmount_currency = 'RUB'
        v_receivingAmount_amount = 'null'
        v_receivingAmount_currency = 'RUB'
        v_timestamp = curTime()

        hs = (v_originatorReferenceNumber +
              v_originator_identification_value +
              v_receiver_identification_value +
              v_paymentAmount_amount +
              v_paymentAmount_currency +
              v_receivingAmount_amount +
              v_receivingAmount_currency +
              v_timestamp)

        roundedNumber = convSum(v_paymentAmount_amount)

        conn = http.client.HTTPSConnection("api.xfer.world", context=ssl._create_unverified_context())

        payload = json.dumps({
            "timestamp": v_timestamp,
            "originatorReferenceNumber": v_originatorReferenceNumber,
            "originatorSignature": encAES(hs),
            "originator": {
                "identification": {
                    "type": "PHONE",
                    "value": v_originator_identification_value
                },
                "fullName": fullName,
                "displayName": displayName,
                "participant": {
                    "participantId": 10115
                },
                "additionalIdentification": [
                    {
                        "type": "ADDRESS",
                        "value": additionalIdentification_address_value
                    },
                    {
                        "type": "BIRTHDAY",
                        "value": additionalIdentification_birthday_value
                    },
                    {
                        "type": "PASSPORT",
                        "value": additionalIdentification_passport_value
                    }
                ]
            },
            "receiver": {
                "identification": {
                    "type": "PHONE",
                    "value": v_receiver_identification_value
                },
                "participant": {
                    "participantId": 10011
                }
            },
            "paymentAmount": {
                "amount": roundedNumber,
                "currency": "RUB"
            },
            "receivingAmount": {
                "currency": "RUB"
            }
        }, use_decimal=True)

        headers = {
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/v3/transfer/check", payload, headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        responseObject = json.loads(data)
        conn.close()
    except Exception as e:
        return jsonify({'response': str(e)})
    return responseObject


@app.route('/xfer/tst', methods=['GET'])
def xferTst():
    try:
        return jsonify({'MSG': 'Message'})

    except Exception as e:
        return jsonify({'MSG': 'Message'})


@app.route('/xfer/state', methods=['POST'])
def xferState():
    try:
        data = request.get_json()

        v_platformReferenceNumber = data['platformReferenceNumber']
        v_timestamp = curTime()

        hs = (v_platformReferenceNumber +
              v_timestamp)

        conn = http.client.HTTPSConnection("api.xfer.world", context=ssl._create_unverified_context())

        payload = json.dumps({
            "timestamp": v_timestamp,
            "platformReferenceNumber": v_platformReferenceNumber,
            "originatorSignature": encAES(hs)
        }
            , use_decimal=True)

        headers = {
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/v3/transfer/state", payload, headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        responseObject = json.loads(data)
        conn.close()
    except Exception as e:
        return jsonify({'response': str(e)})
    return responseObject


@app.route('/xfer/confirm', methods=['POST'])
def xferConfirm():
    try:
        data = request.get_json()

        fullName = data['fullName']
        displayName = data['displayName']
        displayNameRec = data['displayNameRec']
        additionalIdentification_address_value = data['additionalIdentification_address_value']
        additionalIdentification_birthday_value = data['additionalIdentification_birthday_value']
        additionalIdentification_passport_value = data['additionalIdentification_passport_value']
        v_originator_identification_value = data['originator_identification_value']
        v_receiver_identification_value = data['receiver_identification_value']

        v_settlementAmount_amount = data['paymentAmount_amount']
        v_settlementAmount_currency = 'RUB'
        v_platformReferenceNumber = data['platformReferenceNumber']
        v_paymentAmount_amount = data['paymentAmount_amount']
        v_paymentAmount_currency = 'RUB'
        v_receivingAmount_amount = data['paymentAmount_amount']
        v_receivingAmount_currency = 'RUB'
        v_timestamp = curTime()

        hs = (v_platformReferenceNumber +
              v_originator_identification_value +
              v_receiver_identification_value +
              v_paymentAmount_amount +
              v_paymentAmount_currency +
              v_settlementAmount_amount +
              v_settlementAmount_currency +
              v_receivingAmount_amount +
              v_receivingAmount_currency +
              v_timestamp)

        roundedNumber = convSum(v_paymentAmount_amount)

        conn = http.client.HTTPSConnection("api.xfer.world", context=ssl._create_unverified_context())

        payload = json.dumps({
            "timestamp": v_timestamp,
            "platformReferenceNumber": v_platformReferenceNumber,
            "originatorSignature": encAES(hs),
            "originator": {
                "identification": {
                    "type": "PHONE",
                    "value": v_originator_identification_value
                },
                "participant": {
                    "participantId": 10115
                },
                "fullName": fullName,
                "displayName": displayName,
                "additionalIdentification": [
                    {
                        "type": "ADDRESS",
                        "value": additionalIdentification_address_value
                    },
                    {
                        "type": "BIRTHDAY",
                        "value": additionalIdentification_birthday_value
                    },
                    {
                        "type": "PASSPORT",
                        "value": additionalIdentification_passport_value
                    }
                ]
            },
            "receiver": {
                "identification": {
                    "type": "PHONE",
                    "value": v_receiver_identification_value
                },
                "participant": {
                    "participantId": 10011
                },
                "displayName": displayNameRec,
                "currencies": [
                    "RUB"
                ]
            },
            "paymentAmount": {
                "amount": roundedNumber,
                "currency": "RUB"
            },
            "settlementAmount": {
                "amount": roundedNumber,
                "currency": "RUB"
            },
            "receivingAmount": {
                "amount": roundedNumber,
                "currency": "RUB"
            }
        }
            , use_decimal=True)

        headers = {
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/v3/transfer/confirm", payload, headers)
        response = conn.getresponse()
        data = response.read().decode("UTF-8")
        responseObject = json.loads(data)
        conn.close()
    except Exception as e:
        return jsonify({'response': str(e)})
    return responseObject


'''
@app.before_request
def limit_remote_addr():
    if request.remote_addr != '10.111.64.21' | request.remote_addr != '172.16.101.68' | request.remote_addr != '172.16.103.68':
        abort(403)  # Forbidden
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
