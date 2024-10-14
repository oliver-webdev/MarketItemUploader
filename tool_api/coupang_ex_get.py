import os
import time
import hmac, hashlib
import requests

# GET 요청 예제
def get_request(url, headers=None):
    response = requests.get(url, headers=headers)
    print("GET 요청 응답 상태 코드:", response.status_code)
    print("GET 요청 응답 본문:", response.text)

# 등록상품ID
sellerProductId = "15098791344"

os.environ['TZ'] = 'GMT+0'
datetime=time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
method = "GET"

# END POINT
path = f"/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{sellerProductId}"

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
    "Content-Type": "application/json",
    "Authorization": authorization
}

get_request(url, headers)
