from bs4 import BeautifulSoup
import datetime as dt

html_doc = """
<html><head><title>The Office</title></head>
<body>
<p class="title"><b>The Office</b></p>
<p class="story">In my office, there are four officers,
<a href="http://example.com/YW" class="member">YW</a>,
<a href="http://example.com/JK" class="member">JK</a>,
<a href="http://example.com/YJ" class="member">YJ</a> and
<a href="http://example.com/KS" class="member">KS</a>
.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.prettify())
print('title tag를 통째로 가져옴\n', soup.title)
print('title tag 내용을 추출\n', soup.title.text)
print('a tag를 통째로 가져옴\n', soup.a)
print('a tag를 모두 가져옴\n', soup.find_all('a'))
print('3번째 팀원 이름 가져오기\n', soup.find_all('a')[2])

member = soup.find_all('a')
for m in member:
    print(m.text)

index_cd = 'KPI200'
page_n = 1
naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)

from urllib.request import urlopen
source = urlopen(naver_index).read()

# print(source)

source = BeautifulSoup(source, 'lxml')
# print(source.prettify())
td = source.find_all('td')
print('td의 개수 확인', len(td))

print('날짜 들어있는 테이블 확인', source.find_all('table')[0].find_all('tr')[2].find_all('td')[0])
d = source.find_all('td', class_='date')[0].text
print(d)

yyyy= int(d.split('.')[0])
mm = int(d.split('.')[1])
dd = int(d.split('.')[2])
this_date = dt.date(yyyy, mm, dd)

def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])

    this_date = dt.date(yyyy, mm, dd)
    return this_date

this_close = source.find_all('tr')[2].find_all('td')[1].text
print(this_close)
this_close = this_close.replace(',', '')
this_close = float(this_close)
print(this_close)

p = source.find_all('td', class_='number_1')[0].text
print(p)

dates = source.find_all('td', class_='date')
prices = source.find_all('td', class_='number_1')

print(len(dates))
print(len(prices))

for n in range(len(dates)):
    this_date = dates[n].text
    this_date = date_format(this_date)

    this_close = prices[n*4].text
    this_close = this_close.replace(',', '')
    this_close = float(this_close)

paging = source.find('td', class_='pgRR').find('a')['href']

paging = paging.split('&')[1]
paging = paging.split('=')[1]

last_page = source.find('td', class_='pgRR').find('a')['href']
last_page = last_page.split('&')[1]
last_page = last_page.split('=')[1]
last_page = int(last_page)
print(last_page)