# -*- coding:utf-8 -*-

# 처음으로 인터넷 크롤링을 시도하였으며, 정규식을 좀 더 알게 되었다.

import requests
import re
from decimal import getcontext, Decimal

def betting_list_now():

	getcontext().prec = 3

	betting_list = [ # 이름을 지정하는 명확성을 잃는 대신 간결성을 얻었다. 다른 사람이 처음 보고 이해하기는 좀 더 어렵지만 정보를 더 깔끔하게 제시할 수 있다.
			['Senior', '허재성', '오스템임플란트', '048260', 'kosdaq', 21850],
			['Senior', '이충재', '키움증권', '039490', 'kse', 53400],
			['Senior', '북산안선생', '네오위즈인터넷', '104200', 'kosdaq', 11250],
			['Senior', '권용현', '크리스탈지노믹스', '083790', 'kosdaq', 12600],
			['Senior', '박세라', '이마트', '139480', 'kse', 254000],
			['Senior', '박종욱', '동원산업', '006040', 'kse', 337500],
			['Senior', '김영길', '지엠비코리아', '013870', 'kse', 7610],
			['Senior', '하태열', '안국약품', '001540', 'kosdaq', 12500],
			['Senior', '조용래', '대한화섬', '003830', 'kse', 71000],

			['Acting', '김지은', '한샘', '009240', 'kse', 64800],
			['Acting', '박진한', '루트로닉', '085370', 'kosdaq', 13550],
			['Acting', '노경탁', '잉크테크', '049550', 'kosdaq', 19100],
			['Acting', '장육유', '아이센스', '099190', 'kosdaq', 48150],
			['Acting', '이원기', '한국토지신탁', '034830', 'kosdaq', 1755],
			['Acting', '윤태현', '아세아시멘트', '183190', 'kse', 96800],
			['Acting', '김선경', '제이콘텐트리', '036420', 'kosdaq', 3300],
			['Acting', '정소라', 'CJ E&M', '130960', 'kosdaq', 38750],

			['Monkeys', 'Monkey1', '텍셀네트컴', '038540', 'kosdaq', 1265],
			['Monkeys', 'Monkey2', '이니텍', '053350', 'kosdaq', 4200],
			['Monkeys', 'Monkey3', '네패스', '033640', 'kosdaq', 7270],
			['Monkeys', 'Monkey4', '멜파스', '096640', 'kosdaq', 10850],
			['Monkeys', 'Monkey5', '이코리아리츠', '138440', 'kse', 2925],
			['Monkeys', 'Monkey6', '우신시스템', '017370', 'kse', 2515],
			['Monkeys', 'Monkey7', '이필름', '093230', 'kse', 2270],
			['Monkeys', 'Monkey8', '성신양회', '004980', 'kse', 10150],
			['Monkeys', 'Monkey9', '한독', '002390', 'kse', 17000],
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

	averages['Senior'] = Decimal(averages['Senior']**(1.0/9.0) - 1) * 100 # 곱하기 100을 하고 Decimal을 씌우면 소수점 몇십째자리까지 표시됨.
	averages['Acting'] = Decimal(averages['Acting']**(1.0/8.0) - 1) * 100 # 분수를 제곱할 때는 반드시 괄호 치기
	averages['YIG'] = Decimal(averages['YIG']**(1.0/17.0) - 1) * 100 # 1/14 == 0 이기 때문에 소수점을 빼면 0제곱과 같음.
	averages['Monkeys'] = Decimal(averages['Monkeys']**(1.0/9.0) - 1) * 100
	averages = [('Senior', averages['Senior']), ('Acting', averages['Acting']), 
				('YIG', averages['YIG']), ('Monkeys', averages['Monkeys'])]

	betting_list = sorted(betting_list, key = lambda row: row[8], reverse = True)

	return betting_list, averages

if __name__ == "__main__":
	betting_list, averages = betting_list_now()
	print averages