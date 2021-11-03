import os
import datetime
import pandas as pd
import xlrd
import openpyxl
import glob
from datetime import datetime
from shutil import rmtree

def saybebe_convert():
    ## 다운로드폴더 및 파일 전부 삭제 후 폴더 재생성
    rmtree("downloadxls")
    os.mkdir("downloadxls")

    # 현재날짜 가져오기
    dt_now = datetime.now()
    today = dt_now.date().strftime("%Y%m%d")

    df = pd.DataFrame()
    # 업로드폴더에 존재하는 모든 엑셀파일 읽기 (근데 할 때마다 삭제해서 결국 파일 하나만 존재하게 할 것)
    for f in glob.glob("./uploadxls/*.xlsx"):
        df = pd.read_excel(f,sheet_name=0)
    # df = pd.concat(df, ignore_index=True)
    # df.loc[''] = [3,3289764, 123423535, "차민지", "차민지", "070-7730-4265","010-2214-0554","주소주소1","도로명주소","[옵션1:[서울우유] 서울피자관 토마토치즈 수제 화덕피자 380g 1개]",1,0,0,0,0,0,0,0,0]

    # 반복문을 돌리기 위해 데이터프레임의 '행' 수를 end에 저장
    end = len(df)

    # 변환결과 데이터를 df_res에 저장하기 위해 우선 기존데이터로 df_res를 초기화
    df_res = df
    # print(end)

    # 엑셀에서 읽어서 생성한 데이터프레임을 한 행씩 가져와서 옵션의 긴 문자열을 [** 라는 구분자를 이용해서 자르고 리스트에서 하나씩 꺼내어 별도 행으로 추가한 뒤 원래 행을 삭제
    for i in range(end):
        # print(i)
        options = df.loc[i,'옵션'].split('[**')
        options.pop(0)
        # print(options)
        
        # 가격정보를 첫번째 복사될 때만 원래 값으로 넣고, 나머지는 0으로 넣기 위해 변수 설정
        sq = 0
        for option in options:
            if sq == 0:
                price = df.loc[i,"결제가격"]
            else:
                price = 0

            new_data = {
            "번호": df.loc[i,"번호"], "일련번호": df.loc[i,"일련번호"], "주문번호": df.loc[i,"주문번호"], "주문자명":df.loc[i,"주문자명"],
            "받는분이름":df.loc[i,"받는분이름"],"받는분전화번호":df.loc[i,"받는분전화번호"],"받는분핸드폰":df.loc[i,"받는분핸드폰"],
            "우편번호":df.loc[i,"우편번호"],"(구)지번주소":df.loc[i,"(구)지번주소"],"(신)도로명주소":df.loc[i,"(신)도로명주소"],"주문일자":df.loc[i,"주문일자"],
            "상품번호":df.loc[i,"상품번호"],"상품명":df.loc[i,"상품명"],"옵션":option,"수량":df.loc[i,"수량"],"배송메세지":df.loc[i,"배송메세지"],
            "결제가격":price,"배송코드":df.loc[i,"배송코드"],"송장번호":df.loc[i,"송장번호"]
            }
            sq = sq + 1
            df_res = df_res.append(new_data, ignore_index=True)
            
    ### 옵션별로 분리하여 전부 행추가해주었으니 기존 데이터들은 삭제
    df_res = df_res.drop(df_res.index[0:end])

    # print(df_res)
    # 다운로드 폴더에 저장
    filepath = './downloadxls/saybebe_goods_order' + today + '.xlsx'
    df_res.to_excel(filepath,index=False)

    ## 업로드폴더 및 파일 전부 삭제 후 폴더 재생성
    rmtree("uploadxls")
    os.mkdir("uploadxls")


# exit()


