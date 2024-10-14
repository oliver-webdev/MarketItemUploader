import requests

files = {
    f"imageFiles{[0]}":("image1.png",open(r"dt_img_01.png","rb"),'image/png') #,
    # f"imageFiles{[1]}":("image2.JPG",open(r"downloaded_image_1.jpg","rb"),'image/jpeg')
}

def upload_images():
    from datetime import datetime, timedelta

    headers = {'Authorization': '4WcOICnnzyaMbO5ENWZtnN'}
    url = 'https://api.commerce.naver.com/external/v1/product-images/upload'
    
    res = requests.post(url=url, headers=headers, files=files)
    res_data = res.json()

    print(res_data)

upload_images()