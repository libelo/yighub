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

from os import path
from bs4 import BeautifulSoup
import HTMLParser as parser


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

def reverse_escape(content):
    result = re.compile(r'\\r').sub("", content)
    result = re.compile(r'\\n').sub("\n", result)
    result = re.compile(r'\\\\\\"').sub('"', result)
    result = re.compile(r"\\\\\\'").sub("'", result)


    result = re.compile(r'<p>|</p>').sub("\n", result)
    result = re.compile(r'<br />').sub("\n", result)
    p = parser.HTMLParser()
    result = p.unescape(result)
    # result = re.compile(r'&lt;').sub("<", result)
    # result = re.compile(r'&gt;').sub(">", result)
    # result = re.compile(r'&#39;').sub("'", result)
    # result = re.compile(r'&quot;').sub('"', result)
    # result = re.compile(r'&nbsp;').sub(" ", result)
    # result = re.compile(r'&#8226;').sub("•", result)
    # result = re.compile(r'&#46468;').sub("떄", result)
    # result = re.compile(r'&#54973;').sub("횽", result)
    # result = re.compile(r'&#47225;').sub("롹", result)
    # result = re.compile(r'&#47973;').sub("뭥", result)
    # result = re.compile(r'&#48577;').sub("뷁", result)
    # result = re.compile(r'&#52634;').sub("춚", result)
    # result = re.compile(r'&#52573;').sub("쵝", result)
    # result = re.compile(r'&#50043;').sub("썻", result)
    # result = re.compile(r'&#47167;').sub("렿", result)
    # result = re.compile(r'&#51861;').sub("쪕", result)
    # result = re.compile(r'&#55203;').sub("힣", result)
    # result = re.compile(r'&#46489;').sub("떙", result)
    # result = re.compile(r'&#55203;').sub("힣", result)


    return result

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
        u.self_introduction = reverse_escape(row[13])
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


def transform_board(board_name):

    filepath1 = u'/Users/libelo/documents/code/yig03/yig03_20130204/public_html/zero/'
    image_extension = ['jpg', 'JPG', 'png', 'PNG', 'jpeg', 'JPEG', 'bmp', 'BMP', 'gif', 'GIF']

    with sqlite3.connect('yig03.sqlite') as db:

        cur = db.cursor()

        cur.execute("SELECT * FROM zetyx_board_%s" % board_name)

        rows = cur.fetchall()

        for row in rows:

            try:
                b = BulletinBoard.objects.get(name = board_name)
            except:
                b = BulletinBoard(name = board_name)
                b.save()

            e = BulletinEntry()
            e.board = b

            e.title = reverse_escape(row[17])

            e.content = reverse_escape(row[11])
            
            try:
                e.creator = User.objects.get(pk = row[9])
            except User.DoesNotExist:
                noname = User(id = row[9], user_id = '탈퇴회원' + str(row[9]), password = ' ', name = row[14], )
                noname.date_joined = datetime.datetime.fromtimestamp(row[30]) # 정확하진 않지만 탈퇴회원에겐 중요하지 않다.
                noname.last_login = datetime.datetime.fromtimestamp(row[30])
                noname.save()
                e.creator = noname

            e.time_created = datetime.datetime.fromtimestamp(row[30]) #strftime('%Y-%m-%d %H:%M:%S')
            if row[36]:
                e.time_last_modified = datetime.datetime.fromtimestamp(row[36]) #strftime('%Y-%m-%d %H:%M:%S')
            else:
                e.time_last_modified = e.time_created
            e.count_comment = row[33]

            if row[7]:
                cur.execute("SELECT reg_date FROM zetyx_board_%s WHERE no = %d" % (board_name, row[7]))
                find_parent = cur.fetchone()
                if find_parent:
                    parent_object = BulletinEntry.objects.get(time_created = datetime.datetime.fromtimestamp(find_parent[0]))
                else:
                    cur.execute("SELECT reg_date FROM zetyx_board_%s WHERE headnum = %d AND arrangenum = 0" % (board_name, row[2]))
                    parent_object = BulletinEntry.objects.get(time_created = datetime.datetime.fromtimestamp(cur.fetchone()[0]))
                e.parent = parent_object.id
                assert e.parent > 0

            e.depth = row[4]
            if e.depth == 0:
                if b.newest_entry:
                    last_entry = BulletinEntry.objects.get(pk = b.newest_entry)
                    current_arrangement = (last_entry.arrangement/1000 + 1) * 1000
                else:
                    current_arrangement = 1000
                e.arrangement = current_arrangement
                # e.save()
                # b.count_entry += 1
                # b.newest_entry = e.id
                # b.newest_time = e.time_last_modified
                # b.save()
            else:
                assert parent_object.depth + 1 == e.depth
                current_arrangement = parent_object.arrangement - 1
                p = e.parent
                scope = BulletinEntry.objects.filter(board = parent_object.board).filter(arrangement__gt = (current_arrangement/1000) * 1000).filter(arrangement__lte = current_arrangement)
                
                while True:
                    try:
                        q = scope.filter(parent = p).order_by('arrangement')[0] 
                    except IndexError:
                        break
                    else:
                        current_arrangement = q.arrangement - 1
                        p = q.id
                
                to_update = BulletinEntry.objects.filter(board = parent_object.board).filter(arrangement__gt = (current_arrangement/1000) * 1000 ).filter(arrangement__lte = current_arrangement)
                for t in to_update:
                    t.arrangement -= 1
                    t.save()

                e.arrangement = current_arrangement
                # e.save()

                # b.count_entry += 1
                # b.save()

            cur.execute("SELECT file_names, s_file_names, vote_users FROM dq_revolution WHERE zb_id = '%s' AND zb_no = %s" % (board_name, row[0]))
            recs = cur.fetchall()
            if recs and recs[0][2]:
                find_user = re.compile(r'\d+')
                rec_users = find_user.findall(recs[0][2])
                for rec_user in rec_users:
                    try:
                        e.recommendation.add(User.objects.get(pk = int(rec_user)))
                    except:
                        pass
            e.count_view = row[31]
            e.count_recommendation = row[32]

            e.save()
            b.count_entry += 1
            b.newest_entry = e.id
            b.newest_time = e.time_last_modified
            b.save()
            f1_03, f2_03 = None, None
            if row[24]:
                if path.isfile(filepath1 + row[24]):
                    f1_03 = open(filepath1 + row[24])
                else:
                    pass

                if f1_03:
                    if row[24].split('.')[-1] in image_extension:
                        t1 = BulletinThumbnail()
                        t1.entry = e
                        t1.name = reverse_escape(row[26])
                        t1.thumbnail = ImageFile(f1_03)
                        t1.save()
                    else:
                        f1 = BulletinFile()
                        f1.entry = e
                        f1.name = reverse_escape(row[26])
                        f1.file = File(f1_03)
                        f1.hit = row[28]
                        f1.save()
                else:
                    null_ = open('/Users/libelo/documents/code/yig03/파일이_유실되었습니다..txt')
                    null_file = BulletinFile(entry = e, name = '파일이 유실되었습니다.', file = File(null_))
                    null_file.save()
            if row[25]:
                if path.isfile(filepath1 + row[25]): 
                    f2_03 = open(filepath1 + row[25])
                else:
                    pass

                if f2_03:
                    if row[25].split('.')[-1] in image_extension:
                        t2 = BulletinThumbnail()
                        t2.entry = e
                        t2.name = reverse_escape(row[27])
                        t2.thumbnail = ImageFile(f2_03)
                        t2.save()
                    else:
                        f2 = BulletinFile()
                        f2.entry = e
                        f2.name = reverse_escape(row[27])
                        f2.file = File(f2_03)
                        f2.hit = row[29]
                        f2.save()
                else:
                    null_ = open('/Users/libelo/documents/code/yig03/파일이_유실되었습니다..txt')
                    null_file = BulletinFile(entry = e, name = '파일이 유실되었습니다.', file = File(null_))
                    null_file.save()

            if f1_03:
                f1_03.close()
            if f2_03:
                f2_03.close()

            s_f = None
            if recs and recs[0][0]:
                for s_file in enumerate(recs[0][0].split(',')):
                    if path.isfile(filepath1 + s_file[1]):
                        s_f = open(filepath1 + s_file[1])
                    else:
                        pass

                    if s_f:
                        if s_file[1].split('.')[-1] in image_extension:
                            t3 = BulletinThumbnail()
                            t3.entry = e
                            t3.name = reverse_escape(recs[0][1].split(',')[s_file[0]])
                            t3.thumbnail = ImageFile(s_f)
                            t3.save()
                        else:
                            f3 = BulletinFile()
                            f3.entry = e
                            f3.name = reverse_escape(recs[0][1].split(',')[s_file[0]])
                            f3.file = File(s_f)
                            f3.save()
                    else:
                        null_ = open('/Users/libelo/documents/code/yig03/파일이_유실되었습니다..txt')
                        null_file = BulletinFile(entry = e, name = '파일이 유실되었습니다.', file = File(null_))
                        null_file.save()

                    if s_f:
                        s_f.close()

            # cur.execute("SELECT vote_users FROM dq_revolution WHERE zb_id = analysis, zb_no = %s" % row[0])



