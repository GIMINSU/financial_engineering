import bs4
from urllib.request import urlopen
import pandas as pd
import datetime as dt

url = 'http://finance.daum.net/global/index_daily.daum?type=default&ric=/.GSPC&page=1'
source = urlopen(url).read()
source = bs4.BeautifulSoup(source, 'lxml')
# print(source)

dates = source.find_all('td', class_='datetime')
print(dates)
prices = source.find_all('td', class_='num')
print("dates's length : %s" %len(dates))
print("prices's length : ", len(prices))

print('prices의 첫 번째 요인 : \n', prices[0].text)


# 저자 github 코드 복사

def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy, mm, dd)
    return this_date

historical_prices = dict()
def historical_global_daum(index_cd, start_date='', end_date='', page_n=1, last_page=0):
    if start_date:  # start_date가 있으면
        start_date = date_format(start_date)  # date 포맷으로 변환
    else:  # 없으면
        start_date = dt.date.today()  # 오늘 날짜를 지정
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()

    url = 'http://finance.daum.net/global/index_daily.daum?type=default&ric=/.' + index_cd + '&page=' + str(page_n)

    source = urlopen(url).read()
    source = bs4.BeautifulSoup(source, 'lxml')

    dates = source.find_all('td', class_='datetime')  # <td class="datetime">태그에서 날짜 수집
    prices = source.find_all('td', class_='num')  # <td class="num">태그에서 날짜 수집

    rows_in_page = len(dates)

    if len(dates) > 0:

        for n in range(rows_in_page):

            # 날짜 처리
            this_date = dates[n].text
            this_date = date_format(this_date)

            if this_date <= end_date and this_date >= start_date:
                # start_date와 end_date 사이에서 데이터 저장
                # 종가 처리
                this_close = prices[n * 3].text
                this_close = this_close.replace(' ', '')
                this_close = this_close.replace('\t', '')
                this_close = this_close.replace('\n', '')
                this_close = this_close.replace(',', '')
                this_close = float(this_close)

                # 딕셔너리에 저장
                historical_prices[this_date] = this_close

            elif this_date < start_date:
                # start_date 이전이면 함수 종료
                return historical_prices
                # 페이지 네비게이션
        if rows_in_page == 10:
            page_n = int(page_n)
            page_n = page_n + 1

            historical_global_daum(index_cd, start_date, end_date, page_n, last_page)

    return historical_prices

daum = historical_global_daum('GSPC', '2018-4-1', '2018-4-5')
print("추출된 결과물 : \n", daum)

