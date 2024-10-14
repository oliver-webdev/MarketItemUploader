import os
import time
import hmac, hashlib
import requests

"""
쿠팡 OPEN API용 IP:
61.73.128.8,121.143.74.18,61.32.197.218,175.211.95.82
신촌집, 인천집, 스카, 레피사무실

* 과제
notices 일단 하드 코딩 / 자동화 가능 할지? / 메커니즘 이해 필요 / noticeCategoryName, noticeCategoryDetailName
attributes 동일 방식
"""

# POST 요청
def post_request(url, json_data=None, headers=None):
    response = requests.post(url, json=json_data, headers=headers)
    print("POST 요청 응답 상태 코드:", response.status_code)
    print("POST 요청 응답 본문:", response.text)

# 쿠팡 상품 업로드를 위한 설정
def upload_to_coupang(json_data):

    os.environ['TZ'] = 'GMT+0'
    datetime=time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
    method = "POST"

    # END POINT
    path = "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products"

    # ACCESS KEY
    accesskey = "b4655286-298e-4f03-9f08-9c5a7111c38b"
    # SECRET KEY
    secretkey = "e72014c29f6b56a502e592337c8c4336de014417"

    message = datetime+method+path

    signature=hmac.new(secretkey.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()

    authorization  = "CEA algorithm=HmacSHA256, access-key="+accesskey+", signed-date="+datetime+", signature="+signature

    # ************* SEND THE REQUEST *************
    url = "https://api-gateway.coupang.com"+path

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": authorization
    }

    post_request(url, json_data, headers)
