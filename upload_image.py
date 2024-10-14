import requests
import os
import time

def upload_product_image(arr_img_path, token):
    """
    이미지 파일을 서버에 올리고
    업로드 완료한 URL을 반환

    Parameters:
        arr_img_path (arr): 이미지 파일명 배열

    Returns:
        json: 업로드된 이미지 url

    ↓↓↓ request 파라미터 files 예시
    files = {
        f"imageFiles{[0]}":("image1.JPG",open(r"downloaded_image_0.jpg","rb"),'image/jpeg'),
        f"imageFiles{[1]}":("image2.JPG",open(r"downloaded_image_1.jpg","rb"),'image/jpeg')
    }

    ↓↓↓ response json 예시
    {
        'images': [{'url': 'https://shop-phinf.pstatic.net/20240727_58/1722092299460z3qAW_JPEG/3127733334049553_1146674885.JPG'}, 
                   {'url': 'https://shop-phinf.pstatic.net/20240727_58/1722092299460z3qAW_JPEG/3127733334049553_1146674885.JPG'}]
    }
    """

    headers = {
        'Authorization': token
    }
    url = 'https://api.commerce.naver.com/external/v1/product-images/upload'
    url_arr = []

    # 1. 안내 이미지(고정) 업로드 & url 가져오기
    files = {
        f"imageFiles{[0]}":("image1.png",open(r"dt_img_01.png","rb"),'image/png'),
        f"imageFiles{[1]}":("image2.png",open(r"dt_img_02.png","rb"),'image/png'),
        f"imageFiles{[2]}":("image3.png",open(r"dt_img_03.png","rb"),'image/png')
    }
   
    res = requests.post(url=url, headers=headers, files=files)
    res_data = res.json()
    print(res_data)
    print("---안내문 업로드 완료")

    results = res_data.get('images')
    for img_notice in results:
        url_arr.append(img_notice.get('url'))

    # 2. 상품 이미지 업로드 & url 가져오기
    files = {}
    index = 0
    for data in arr_img_path:
        try:
            files[f"imageFiles{[index]}"] = (f"image{index}.JPG",open(f"{data}","rb"),'image/jpeg')
        except Exception as e:
            print(f"파일 읽기 에러 발생: {e}")
        time.sleep(1) # 파일 읽기 시간
        index = index + 1

        # 업로드가 완료되면 로컬 이미지 파일 삭제
        try:
            if os.path.isfile(data):
                os.remove(data)
                print(f"파일 {data} 가 삭제되었습니다.")
            else:
                print(f"파일 {data} 이(가) 존재하지 않습니다.")
        except Exception as e:
            print(f"파일을 삭제하는 중 오류가 발생했습니다: {e}")
    
    # files 확인
    print(f"--- 업로드 files 확인: {files}")

    # 서버에 파일 업로드
    res = requests.post(url=url, headers=headers, files=files)
    res_data = res.json()
    print(res_data)

    results = res_data.get('images')
    for img_product in results:
        url_arr.append(img_product.get('url'))
    
    return ','.join(url_arr)

# 테스트용
# upload_product_image(['downloaded_image_0.jpg', 'downloaded_image_1.jpg'])