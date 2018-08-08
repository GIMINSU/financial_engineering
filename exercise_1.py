# 함수의 개념

def f(x):
    y = x + 1
    return y

print(f(1))
f2 = f(f(1))
print(f2)

# 외부 library 사용

import bs4
from urllib.request import urlopen
import pandas as pd
# 크롬으로 http://book.finterstellar.com/sample.html 접속
# 페이지 소스 보기
html_doc = '''
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
'''

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')
# BeautifulSoup 함수를 이용해 html_doc을 해석해서 soup에 저장

# tag가 잘 보이도록 prettify 함수를 이용해 HTML 코드를 태그 단위별로 줄바꿈 해서 보여줌
# tag란 HTML 문서의 꼬리표 <html>, <head>, <body> 등을 의미함

print(soup.prettify())
#title tag를 통째로 가져옴
print(soup.title)

# tag까지 필요한게 아니므로 텍스트만 가져오려면 text 함수를 사용한다.
print(soup.title.text)

# 모든 a tag를 가져오려면 find_fall 함수를 써야 함
print(soup.find_all('a'))
'''
tag를 제외하고 이름만 뽑으려고 text 함수를 사용해도(soup.find_all('a').text)
결과가 리스트 형태기 때문에 찾을 수 없음 따라서 리스트의 데이터를 하나하나 읽어서
그 안의 데이터 값을 가져와야 함
'''

member = soup.find_all('a')
for a in member:
    print(a.text)

'''
네이버에서 KOSPI200 지수 수집하기
크롬에서 https://finance.naver.com/sise/sise_index.nhn?code=KPI200 접속
일별시세
일별시세 테이블에서 프레임 소스보기
데이터를 뽑아낼 데이터가 들어있는 웹페이지의 주소 확보
소스보기주소에서 view-source:를 제외한 나머지 부분
주소창에 쳐서 확인
데이터가 어디까지 들어있는지 확인하기 위해 화면 하단 페이지 네비게이션의 맨뒤 버튼을 눌러서 마지막 데이터 확인
https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=520 
ULR에 page라는 인수가 따라붙은 거시 보임
일별시세 ULR은
https://finance.naver.com/sise/sise_index_day.nhn?code=지수코드&page=페이지번호
라는 것을 확인함
'''

index_cd = 'KPI200'
page_n = 1
naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd +'&page=' + str(page_n)

from urllib.request import urlopen
source = urlopen(naver_index).read()
print(source)
# source를 BeautifulSoup를 이용해 lxml로 해석하고 prettify함수로 태그별로 읽음
source = bs4.BeautifulSoup(source, 'lxml')
print(source.prettify())  # error 발생 시 lxml library를 설치해야 함

'''
이 많은 소스 중 어디를 긁어야 원하는 데이터를 뽑을 수 있을까?
긁어야 할 데이터 확인
날짜와 지수를 추출해야 함
네이버는 지수를 '체결가' 필드에 넣어놓음 이 데이터가 해당 날짜의 종가지수
이 데이터가 정확하게 어느 부분에 있는지 알아보는 방법이 있음
일별시세 테이블의 날짜 위에 마우스를 가져가 오른쪽클릭을 하고 나오는 메뉴 중 검사 클릭
Elements tap을 클릭한 후 스크롤바를 위아래로 움직이면 파란색으로 해당 내용이 표시됨
필요한 데이터 중 날짜는 <td class="date">2006.01.03</td> 에 들어 있음
같은 날 종가(체결가에 들어있음) 위에서 오른 클릭 하면 <td class="number_1">178.81</td>에
종가가 들어 있는 것을 확인할 수 있음
필요한 데잍가 모두 <td> tag에 들어 있는 것을 확인했으니 BeautifulSoup를 이용해서
<td> tag를 찾아 안에 들어 있는 데이터를 뽑아 내는 것이 최종 목표임
<td> tag 분석을 시작하기 전에 <td> tag가 몇 개나 있는지 확인
'''
td = source.find_all('td') # <td> tag를 모두 골라내서 td라는 변수에 저장
print(len(td)) # td 개수 확인 54개 나옴

'''
일일이 눈으로 확인하기에 너무 많아서 다른 방법을 찾아야 함
데이터를 대량으로 제공하는 사이트에서 원하는 데이터의 위치를 찾아낼 때 XPath 주소를 사용
Xpath(XML Path Language)란 엡사이트 또는 XML 문서에 있는 작은 항목의 주소를 문서에 포함된 태그를 조합한 경로 형태로 
표현하는 언어
크롬 브라우저에서 데이터의 XPath를 확인하는 방법
스크린의 우측에서 음영으로 선택된 부분에 마우스를 갖다댄 후
오른쪽 클릭을 하면 나오는 메뉴 중 Copy를 선택한 후
Copy XPath를 클릭
XPath 주소가 나타남
/html/body/div/table[1]/tbody/tr[3]/td[1]
앞에서부터 /(슬래시) 단위로 html->body->div->table(첫번째)->tr(세번째)->td(첫번째)를 차례대로 찾아가라
XPath 상의 tbody는 실제 코드상에 있는 것이 아니라 여기에서부터 테이블의 내용이 시작된다고 표시해주는 것이므로
tbody를 제외한 나머지를 찾으며 따라가보면 원하는 데이터에 도달하게 됨
찾아가는 방법은 찾는 값이 하나일 경우에는 find(tag명), 여러 개일 경우에는 find_all(tag명)[순서]를 이용함
python은 숫자르 0부터 세기 때문에 XPath 수에서 -1을 해줘야 함
XPath를 python code로 표현
'''
# /html/body/div/table[1]/tbody/tr[3]/td[1]
print(source.find_all('table')[0].find_all('tr')[2].find_all('td')[0])
'''
'<td class = "date"> 처럼 class 이름을 이용해 특별히 이름을 붙인 td tag는 이름을 지정해서 뽑아낼 수 있음
이렇게 할 경우 td앞에 붙는 tag를 생략할 수 있어서 유용함
'''
d = source.find_all('td', class_='date')[0].text
print(d)
# 원하는 날짜를 찾기는 했으나 날짜 형식이 python의 날짜형식과 다름
# python이 날짜로 인식할 수 있도록 형식을 바꿔줌 datetime 함수를 이용함

import datetime as dt
# 문자열.split(구분자) 함수를 이용해 구분자를 기준으로 문자열을 년,월,일로 분해함
# 분해한 문자열은 dt.date(년, 월, 일) 함수를 이용해 날짜 형식으로 바꿔서 this_date 함수에 저장함
yyyy = int(d.split('.')[0])
mm = int(d.split('.')[1])
dd = int(d.split('.')[2])
this_date = dt.date(yyyy, mm, dd)
print(type(d))
print(this_date)
print(type(this_date))
# 읽어온 날짜 정보를 date 형식으로 바꿀 일이 계속 생기므로 이 기능을 date_format() 함수로 정의해준다
def date_format(d):
    d = str(d).replace('-', '.')
    yyyy = int(d.split('.')[0])
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])
    this_date = dt.date(yyyy, mm, dd)
    return this_date

# 2행에 d = str(d).replace('-', '.')는 날짜 구분자가 .이 아닌 -로 되어 있는 경우 .으로 변환해주는 기능임

'''
이제 지수를 가져온다.
해당 일자의 종가지수를 가져옴
종가를 가리키는 XPath를 구해보면
/html/body/div/table[1]/tbody/tr[3]/td[2]
종가를 가져올 때는 받아온 데이터를 숫자로 인식되도록 처리하기 위해 숫자의 천의 자리를 표시하는 쉼표(,)를 제거하는 작업이 필요함
replace() 함수를 이용해 쉼표 제거
'''
this_close = source.find_all('tr')[2].find_all('td')[1].text
this_close = this_close.replace(',','') # 쉼표(,) 제거
this_close = float(this_close) # 숫자로 인식
print(this_close)
# <td class="number_1">178.81</td> 역시 간단하게 변환할 수 있음
p = source.find_all('td', class_='number_1')[0].text
print(p)
# 간단한 코드를 이용해 페이지에 있는 모든 날짜와 가격을 불러옴
dates = source.find_all('td', class_='date')
prices = source.find_all('td', class_ = 'number_1')
print('date and price \n', dates, prices)