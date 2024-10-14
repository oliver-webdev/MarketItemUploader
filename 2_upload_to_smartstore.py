import pandas as pd

from datetime import datetime
from coupang_upload_post import upload_to_coupang
from smartstore_upload_post import upload_to_smartstore

# 엑셀 파일 경로
file_path = 'product_upload_data.xlsx'

# 엑셀 파일 읽기
df = pd.read_excel(file_path, sheet_name='Sheet1')

# E~AD 열의 제목 가져오기
columns = df.columns[4:30]  # E(5)~AD(30)열

# E~AD 열의 데이터 가져오기 (두 번째 행부터)
data = df.iloc[:, 4:30]

# 각 행의 데이터를 딕셔너리로 변환하여 리스트로 저장
data_list = data.apply(lambda row: dict(zip(columns, row)), axis=1).tolist()

"""
************** 행 데이터(각 상품) 건별 반복 전송
"""
for index, item in enumerate(data_list):
   img_url = data_list[index].get('img_url')
   prd_nm = data_list[index].get('prd_nm')
   cat_id = data_list[index].get('cat_id')
   cat_id_coupang = data_list[index].get('cat_id_coupang')
   price_n = data_list[index].get('price_naver') # 일단 사용하지 않음
   price_c = data_list[index].get('price_etc') # 판매가
   price_dc = data_list[index].get('price_dc') # 판매가 - 네이버판매용가격(price_n)
   desc = data_list[index].get('desc')
   desc_fix = data_list[index].get('desc_fix')
   brand = data_list[index].get('brand')
   maker = data_list[index].get('maker')
   tag_naver = data_list[index].get('tag_naver')
   meta_naver = data_list[index].get('meta_naver')
   tag_coupang = data_list[index].get('tag_coupang')
   attr_type_1_code = data_list[index].get('attr_type_1_code')
   attr_type_2_code = data_list[index].get('attr_type_2_code')
   attr_theme_code = data_list[index].get('attr_theme_code')
   attr_series_code = data_list[index].get('attr_series_code')
   attr_scale_code = data_list[index].get('attr_scale_code')
   attr_act_code = data_list[index].get('attr_act_code')

   # 이미지 URL 정의
   img_notice = ""         # 해외구매대행 안내 이미지
   img_prd = ""            # 상품이미지
   img_delivery_prc = ""   # 배송프로세스 이미지
   img_alert = ""          # 유의사항 이미지
   image_rep = ""          # 대표 이미지
   image_opt = []          # 추가 이미지

   # 이미지 URL 파싱
   img_url_list = img_url.split(',')
   for idx, img_one in enumerate(img_url_list):
      # 해외구매대행 안내 이미지
      if idx == 0:
         img_notice = f"""
   <div style="text-align: center; margin-bottom: 20px;">
   <img src="{img_one}" alt="제품 이미지" style="width: 100%; max-width: 860px; height: auto;">
   </div>
   """
         continue
      # 배송프로세스 이미지
      if idx == 1:
         img_delivery_prc = f"""
   <div style="text-align: center; margin-bottom: 20px;">
   <img src="{img_one}" alt="제품 이미지" style="width: 100%; max-width: 860px; height: auto;">
   </div>
   """
         continue
      # 유의사항 이미지
      if idx == 2:
         img_alert = f"""
   <div style="text-align: center; margin-bottom: 20px;">
   <img src="{img_one}" alt="제품 이미지" style="width: 100%; max-width: 860px; height: auto;">
   </div>
   """
         continue
      # 상품이미지 (3번째 인덱스부터 모두)
      img_prd = img_prd + f"""
   <div style="text-align: center; margin-bottom: 20px;">
   <img src="{img_one}" alt="제품 이미지" style="width: 100%; max-width: 860px; height: auto;">
   </div>
   """
      if idx == 3:
         # 대표이미지로 저장
         image_rep = img_one
      if idx >= 4:
         image_opt.append(img_one)

   n_img_list = [{'url': item_url} for item_url in image_opt]

   # 쿠팡 이미지 파라미터
   c_img_list = []
   # URL 리스트를 순회하며 딕셔너리 리스트를 생성
   for i, url_detail in enumerate(img_url_list):
      if i < 3:
         continue

      # imageOrder가 0이면 imageType은 'REPRESENTATION', 아니면 'DETAIL'
      image_type = "REPRESENTATION" if i == 3 else "DETAIL"
      image_path = img_url_list[i]
    
      # 딕셔너리 생성
      image_dict = {
         "imageOrder": i - 3,
         "imageType": image_type,
         "vendorPath": image_path
      }
    
      # 딕셔너리를 리스트에 추가
      c_img_list.append(image_dict)
   
   # 상세페이지를 HTML로 작성
   detail = f"""
   <div style="max-width: 860px; margin: 0 auto; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
   {img_notice}
   {img_prd}
   {desc}
   {desc_fix}
   {img_delivery_prc}
   {img_alert}
   </div>
   """
   # 네이버 태그 파싱
   text_list = tag_naver.split(',')

   # 파싱한 태그 리스트
   tag_list = [{"text": item} for item in text_list]
   
   # 쿠팡 검색어 리스트
   tag_coupang_list = tag_coupang.split(',')

   # 상품속성
   attr_list = [
      {
         "attributeSeq": 10025355,
         "attributeValueSeq": attr_type_1_code
      },
      {
         "attributeSeq": 10025355,
         "attributeValueSeq": attr_type_2_code
      },
      {
         "attributeSeq": 10014736,
         "attributeValueSeq": attr_theme_code
      },
      {
         "attributeSeq": 10014737,
         "attributeValueSeq": attr_series_code
      },
      {
         "attributeSeq": 10025374,
         "attributeValueSeq": attr_scale_code
      },
      {
         "attributeSeq": 10025384,
         "attributeValueSeq": attr_act_code
      }
   ]
   # 피규어 카테고리가 아니라면 속성 리스트는 빈 값 (임시방편)
   if cat_id != 50007028:
      attr_list = []

   # [스마트스토어]상품 등록 파라미터 작성
   payload = {
      "originProduct":{
         "statusType":"SALE",
         "saleType":"NEW",
         "leafCategoryId":cat_id,
         "name":prd_nm,
         "detailContent":detail,
         "images":{
            "representativeImage":{
               "url":img_url_list[3]
            },
            "optionalImages":n_img_list
         },
         "salePrice":price_c,
         "stockQuantity":20,
         "deliveryInfo":{
            "deliveryType":"DELIVERY",
            "deliveryAttributeType":"NORMAL",
            "deliveryCompany":"EPOST",
            "deliveryBundleGroupUsable":True,
            "deliveryBundleGroupId":54040354,
            "deliveryFee":{
               "deliveryFeeType":"FREE",
               "baseFee":0
            },
            "claimDeliveryInfo":{
               "returnDeliveryCompanyPriorityType":"PRIMARY",
               "returnDeliveryFee":12000,
               "exchangeDeliveryFee":12000,
               "shippingAddressId":106173292,
               "returnAddressId":106438111,
               "freeReturnInsuranceYn":False
            },
            "installationFee":False,
            "businessCustomsClearanceSaleYn":False
         },
         "detailAttribute":{
            "naverShoppingSearchInfo":{
               "manufacturerName":maker,
               "brandName":brand
            },
            "afterServiceInfo":{
               "afterServiceTelephoneNumber":"0507-0178-2551",
               "afterServiceGuideContent":"평일 10시~17시\n토요일 10시~14시\n문자, 전화 문의 가능합니다."
            },
            "purchaseQuantityInfo":{
               "maxPurchaseQuantityPerId":1
            },
            "originAreaInfo":{
               "originAreaCode":"0200036",
               "importer":"구매대행",
               "content":"일본산(구매대행)",
               "plural":False
            },
            "purchaseReviewInfo":{
               "purchaseReviewExposure":True
            },
            "eventPhraseCont":"구매 금액 1% 포인트 적립 / 리뷰 작성 시 최대 600 포인트 적립",
            "taxType":"TAX",
            "certificationTargetExcludeContent":{
               "kcExemptionType":"OVERSEAS",
               "kcCertifiedProductExclusionYn":"KC_EXEMPTION_OBJECT"
            },
            "sellerCommentUsable":False,
            "minorPurchasable":True,
            "productInfoProvidedNotice":{
               "productInfoProvidedNoticeType":"ETC",
               "etc":{
                  "returnCostReason":"상품 상세설명 참조",
                  "noRefundReason":"상품 상세설명 참조",
                  "qualityAssuranceStandard":"상품 상세설명 참조",
                  "compensationProcedure":"상품 상세설명 참조",
                  "troubleShootingContents":"상품 상세설명 참조",
                  "itemName":"상품 상세설명 참조",
                  "modelName":"상품 상세설명 참조",
                  "certificateDetails":"상품 상세설명 참조",
                  "manufacturer":"상품 상세설명 참조",
                  "customerServicePhoneNumber":"상품 상세설명 참조"
               }
            },
            "productAttributes":attr_list,
            "seoInfo":{
               "metaDescription":meta_naver,
               "sellerTags":tag_list
            }
         },
         "customerBenefit":{
            "immediateDiscountPolicy":{
               "discountMethod":{
                  "value":price_dc,
                  "unitType":"WON"
               }
            },
            "purchasePointPolicy":{
               "value":1,
               "unitType":"PERCENT"
            },
            "reviewPointPolicy":{
               "textReviewPoint":150,
               "photoVideoReviewPoint":150,
               "afterUseTextReviewPoint":150,
               "afterUsePhotoVideoReviewPoint":150
            }
         }
      },
      "smartstoreChannelProduct":{
         "storeKeepExclusiveProduct":False,
         "naverShoppingRegistration":True,
         "channelProductDisplayStatusType":"ON"
      }
   }

   # print(f"--- 전송할 JSON: {payload}")
   
   # [쿠팡]상품 등록 파라미터 작성
   json_data = {
      "displayCategoryCode": cat_id_coupang,
      "sellerProductName": prd_nm,
      "vendorId": "A01010365",
      "saleStartedAt": datetime.now().replace(microsecond=0).isoformat(),
      "saleEndedAt": "2099-01-01T23:59:59",
   #    "displayProductName":"해피바스 솝베리 클렌징 오일",
      "brand": brand,
   #    "generalProductName":"솝베리 클렌징 오일",
   #    "productGroup":"클렌징 오일",
      "deliveryMethod":"AGENT_BUY",
      "deliveryCompanyCode":"EPOST",
      "deliveryChargeType":"FREE",
      "deliveryCharge":0,
      "freeShipOverAmount":0,
      "deliveryChargeOnReturn": 12000,
      "remoteAreaDeliverable":"Y",
      "unionDeliveryType":"NOT_UNION_DELIVERY",
      "returnCenterCode":"1001734209",
      "returnChargeName":"신촌 오피스",
      "companyContactNumber":"0507-0178-2551",
      "returnZipCode":"04058",
      "returnAddress":"서울특별시 마포구 서강로 133",
      "returnAddressDetail":"병우빌딩 815호",
      "returnCharge": 12000,
      "outboundShippingPlaceCode":19652131,
      "vendorUserId":"jcthemax",
      "requested": True,
      "items":[
         {
            "itemName": "단일상품",
            "originalPrice": price_c,
            "salePrice": price_c,
            "maximumBuyCount": "20",
            "maximumBuyForPerson": "1",
            "outboundShippingTimeDay": "2",
            "maximumBuyForPersonPeriod": "1",
            "unitCount":1,
            "adultOnly":"EVERYONE",
            "taxType":"TAX",
            "parallelImported":"NOT_PARALLEL_IMPORTED",
            "overseasPurchased":"OVERSEAS_PURCHASED",
            "pccNeeded": True,
         #  "externalVendorSku":"P00000GH000A",
         #  "barcode":"",
         #  "emptyBarcode":true,
         #  "emptyBarcodeReason":"상품확인불가_바코드없음사유",
         #  "modelNo":"1717171",
         #  "extraProperties":null,
         #  "certifications":[
         #     {
         #        "certificationType":"NOT_REQUIRED",
         #        "certificationCode":""
         #     }
         #  ],
            "searchTags": tag_coupang_list,
            "images": c_img_list,
            "notices":[
               {
                  "noticeCategoryName":"기타 재화",
                  "noticeCategoryDetailName":"품명 및 모델명",
                  "content":"상세페이지 참조"
               },
               {
                  "noticeCategoryName":"기타 재화",
                  "noticeCategoryDetailName":"인증/허가 사항",
                  "content":"상세페이지 참조"
               },
               {
                  "noticeCategoryName":"기타 재화",
                  "noticeCategoryDetailName":"제조국(원산지)",
                  "content":"상세페이지 참조"
               },
               {
                  "noticeCategoryName":"기타 재화",
                  "noticeCategoryDetailName":"제조자(수입자)",
                  "content":"상세페이지 참조"
               },
               {
                  "noticeCategoryName":"기타 재화",
                  "noticeCategoryDetailName":"소비자상담 관련 전화번호",
                  "content":"상세페이지 참조"
               }
            ],
            "attributes":[
               # {
               #    "attributeTypeName":"피규어 형태",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"피규어 종류",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"피규어 캐릭터",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"출시/발매 년도",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"피규어 제작방식",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"최소 연령",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"스케일",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"높이",
               #    "attributeValueName":""
               # },
               # {
               #    "attributeTypeName":"세트여부",
               #    "attributeValueName":""
               # }
            ],
            "contents":[
               {
                  "contentsType":"TEXT",
                  "contentDetails":[
                     {
                        "content": detail,
                        "detailType":"TEXT"
                     }
                  ]
               }
            ]
         }
      ],
      "manufacture":maker
   }

   # print(payload)
   """
   ----- 스마트스토어 전송 -----
   """
   try:
      upload_to_smartstore(payload)
   except Exception as e:
      print(f"--- 스마트스토어 업로드 에러: {e}")

   """
   ----- 쿠팡 전송 -----
   """
   try:
      upload_to_coupang(json_data)
   except Exception as e:
      print(f"--- 쿠팡 업로드 에러: {e}")

# 상품 업로드 끝