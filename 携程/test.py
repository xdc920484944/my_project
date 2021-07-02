import datetime
import json
import time

import requests

checkIn = datetime.datetime.now()
checkOut = checkIn + datetime.timedelta(days=1)


def hotel():
    data = {'city': '福州', 'keyword': '鼓楼区', 'start_date': checkIn, 'end_date': checkOut, 'low_price': '0',
            'high_price': '200'}
    r = requests.post(url='http://101.132.135.226:9566/hotel_list', json=data)


def bed():
    task = {
        'hotelIds': [
            {'task': ['479930', ], 'checkIn': '20210701', 'checkOut': '20210702'},
            {'task': ['6616554', ], 'checkIn': '20210701', 'checkOut': '20210702'},

        ]
    }
    r = requests.post(url='http://127.0.0.1:9566/hotel_detail', json=task)


hotel()
# bed()
