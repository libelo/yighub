# from yig03 to yighub
# -*- coding: utf-8 -*-
import sqlite3

import re
import datetime

from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from yighub.models import User


def extract_one(board_name, no):
	
	with sqlite3.connect('yig03.sqlite') as db:

		cur = db.cursor()

		script = "SELECT * FROM %s WHERE no = %d" % (board_name, no)

		cur.execute(script)
		return cur.fetchone()

def extract_user():

	with sqlite3.connect('yig03.sqlite') as db:

		cur = db.cursor()

		cur.execute("SELECT * FROM zetyx_member_table")

		rows = cur.fetchall()

		return rows

def transform_user():

    rows = extract_user()
    
    for row in rows:
        u = User()
        u.id = row[0]
        u.user_id = row[2]
        u.password = '' #row[3]
        u.name = row[5]
        if row[6] == 9:
            u.level = 'non'
        else:
            u.level = 'reg'
        u.email = row[7]
        s = ''
        if row[8]:
            s += u'홈페이지: ' + row[8]
        if row[10]:
            if row[8]:
                s += ' | '
            s += u'네이트온: ' + row[10] + u' '
        if row[11]:
            if row[8] or row[10]:
                s += ' | '
            s += u'msn: ' + row[11]
        u.sns = s
        u.self_introduction = re.compile(r'\\r\\n').sub("\n", row[13])
        u.point = row[14]*10 + row[15]*3
        regex_p = re.compile(r'\d{3}-\d{3,4}-\d{4}')
        if row[22]:
            if regex_p.match(row[22]):
                u.phone_number = row[22]
            elif re.compile(r'\d{3} \d{3,4} \d{4}').match(row[22]):
                u.phone_number = '-'.join(row[22].split(' '))
            elif re.compile(r'(\d|-)+').match(row[22]):
                digits = ''.join(row[22].split('-'))
                u.phone_number = row[22][:3] + u'-' + row[22][3:7] + u'-' + row[22][7:]
            else:
                assert len(row[22]) == 11
                u.phone_number = row[22][:3] + u'-' + row[22][3:7] + u'-' + row[22][7:]
        if row[24]:
            u.birthday = datetime.datetime.fromtimestamp(row[24]).strftime('%Y-%m-%d')
        u.date_joined = datetime.datetime.fromtimestamp(row[26]).strftime('%Y-%m-%d')
        if row[45]:
            u.last_login = datetime.datetime.fromtimestamp(row[45]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            u.last_login = timezone.now()
        f03 = None
        if row[25]:
            try:
                f03 = open(u'/Users/libelo/documents/code/yig03/yig03_20130204/public_html/zero/' + row[25])
            except IOError:
                pass # db와 파일이 최신으로 업데이트되면 이것도 처리한다.
            else:
                u.avatar = ImageFile(f03)
        u.save()

        if f03:
            f03.close()

