# from yig03 to yighub
# -*- coding: utf-8 -*-
import sqlite3

import re
import datetime

from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone

from yighub.models import User
from yighub.models import Entry
from yighub.models import BulletinBoard, BulletinEntry, BulletinThumbnail, BulletinFile, BulletinComment


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
            u.last_login = datetime.datetime.fromtimestamp(row[26]).strftime('%Y-%m-%d %H:%M:%S')
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


def transform_analysis():

    with sqlite3.connect('yig03.sqlite') as db:

        cur = db.cursor()

        cur.execute("SELECT * FROM zetyx_board_analysis")

        rows = cur.fetchall()

        row = rows[400]

        b = BulletinBoard.objects.get(name = 'Company Analysis')

        e = BulletinEntry()
        e.board = b

        e.arrangement = 1000

        e.depth = row[4]
        e.title = row[17]
        e.content = re.compile(r'\\r\\n').sub("\n", row[11])
        e.creator = User.objects.get(pk = row[9])
        e.time_created = datetime.datetime.fromtimestamp(row[30]).strftime('%Y-%m-%d %H:%M:%S')
        if row[36]:
            e.time_last_modified = datetime.datetime.fromtimestamp(row[36]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            e.time_last_modified = e.time_created
        e.count_comment = row[33]

        cur.execute("SELECT vote_users FROM dq_revolution WHERE zb_id = 'analysis' AND zb_no = %s" % row[0])
        recs = cur.fetchall()
        if recs:
            assert len(recs) == 1
            rec = recs[0]
            find_user = re.compile(r'\d+')
            rec_users = find_user.findall(rec)
            for rec_user in rec_users:
                e.recommendation.add(User.objects.get(pk = rec_user))

        e.count_view = row[31]
        e.count_recommendation = row[32]

        e.save()

        f1_03, f2_03 = None, None
        if row[24]:
            try: 
                f1_03 = open(u'/Users/libelo/documents/code/yig03/yig03_20130204/public_html/zero/' + row[24])
            except:
                pass
            else:
                f1 = BulletinFile()
                f1.entry = e
                f1.name = row[26]
                f1.file = File(f1_03)
                f1.hit = row[28]
                f1.save()
        if row[25]:
            try: 
                f2_03 = open(u'/Users/libelo/documents/code/yig03/yig03_20130204/public_html/zero/' + row[25])
            except:
                pass
            else:
                f2 = BulletinFile()
                f2.entry = e
                f2.name = row[27]
                f2.file = File(f2_03)
                f2.hit = row[29]
                f2.save()

        if f1_03:
            f1_03.close()
        if f2_03:
            f2_03.close()

        return datetime.datetime.fromtimestamp(row[30]).strftime('%Y-%m-%d %H:%M:%S')

        # cur.execute("SELECT vote_users FROM dq_revolution WHERE zb_id = analysis, zb_no = %s" % row[0])



