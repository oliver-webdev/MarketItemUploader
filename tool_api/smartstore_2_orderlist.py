import requests

def get_new_order_list():
    from datetime import datetime, timedelta

    headers = {'Authorization': '1kzukuAywRfZcG3qz38nQi'}
    url = 'https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/last-changed-statuses'
    
    now = datetime.now()
    # before_date = now - timedelta(hours=3) #3시간전
    # before_date = now - timedelta(seconds=10) #10초전
    # before_date = now - timedelta(minutes=10) #10분전
    before_date = now - timedelta(days=2) #이틀전
    iosFormat = before_date.astimezone().isoformat()

    params = {
            'lastChangedFrom' : iosFormat, #조회시작일시
            'lastChangedType' : 'DISPATCHED', #최종변경구분(PAYED : 결제완료, DISPATCHED : 발송처리)
        }

    res = requests.get(url=url, headers=headers, params=params)
    res_data = res.json()

    if 'data' not in res_data: #조회된 정보가 없을 경우 data키 없음
        print('주문 내역 없음')
        return False

    data_list = res_data['data']['lastChangeStatuses']

    for data in data_list:
        print(data) #주문 정보


get_new_order_list()
