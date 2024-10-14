from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from googletrans import Translator
from PIL import Image
import pandas as pd
import requests
import os

def get_product_detail(url):
    
    try:
        # WebDriver 옵션: 창 안 띄워지도록 설정(추후 서버 혹은 백그라운드 환경에서 작동 가능)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # WebDriver 인스턴스를 생성합니다
        driver = webdriver.Chrome(options=options)

        # 지정한 URL로 브라우저를 엽니다.
        driver.get(url) # url 빈 값이 읽힌 경우 예외 발생: missing command parameters
        wait = WebDriverWait(driver, 5)
    except Exception as e:
        print(f"드라이버 초기화 중 에러 발생: {str(e)}")

    # return 데이터 초기화
    title = None
    desc = None
    html_table = None
    price = None
    img_path = []

    # 제품명
    try:
        title = wait.until(EC.presence_of_element_located((By.ID, 'productTitle')))
        print("제품명: ", title.text)
    except AttributeError:
        print("제품명 가져오기 실패")
    except Exception as e:
        print(f"제품명 가져오기 실패: {e}")

    # 제품설명
    try:
        desc = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#productDescription span')))
        print("제품설명: ", desc.text)
    except AttributeError:
        print("제품설명 가져오기 실패")
    except Exception as e:
        print(f"제품설명 가져오기 실패: {e}")
        desc = title

    # 치환할 문자열과 치환될 문자열을 딕셔너리로 정의
    replace_dict = {
        '범프 푸시': '반프레스토(Banpresto)',
        '포장': '패키지',
        '킬로그램': 'kg',
        '요한 ': 'JUN',
        '메가 하우스': '메가하우스(MegaHouse)'
    }

    # 테스트 중
    try:
        wait = WebDriverWait(driver, 10)

        # case1 ID를 가진 div 요소가 있는지 확인
        case1_div = driver.find_element(By.CSS_SELECTOR, '#detailBullets_feature_div')
        print("--- 불렛형 등록정보 처리")
        
        # case1 관련 로직을 여기서 수행
        detail_bullets_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#detailBullets_feature_div')))

        # div 내의 ul 요소를 찾고, 그 안에 있는 모든 li 요소들을 가져옵니다.
        li_elements = detail_bullets_div.find_elements(By.TAG_NAME, 'li')

        # li 요소 내 텍스트를 추출하여 리스트로 만듭니다.
        li_texts = [li.text for li in li_elements]

        # 결과 출력
        print(li_texts)

        # 텍스트를 항목과 값으로 분리하고, HTML 테이블 행으로 변환합니다.
        table_rows = []
        for text in li_texts:
            if ':' in text:
                key, value = map(str.strip, text.split(':', 1))
                
                # 번역기 설정
                translator = Translator()

                # 텍스트를 번역합니다. (일본어 -> 영어 예시)
                translated_key = translator.translate(key, src='auto', dest='ko').text
                translated_value = translator.translate(value, src='auto', dest='ko').text

                # translated_key가 replace_dict에 있는지 확인 후 치환
                if translated_key in replace_dict:
                    translated_key = replace_dict[translated_key]
                
                # translated_value replace_dict에 있는지 확인 후 치환
                if translated_value in replace_dict:
                    translated_key = replace_dict[translated_value]

                table_rows.append(f"""<tr>
<td style="background-color: #e0f7fa; font-weight: bold; padding: 8px; border: 1px solid #ddd; text-align: left;">
{translated_key}
</td>
<td style="background-color: #ffffff; padding: 8px; border: 1px solid #ddd; text-align: left;">
{translated_value}
</td>
</tr>
""")

        # HTML 테이블 생성 (스타일 포함)
        html_table = f"""<table style="border-collapse: collapse; table-layout: auto; width: 100%;">
<thead>
<tr>
<th style="background-color: #f2f2f2; font-weight: bold; padding: 12px; border: 1px solid #ddd; text-align: left;">
제품정보
</th>
<th style="background-color: #f2f2f2; padding: 12px; border: 1px solid #ddd; text-align: left;">
내용
</th>
</tr>
</thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
"""
        # HTML 테이블 출력
        print(f"--- 만들어진 테이블: {html_table}")

    except NoSuchElementException:
        print("--- 불렛형 등록정보 없음")

        try:
            # case2 ID를 가진 div 요소가 있는지 확인
            case2_div = driver.find_element(By.ID, 'productDetails_techSpec_section_1')
            print("--- 테이블형 등록정보 처리")
            # case2 관련 로직을 여기서 수행
            table = wait.until(EC.presence_of_element_located((By.ID, 'productDetails_techSpec_section_1')))

            # 테이블의 모든 행을 찾습니다.
            rows = table.find_elements(By.TAG_NAME, 'tr')

            # 테이블 데이터를 저장할 리스트 초기화
            table_data = []

            for row in rows:
                # 각 행에서 모든 열을 찾습니다.
                cols = row.find_elements(By.TAG_NAME, 'th')
                values = row.find_elements(By.TAG_NAME, 'td')
                
                # 열의 텍스트 값을 가져와서 리스트로 변환
                row_data = [col.text for col in cols] + [value.text for value in values]
                table_data.append(row_data)

            # pandas 데이터프레임으로 변환
            df = pd.DataFrame(table_data, columns=["Attribute", "Value"])

            # 번역기 설정
            translator = Translator()

            # 번역된 데이터를 저장할 리스트 초기화
            translated_data = []

            # 데이터프레임의 각 행을 번역
            for index, row in df.iterrows():
                attribute_translated = translator.translate(row['Attribute'], src='auto', dest='ko').text
                value_translated = translator.translate(row['Value'], src='auto', dest='ko').text
                translated_data.append([attribute_translated, value_translated])

            # 번역된 데이터로 새로운 데이터프레임 생성
            translated_df = pd.DataFrame(translated_data, columns=["제품정보", "내용"])

            # 번역된 데이터를 HTML 테이블로 변환
            html_table = translated_df.to_html(index=False, header=True, escape=False)

            # 스타일 추가
            html_table = html_table.replace(
                '<table border="1" class="dataframe">',
                '<table border="1" class="dataframe" style="width: 100%; border-collapse: collapse; margin-top: 20px;">'
            ).replace(
                '<th>',
                '<th style="text-align: left; padding: 8px; background-color: #f4f4f4; border: 1px solid #ddd;">'
            ).replace(
                '<td>',
                '<td style="padding: 8px; border: 1px solid #ddd;">'
            )
            # HTML 테이블 출력
            print(f"--- 만들어진 테이블: {html_table}")
        
        except NoSuchElementException:
            print("--- 불렛형/테이블형 등록정보 모두 없음")
            # 예외 처리나 추가 로직을 여기에 작성할 수 있습니다.
        except Exception as e:
            print(f"--- 기타 예외 발생: {e}")
            html_table = ""

    # 가격
    try:
        price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole')))
        print("제품 가격: ", price.text)
    except AttributeError:
        print("제품 가격 가져오기 실패")
    except Exception as e:
        print(f"제품 가격 가져오기 실패: {e}")

    try:
        # 첫 번째 이미지 경로
        xpath = '//*[@id="imgTagWrapperId"]' 
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element.click()
        
        # 첫 번째 이미지 저장
        img_wrapper = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ivLargeImage"]/img')))
        img_url = img_wrapper.get_attribute('src')
        img_data = requests.get(img_url).content
        with open('downloaded_image_0.jpg', 'wb') as handler:
            handler.write(img_data)

        print("이미지가 성공적으로 다운로드되었습니다: downloaded_image_0.jpg")
        img_path.append('downloaded_image_0.jpg')

        # 대표이미지는 크기를 1000x1000으로 변경해 줌
        # 이미지 파일 경로
        input_image_path = "downloaded_image_0.jpg"

        # 이미지 열기
        image = Image.open(input_image_path)

        # 이미지의 원본 크기와 목표 크기
        original_size = image.size
        target_size = (1000, 1000)

        # 원본 이미지 비율을 유지하며 리사이즈
        image.thumbnail(target_size, Image.Resampling.LANCZOS)

        # 새로운 캔버스 생성 (배경 흰색)
        background = Image.new("RGB", target_size, (255, 255, 255))

        # 이미지 중앙에 배치
        image_position = (
            (target_size[0] - image.size[0]) // 2,
            (target_size[1] - image.size[1]) // 2
        )
        background.paste(image, image_position)

        # 원본 파일명과 동일한 이름으로 저장하기 위한 경로 설정
        base_name = os.path.basename(input_image_path)
        file_name, _ = os.path.splitext(base_name)
        output_image_path_with_bg = 'downloaded_image_0.jpg'

        # 결과 저장
        background.save(output_image_path_with_bg)

        # 추가 이미지 있는 경우 모두 저장
        start_index = 1
        end_index = 10
        for i in range(start_index, end_index):
            xpath = f'//*[@id="ivImage_{i}"]/div'
            
            try:
                driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                print("모든 이미지 저장 완료")
                break
            except Exception as e:
                print(f"처리할 이미지가 더 이상 없음: {e}")
                break
            
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()

            img_wrapper = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ivLargeImage"]/img')))
            img_url = img_wrapper.get_attribute('src')
            img_data = requests.get(img_url).content
            with open(f'downloaded_image_{i}.jpg', 'wb') as handler:
                handler.write(img_data)

            print(f"이미지가 성공적으로 다운로드되었습니다: downloaded_image_{i}.jpg")
            img_path.append(f'downloaded_image_{i}.jpg')
        
    finally:
        # 각 행의 데이터를 딕셔너리로 저장
        data = {
            'title': title.text,
            'desc': desc.text,
            'html_table': html_table,
            'price': price.text,
            'img_path': img_path
        }
        driver.quit()

    return (data)
