import json
from mongo import MonGo

# 函数名必须是response
# flow为fiddler所抓到的包
from config import DEBUG


def field(_list):
    result = []
    for hotel in _list:
        one = {'hotelName': hotel['base']['hotelName'], 'hotelId': hotel['base']['hotelId'],
               'badgeHover': 'badgeHover' in hotel['base'], 'lat': hotel['position']['lat'],
               'lng': hotel['position']['lng'], 'cityName': hotel['position']['cityName'],
               'area': hotel['position']['area'], 'address': hotel['position']['address'],
               'number': hotel['score'].get('number', None), 'checkIn': json.loads(hotel['traceInfo'])['checkIn'],
               'checkOut': json.loads(hotel['traceInfo'])['checkOut'], 'star': hotel['base']['star'],
               'priceDelete': hotel['money'].get('priceDelete', None), 'price': hotel['money']['price'],
               'ImageUrl': hotel['picture']['list'][0]}
        result.append(one)
    return result


def response(flow):
    if 'm.ctrip.com/restapi/soa2/21881/json/HotelSearch' in flow.request.url:
        print('===========================' * 3)
        origin_list = json.loads(flow.response.text)['Response']['hotelList']['list']
        hotel_list = field(_list=origin_list)
        print(hotel_list)
        MonGo().insert_data(collection='hotel', data=hotel_list)

    # mitmdump -s C:\Users\xdc\Desktop\demo\spider\携程\test.py -p 8080
    # chrome --remote-debugging-port=9222
