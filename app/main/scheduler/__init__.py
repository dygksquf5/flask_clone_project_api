import requests
import json


def sensor():
    print("Scheduler is alive!")
    # GET
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    res = requests.get('http://localhost:5000/order/schedule')
    print(str(res.status_code) + " | " + res.text)
    if not res.text:
        print(' nothing ')
    else:
        info = res.json()
        for order in info:
            data = {
                'order_id': order['uuid'],
                'set_status': 5
            }
            res = requests.patch('http://localhost:5000/order/status', data=json.dumps(data), headers=headers)
            print(str(res.status_code) + " | " + res.text)
