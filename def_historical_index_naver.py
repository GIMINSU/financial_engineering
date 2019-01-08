import bs4
from urllib.request import urlopen
import pandas as pd
import datetime as dt

# 읽어온 날짜 정보를 date 형식으로 바꿀 일이 계속 생기므로 이 기능을 date_format() 함수로 정의해준다
def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy, mm, dd)
    return this_date

# # 데이터 추출 기능을 함수로 만들기
# def historical_index_naver(index_cd, start_date='', end_date='', page_n=1, last_page=0):
#
#     if start_date:
#         start_date = date_format(start_date)
#     else:
#         start_date = dt.date.today()
#     if end_date:
#         end_date = date_format(end_date)
#     else:
#         end_date = dt.date.today()
#
#     naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)
#
#     source = urlopen(naver_index).read() # 지정한 페이지에서 코드 읽기
#     source = bs4.BeautifulSoup(source, 'lxml') # BeautifulSoup를 이용해 tag별로 code 분류
#
#     dates = source.find_all('td', class_='date') # <td class="date"> tag에서 날짜 수집
#     prices = source.find_all('td', class_='number_1') # <td class="number_1> tag에서 지수 수집
#     historical_prices = dict()
#     for n in range(len(dates)):
#
#         if dates[n].text.split('.')[0].isdigit():
#
#             # 날짜 처리
#             this_date = dates[n].text
#             this_date=date_format(this_date)
#
#             if this_date <= end_date and this_date >= start_date:
#             # start_date와 end_date 사이에서 데이터 저장
#                 # 종가처리
#                 this_close = prices[n*4].text # price 중 종가지수인 0, 4, 8... 번째 데이터 추출
#                 this_close = this_close.replace(',', '')
#                 this_close = float(this_close)
#
#                 # dictionary에 저장
#                 if this_date not in historical_prices:
#                     historical_prices[this_date] = this_close
#             elif this_date < start_date:
#                 return historical_prices
#
#         # 페이지 네비게이션
#         if last_page == 0:
#             last_page= source.find('td', class_='pgRR').find('a')['href']
#             # 마지막 페이지 주소 추출
#             last_page = last_page.split('&')[1]
#             last_page = last_page.split('=')[1]
#             last_page = int(last_page)
#
#         # 다음 페이지 호출
#         if page_n < last_page:
#             page_n = page_n +1
#             historical_index_naver(index_cd, start_date, end_date, page_n, last_page)
#         return historical_prices


# git 복사해온 코드
historical_prices = dict()
def historical_index_naver(index_cd, start_date, end_date, page_n=1, last_page=0):
    if start_date:  # start_date가 있으면
        start_date = date_format(start_date)  # date 포맷으로 변환
    else:  # 없으면
        start_date = dt.date.today()  # 오늘 날짜를 지정
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()

    naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

    source = urlopen(naver_index).read()  # 지정한 페이지에서 코드 읽기
    source = bs4.BeautifulSoup(source, 'lxml')  # 뷰티풀 스프로 태그별로 코드 분류

    dates = source.find_all('td', class_='date')  # <td class="date">태그에서 날짜 수집
    prices = source.find_all('td', class_='number_1')  # <td class="number_1">태그에서 지수 수집

    for n in range(len(dates)):

        if dates[n].text.split('.')[0].isdigit():

            # 날짜 처리
            this_date = dates[n].text
            this_date = date_format(this_date)

            if this_date <= end_date and this_date >= start_date:
                # start_date와 end_date 사이에서 데이터 저장
                # 종가 처리
                this_close = prices[n * 4].text  # prices 중 종가지수인 0,4,8,...번째 데이터 추출
                this_close = this_close.replace(',', '')
                this_close = float(this_close)

                # 딕셔너리에 저장
                historical_prices[this_date] = this_close

            elif this_date < start_date:
                # start_date 이전이면 함수 종료
                return historical_prices

                # 페이지 네비게이션
    if last_page == 0:
        last_page = source.find('td', class_='pgRR').find('a')['href']
        # 마지막페이지 주소 추출
        last_page = last_page.split('&')[1]  # & 뒤의 page=506 부분 추출
        last_page = last_page.split('=')[1]  # = 뒤의 페이지번호만 추출
        last_page = int(last_page)  # 숫자형 변수로 변환

    # 다음 페이지 호출
    if page_n < last_page:
        page_n = page_n + 1
        historical_index_naver(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices

index_cd = 'KPI200'
historical_index_naver(index_cd, '2019-1-2', '2019-1-8')
print(historical_prices)