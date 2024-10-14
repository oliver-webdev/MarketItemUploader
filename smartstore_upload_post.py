
import requests

from get_token import get_token

# POST 요청
def post_request(url, json_data=None, headers=None):
    res = requests.post(url, json=json_data, headers=headers)
    res_data = res.json()
    print(res_data)

# 스마트 스토어에 1건의 상품을 업로드
def upload_to_smartstore(payload):
    token = get_token(client_id='wlzNpmIHUiTBUzf6Bor7C', client_secret='$2a$04$IUvzowqvAMl/LbLCGNUgke')
   
    # 상품 전송
    url = 'https://api.commerce.naver.com/external/v2/products'
    headers = {
        'Authorization': token,
        'content-type': "application/json"
    }

    post_request(url, payload, headers)

    # res = requests.post(url=url, headers=headers, json=payload)
    # res_data = res.json()
    # print(res_data)
