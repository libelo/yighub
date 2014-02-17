# -*- coding:utf-8 -*-

# 처음으로 인터넷 크롤링을 시도하였으며, 정규식을 좀 더 알게 되었다.

import requests
import re
from decimal import getcontext, Decimal

def betting_list_now():

	getcontext().prec = 3

	betting_list = [ # 이름을 지정하는 명확성을 잃는 대신 간결성을 얻었다. 다른 사람이 처음 보고 이해하기는 좀 더 어렵지만 정보를 더 깔끔하게 제시할 수 있다.
			['Senior', '박종욱', '기아차', '000270', 'kse', 54000],
			['Senior', '조용래', 'SK하이닉스', '000660', 'kse', 37850],
			['Senior', '김영길', '삼진제약', '005500', 'kse', 16400],
			['Senior', '윤을정', '한스바이오메드', '042520', 'kosdaq', 17900],
			['Senior', '여준영', '윈스테크넷', '136540', 'kosdaq', 15200],
			['Senior', '조상현', 'KC코트렐', '119650', 'kse', 9220],
			['Senior', '이희건', 'KT', '030200', 'kse', 30800],

			['Acting', '노경탁', '대덕GDS', '004130', 'kse', 16050],
			['Acting', '박진한', '한진칼', '180640', 'kse', 23250],
			['Acting', '김선경', 'LG패션', '093050', 'kse', 29300],
			['Acting', '장육유', '웅진씽크빅', '095720', 'kse', 6950],
			['Acting', '이원기', 'LG생활건강우', '051905', 'kse', 208000],
			['Acting', '정소라', '코나아이', '052400', 'kosdaq', 37600],
			['Acting', '윤태현', '삼성전자', '005930', 'kse', 1280000],

			['Monkeys', 'Monkey1', '디지탈아리아', '115450', 'kosdaq', 2320],
			['Monkeys', 'Monkey2', 'SBI인베스트먼트', '019550', 'kosdaq', 366],
			['Monkeys', 'Monkey3', '내츄럴엔도텍', '168330', 'kosdaq', 59100],
			['Monkeys', 'Monkey4', 'AK홀딩스', '006840', 'kse', 39400],
			['Monkeys', 'Monkey5', 'JW홀딩스', '096760', 'kse', 2475],
			['Monkeys', 'Monkey6', '대상홀딩스', '084690', 'kse', 8070],
			['Monkeys', 'Monkey7', '동아엘텍', '088130', 'kosdaq', 6840],
		]	

	price_reg = re.compile(u'<span class=(?:up|down|hold)color>([\d]+),?([\d]*),?([\d]*)</span>') # 괄호를 쓰지만 결과에 표시하고 싶지 않을 때는 (?:...)을 쓴다.
	diff_reg = re.compile(u'<span class=(?:up|down|hold)color>(.+?)</span>')
	averages = {'Senior': 1, 'Acting': 1, 'YIG': 1, 'Monkeys': 1}

	for row in betting_list:
		stock_code = row[3]
		param = (row[4], row[4], stock_code, ('A' if row[4]=='kse' else 'B'))
		url = 'http://stock.koscom.co.kr/%s_sise/%s_hyun.jsp?code=A%s&market=%s' % param
		r = requests.get(url)
		result = price_reg.findall(r.text)
		diff = diff_reg.findall(r.text)
		# print result
		current_price = int(result[0][0] + result[0][1] + result[0][2])
		difference = (diff[1] if diff[1] != '&nbsp;' else '') + diff[2] + diff[3]
		raw_rate = float(current_price)/float(row[5])-1
		averages[row[0]] *= raw_rate + 1
		# print row[0], averages[row[0]]
		if row[0] == 'Senior' or row[0] == 'Acting': # row[0] == 'Senior' or 'Acting' 이 실수를 조심하자.
			averages['YIG'] *= raw_rate + 1
		rate = Decimal(raw_rate) * 100  # Decimal은 float로 계산이 완료된 후에 덮이는 게 좋다. 그렇지 않으면 끝이 잘려서 계산이 제대로 되지 않는다.

		row.append(current_price)
		row.append(difference)
		row.append(rate)
		# print row[1], row[2], row[4], current_price, rate, url

	averages['Senior'] = Decimal(averages['Senior']**(1.0/7.0) - 1) * 100 # 곱하기 100을 하고 Decimal을 씌우면 소수점 몇십째자리까지 표시됨.
	averages['Acting'] = Decimal(averages['Acting']**(1.0/7.0) - 1) * 100 # 분수를 제곱할 때는 반드시 괄호 치기
	averages['YIG'] = Decimal(averages['YIG']**(1.0/14.0) - 1) * 100 # 1/14 == 0 이기 때문에 소수점을 빼면 0제곱과 같음.
	averages['Monkeys'] = Decimal(averages['Monkeys']**(1.0/7.0) - 1) * 100
	averages = [('Senior', averages['Senior']), ('Acting', averages['Acting']), 
				('YIG', averages['YIG']), ('Monkeys', averages['Monkeys'])]

	betting_list = sorted(betting_list, key = lambda row: row[8], reverse = True)

	return betting_list, averages

if __name__ == "__main__":
	betting_list, averages = betting_list_now()
	print averages