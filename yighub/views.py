# -*- coding: utf-8 -*-

from django.template import Context, loader

from yighub.models import User, Letter, Memo, UserForm
from yighub.models import BulletinBoard, TaskforceBoard, PublicBoard
from yighub.models import BulletinEntry, TaskforceEntry, PublicEntry
from yighub.models import BulletinComment, TaskforceComment, PublicComment
from yighub.models import BulletinThumbnail, TaskforceThumbnail, PublicThumbnail 
from yighub.models import BulletinFile, TaskforceFile, PublicFile, File
from yighub.models import BulletinEntryForm, TaskforceEntryForm, PublicEntryForm
from yighub.models import TaskforceBoardForm
from yighub.models import Album, Photo, PhotoComment
from yighub.models import AlbumForm, PhotoForm

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
import mimetypes
import datetime
from django.utils import timezone
from django.contrib.auth import hashers

import re

import transformation

PublicBoardList = PublicBoard.objects.all()
PublicBoardDict = {}
for public_board in PublicBoardList:
    PublicBoardDict[public_board.name[:4]] = public_board

current_ordinal = 21

def classify(board):
    exist = True
    if board == 'bulletin':
        Board = BulletinBoard
        Entry = BulletinEntry
        Comment = BulletinComment
        Thumbnail = BulletinThumbnail
        File = BulletinFile
        EntryForm = BulletinEntryForm
    elif board == 'taskforce':
        Board = TaskforceBoard
        Entry = TaskforceEntry
        Comment = TaskforceComment
        Thumbnail = TaskforceThumbnail
        File = TaskforceFile
        EntryForm = TaskforceEntryForm
    elif board == 'public':
        Board = PublicBoard
        Entry = PublicEntry
        Comment = PublicComment
        Thumbnail = PublicThumbnail
        File = PublicFile
        EntryForm = PublicEntryForm
    else:
        exist = False

    return (exist, Board, Entry, Comment, Thumbnail, File, EntryForm)


def pagination(board, board_id, current_page, page_size = 20): # board_number가 0이면 최신글 목록

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    board_id = int(board_id)
    current_page = int(current_page) if current_page != '0' else 1
    no = (current_page - 1) * page_size # 그 앞 페이지 마지막 글까지 개수

    # 총 글 수와 entry list 구하기
    if board_id != 0:
        b = Board.objects.get(pk = board_id)
        count_entry = b.count_entry #Entry.objects.filter(board = ... ).count()
        entry_list = Entry.objects.filter(board = b).order_by('-arrangement')[no : (no + page_size)]
    else:
        count_entry = Entry.objects.count()
        entry_list = Entry.objects.all().order_by('-time_created')[no : (no + page_size)] # filter(board = board_number)

    # 첫 페이지와 끝 페이지 설정
    first_page = 1
    last_page = (count_entry - 1)/page_size + 1

    # 페이지 리스트 만들기
#    real_list = []
    for e in entry_list:
        e.range = range(e.depth)
        """
        if e.depth:
            try:
                p = Entry.objects.get(pk = e.parent)
            except Entry.DoesNotExist:
                real_list.append("원본 글이 삭제되었습니다.")
            else:
                if p.board.pk != board_number:
                    real_list.append("원본 글이 이동되었습니다.")
                else:
                    pass
        real_list.append(e) 
        """
    # if current_page < 5:
    if current_page < 4:
        start_page = 1
    else:
        # start_page = current_page - 4
        start_page = current_page - 3

    # if current_page > last_page - 5:
    if current_page > last_page - 4:
        end_page = last_page
    elif current_page < 4:
        end_page = 7
    else:
        # end_page = current_page + 4
        end_page = current_page + 3

    page_list = range(start_page, end_page + 1)

    # 이전 페이지, 다음 페이지 설정
    prev_page = current_page - 5
    next_page = current_page + 5

    # 맨 첫 페이지나 맨 끝 페이지일 때 고려
    if current_page > last_page - 5:
        next_page = 0
        last_page = 0
    if current_page <= 5:
        prev_page = 0
        first_page = 0

    return {'entry_list' : entry_list,
            'current_page' : current_page,
            'page_list' : page_list,
            'first_page' : first_page,
            'last_page' : last_page,
            'prev_page' : prev_page,
            'next_page' : next_page,
            }

def check_permission(request, board, current_board = None, mode = 'reading'):
    
    LevelDict = {'non':0, 'pre':1, 'asc':2, 'reg':3, 'exe':4, 'mgr':5}

    if board == 'public' and mode == 'reading':
        return True, None

    try:
        u = request.session['user_id']
        user = User.objects.get(user_id = u) 
    except KeyError:
        return False, redirect('yighub:login')
    except User.DoesNotExist: # 세션에는 남아있지만 데이터베이스에는 없는 경우. 회원탈퇴이거나 다른 app을 쓰다 접근.
        return False, redirect('yighub:logout',)

    if not current_board:
        if LevelDict[user.level] >= 1:
            return True, None
        else:
            messages.error(request, '접근 권한이 없습니다.')
            return False, render(request, 'yighub/error.html', )

    if mode == 'reading':
        if LevelDict[user.level] >= LevelDict[current_board.permission_reading]:
            return True, None
        else:
            messages.error(request, '접근 권한이 없습니다.')
            return False, render(request, 'yighub/error.html', )
    elif mode == 'writing':
        if LevelDict[user.level] >= LevelDict[current_board.permission_writing]:
            return True, None
        else:
            messages.error(request, '접근 권한이 없습니다.')
            return False, render(request, 'yighub/error.html', )
    else:
        raise 'invalid argument'

def get_board_list(board):

    if board == 'taskforce':
        board_list = TaskforceBoard.objects.filter(archive = False).order_by('-count_entry')
    elif board == 'bulletin':
        board_list = BulletinBoard.objects.all()
    else:
        board_list = None

    return board_list

def home(request):

    if 'user_id' not in request.session:
        return render(request, 'yighub/home_for_visitor.html', {'public_dict' : PublicBoardDict})
    else:
        u = request.session['user_id']
    try:
        user = User.objects.get(user_id = u)
    except User.DoesNotExist:
        return redirect(reverse('yighub:logout'))

    # 홈페이지를 열 때마다 마지막 방문날짜를 업데이트한다.
    user.last_login = timezone.now()
    user.save()
    
    if user.level == 'non':
        return render(request, 'yighub/home_for_visitor.html', {'public_dict' : PublicBoardDict})

    memos = Memo.objects.all().order_by('-pk')[0:10]
    bulletin_list = get_board_list('bulletin')
    taskforce_list = get_board_list('taskforce')
    # bulletin_news = BulletinEntry.objects.all().order_by('-time_created')[0:5]
    # for b in bulletin_news:
    #     b.range = range(b.depth)
    # taskforce_news = TaskforceEntry.objects.all().order_by('-time_created')[0:5]
    # for t in taskforce_news:
    #     t.range = range(t.depth)
    news = []
    bulletin_news = BulletinEntry.objects.all().order_by('-time_created')[0:10]
    for b in bulletin_news:
        b.board_type = 'bulletin'
    news += bulletin_news
    taskforce_news = TaskforceEntry.objects.all().order_by('-time_created')[0:10]
    for t in taskforce_news:
        t.board_type = 'taskforce'
    news += taskforce_news
    news = sorted(news, key = lambda news: news.time_created, reverse = True)[:10]
    """ 메모를 위한 거였구만.

    # 최신글 목록 가져오기
    news = Entry.objects.all().order_by('-arrangement')[0:10]

    current_page = int(current_page)
    page_size = 10
    no = (current_page - 1) * page_size

    # 총 글 수와 entry list 구하기
    count_entry = Memo.objects.count()
    entry_list = Memo.objects.all().order_by('-pk')[no : (no + page_size)] # filter(board = board_number)

    # 첫 페이지와 끝 페이지 설정
    first_page = 1
    last_page = (count_entry - 1)/page_size + 1
    
    # 페이지 리스트 만들기
    if current_page < 5:
        start_page = 1
    else:
        start_page = current_page - 4

    if current_page > last_page - 5:
        end_page = last_page
    else:
        end_page = current_page + 4
    
    page_list = range(start_page, end_page + 1)

    # 이전 페이지, 다음 페이지 설정
    prev_page = current_page - 1
    next_page = current_page + 1
    
    # 맨 첫 페이지나 맨 끝 페이지일 때 고려
    if current_page == last_page:
        next_page = 0
        last_page = 0
    if current_page == first_page:
        prev_page = 0
        first_page = 0
    """

    # # memo 페이지 dictionary 만들기
    # m = {'entry_list' : entry_list, 'current_page' : current_page,
    #         'page_list' : page_list,
    #         'first_page' : first_page,
    #         'last_page' : last_page,
    #         'prev_page' : prev_page,
    #         'next_page' : next_page,
    #        }

    return render(request, 'yighub/home_for_member.html', # 아직까지는 페이지 넘기기 지원하지 않음.
                                  { 'user' : user,
                                    'public_dict' : PublicBoardDict,
                                    'bulletin_list' : bulletin_list,
                                    'taskforce_list' : taskforce_list,
                                    # 'bulletin_news' : bulletin_news,
                                    # 'taskforce_news' : taskforce_news,
                                    'news' : news,
                                    'memos' : memos,
                                   },   
                                  ) 

def news(request, board, page):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False or Board == PublicBoard:
        raise Http404

    # 권한 검사
    try:
        u = request.session['user_id']
        user = User.objects.get(user_id = u) 
    except KeyError:
        return redirect('yighub:login')
    except User.DoesNotExist: # 세션에는 남아있지만 데이터베이스에는 없는 경우. 회원탈퇴이거나 다른 app을 쓰다 접근.
        return redirect('yighub:logout',)
    if user.level == 'non':
        messages.error(request, '접근 권한이 없습니다.')
        return render(request, 'yighub/error.html', )

    p = pagination(board, board_id = 0, current_page = page)
    board_list = get_board_list(board)

    return render(request, 'yighub/news.html',
        {'user': user, 'public_dict' : PublicBoardDict, 'board': board, 'board_list': board_list, 'page': p}
        )

def listing(request, board, board_id, page = '0'):    # url : yig.in/yighub/board/1/page/3

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        current_board = Board.objects.get(pk = board_id)
    except Board.DoesNotExist:
        raise Http404

    if current_board.name in ('Research',):
        p = pagination(board, board_id, current_page = page, page_size = 3)
    elif current_board.name in ('simA', 'simB', 'simV', 'Universe'):
        p = pagination(board, board_id, current_page = page, page_size = 1)        
    else:
        p = pagination(board, board_id, current_page = page)
    board_list = get_board_list(board)
    
    # 권한 검사
    permission = check_permission(request, board, current_board)
    if permission[0] == False:
        return permission[1] 
    try:
        u = request.session['user']
    except:
        u = None

    if board == 'public':

        if current_board.name == 'Member Profile':

            if page == '0':
                p['display_ordinal'] = current_ordinal
            else:
                p['display_ordinal'] = int(page)

            p['user_list'] = User.objects.filter(ordinal = p['display_ordinal'])
            p['ordinal_range'] = range(1, current_ordinal+1)

        if current_board.name == 'History':
            for e in p['entry_list']:                
                e.history = [] 
                months = e.content.split('\n')
                for m in months:
                    month = m.split('-')[0][:-1]
                    events = m.split('-')[1].split(', ')
                    e.history.append({'month': month, 'events': events})

        return render(request, 'yighub/public_' + current_board.name + '.html', 
            {'user': u, 'public_dict' : PublicBoardDict, 'board': board, 'board_list': board_list, 'current_board': current_board, 'page': p}
            )

    return render(request, 'yighub/listing.html',
        {'user': u, 'public_dict' : PublicBoardDict, 'board': board, 'board_list': board_list, 'current_board': current_board, 'page': p}
        )

    # if board_id:
    #     b = Board.objects.get(pk = board_id)
    # else:
    #     class b:
    #         pass
    #     b.name = '최신글 목록'

    # if b.name == '최신글 목록':
    #     return render(request, 'yighub/news.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # if b.name == 'Board':
    #     return render(request, 'yighub/board.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # if b.name == 'Notice':
    #     return render(request, 'yighub/notice.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # if b.name == 'Company Analysis':
    #     return render(request, 'yighub/company analysis.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # if b.name == 'Portfolio':
    #     return render(request, 'yighub/portfolio.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # if b.name == 'Column':
    #     return render(request, 'yighub/column.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })
    # else:
    #     return render(request, 'yighub/taskforce.html', {'user' : request.session['user'], 'board' : b, 'page' : p, })

def create_taskforce(request):

    # 권한 검사
    permission = check_permission(request, 'taskforce', mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.method == 'POST':
        form = TaskforceBoardForm(request.POST)
        if form.is_valid():

            t = form.save(commit = False)            
            t.permission_reading = 'pre'
            t.permission_writing = 'pre'
            t.save()

            return redirect('yighub:news', board='taskforce', page=1 )
    else:
        form = TaskforceBoardForm()

    u = request.session['user']

    return render(request, 'yighub/create_taskforce.html', {'user' : u, 'public_dict' : PublicBoardDict, 'form' : form})

def edit_taskforce(request, taskforce_id): # 여기서 archive로 넘기기도 처리. 삭제는 일단 구현 안함. 게시글이 하나도 없을 때만 가능.

    try:
        t = TaskforceBoard.objects.get(pk = taskforce_id)
    except TaskforceBoard.DoesNotExist:
        return Http404

    # 권한 검사
    permission = check_permission(request, 'taskforce', current_board = t, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.method == 'POST':
        form = TaskforceBoardForm(request.POST, instance = t)
        if form.is_valid():

            t = form.save(commit = False)
            if 'to_archive' in request.POST:
                if request.POST['to_archive']:
                    t.archive = True
            if 'to_list' in request.POST:
                if request.POST['to_list']:
                    t.archive = False
            t.save()

            return redirect('yighub:news', board='taskforce', page=1 )
    else:
        form = TaskforceBoardForm(instance = t)

    u = request.session['user']

    return render(request, 'yighub/edit_taskforce.html', {'user' : u, 'public_dict' : PublicBoardDict, 'form' : form, 'current_taskforce' : t})

def taskforce_archive(request):

    # 권한 검사
    permission = check_permission(request, 'taskforce', mode = 'writing')
    if permission[0] == False:
        return permission[1]

    taskforce_list = TaskforceBoard.objects.filter(archive = True).order_by('-newest_time')

    u = request.session['user']
    board_list = get_board_list('taskforce')

    return render(request, 'yighub/taskforce_archive.html', 
        {'user' : u, 
        'public_dict' : PublicBoardDict, 
        'board' : 'taskforce', 
        'board_list' : board_list,
        'taskforce_list' : taskforce_list
        })

def read(request, board, entry_id,):
        
    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id) 
    except Entry.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, board, e.board)
    if permission[0] == False:
        return permission[1]
    u = request.session['user']
    
    e.count_view += 1
    e.save()

    thumbnails = e.thumbnails.all()
    files = e.files.all() #File.objects.filter(entry = e)
    recommendations = e.recommendation.all()
    comments = e.comments.order_by('arrangement')
    current_board = e.board
    board_list = get_board_list(board)

    return render(request, 'yighub/read.html',
      {'user' : u,
      'public_dict' : PublicBoardDict, 
      'board' : board,
      'board_list' : board_list,
      'current_board' : current_board,
      'entry' : e,
      'thumbnails' : thumbnails,
      'files' : files,
      'recommendations' : recommendations,
      'comments' : comments,
      },
      )

def create(request, board, board_id = None):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    if board_id:
        try:
            current_board = Board.objects.get(pk = board_id)
        except Board.DoesNotExist:
            raise Http404
    else:
        current_board = None

    # 권한 검사
    permission = check_permission(request, board, current_board, mode = 'writing')
    if permission[0] == False:
        return permission[1]
    u = request.session['user']

    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            
            current_board = Board.objects.get(pk = request.POST['board'])

            # arrangement 할당
            try:
                last_entry = Entry.objects.filter(board = current_board).order_by('-arrangement')[0]
            except IndexError:
                arrangement = 1000
            else:
                arrangement = (last_entry.arrangement/1000 + 1) * 1000

            # 글을 저장한다.
            e = form.save(commit = False)
            e.creator = request.session['user']
            e.time_created = timezone.now()
            e.time_last_modified = timezone.now()
            e.arrangement = arrangement
            e.save()

            # 썸네일을 저장한다.
            thumbnails = request.FILES.getlist('thumbnails')
            for thumbnail in thumbnails:
                t = Thumbnail(entry = e, name = thumbnail.name, thumbnail = thumbnail)
                t.save()
            
            # 여러 파일들을 저장한다.
            files = request.FILES.getlist('files')
            for file in files:
                f = File(entry = e, name = file.name, file = file)
                f.save()
            
            # 게시판 정보를 업데이트한다.
            b = Board.objects.get(pk = request.POST['board'])
            b.count_entry += 1
            b.newest_entry = e.id
            b.newest_time = e.time_last_modified
            b.save()

            return redirect('yighub:listing', board=board, board_id=b.id, page=1)
    else:
        if board_id:
            form = EntryForm(initial = {'board' : current_board})
        else:
            form = EntryForm()

    board_list = get_board_list(board)

    return render(request, 'yighub/create.html', 
        {'user' : u, 
        'public_dict' : PublicBoardDict, 
        'board' : board,
        'board_list' : board_list,
        'current_board' : current_board,
        'form' : form, }
        )

def edit(request, board, entry_id):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id)
    except Entry.DoesNotExist:
        return Http404
        #messages.error(request, 'the entry does not exist')
        #return render(request, 'yighub/error.html', )

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]
    u = request.session['user']

    if request.method == 'POST':
        form = EntryForm(request.POST, instance = e)
        if form.is_valid():

            e = form.save(commit = False)
            e.time_last_modified = timezone.now()
            e.save()
            
            for t in e.thumbnails.all():
                try:
                    string = 'delete_thumbnail_' + str(t.id)
                    request.POST[string]
                except KeyError:
                    pass
                else:
                    t.thumbnail.delete()
                    t.delete()

            thumbnails = request.FILES.getlist('thumbnails')
            for thumbnail in thumbnails:
                t = Thumbnail(entry = e, name = thumbnail.name, thumbnail = thumbnail)
                t.save()

            for f in e.files.all():
                try:
                    string = 'delete_file_' + str(f.id)
                    request.POST[string]
                except KeyError:
                    pass
                else:
                    f.file.delete()
                    f.delete()
            
            files = request.FILES.getlist('files')
            for file in files:
                f = File(entry = e, name = file.name, file = file)
                f.save()

            # 게시판 정보를 업데이트한다. - 필요한가?
            ##b = e.board
            ##b.newest_entry
            ##b.newest_time

            return redirect('yighub:read', board=board, entry_id = entry_id) #HttpResponseRedirect(reverse('yighub.views.read', args = (entry_id, )))
            
    else:
        form = EntryForm(
            initial = {'user' : u,
            'board' : e.board, 'title' : e.title, 'content' : e.content, 'notice' : e.notice}
            )
    
    thumbnails = e.thumbnails.all()
    files = e.files.all()
    board_list = get_board_list(board)
    current_board = e.board

    return render(request, 'yighub/edit.html', 
        {'user' : u, 
        'public_dict' : PublicBoardDict, 
        'board' : board,
        'board_list' : board_list,
        'current_board' : current_board,
        'form' : form, 'thumbnails' : thumbnails, 'files' : files, 'entry_id' : entry_id },)


def delete(request, board, entry_id):
    
    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id)
    except Entry.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.session['user'] == e.creator:
        thumbnails = e.thumbnails.all()
        for t in thumbnails:
            t.thumbnail.delete()

        files = e.files.all()
        for f in files:
            f.file.delete()

        # 게시판 정보를 업데이트한다.
        b = e.board
        b.count_entry -= 1
        if e.id == b.newest_entry:
            if b.count_entry > 1: 
                prev_entry = Entry.objects.filter(board = b).order_by('-arrangement')[1] # edit과 reply를 포함하면 time_last_modified로.
                b.newest_entry = prev_entry.id
                b.newest_time = prev_entry.time_last_modified
            else: # 게시판에 글이 하나 남았을 때
                b.newest_entry = None
                b.newest_time = None
        b.save()

        e.delete()
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )
        #return render(request, 'yighub/error.html', {'error' : 'invalid approach'})
    return HttpResponseRedirect(reverse('yighub:home', ))

def reply(request, board, entry_id): # yig.in/entry/12345/reply     

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        parent = Entry.objects.get(pk = entry_id)
    except Entry.DoesNotExist:
        raise Http404
    
    # 권한 검사
    permission = check_permission(request, board, parent.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]
    u = request.session['user']

    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            
            current_depth = parent.depth + 1
            current_arrangement = parent.arrangement - 1
            p = entry_id
            scope = Entry.objects.filter(board = parent.board).filter(arrangement__gt = (current_arrangement/1000) * 1000).filter(arrangement__lte = current_arrangement)
            
            while True:
                try:
                    q = scope.filter(parent = p).order_by('arrangement')[0] 
                except IndexError:
                    break
                else:
                    current_arrangement = q.arrangement - 1
                    p = q.id
            
            to_update = Entry.objects.filter(board = parent.board).filter(arrangement__gt = (current_arrangement/1000) * 1000 ).filter(arrangement__lte = current_arrangement)
            for e in to_update:
                e.arrangement -= 1
                e.save()

            reply = form.save(commit = False)
            reply.arrangement = current_arrangement
            reply.depth = current_depth
            reply.parent = entry_id
            reply.creator = request.session['user']
            reply.time_created = timezone.now()
            reply.time_last_modified = timezone.now()
            reply.save()

            thumbnails = request.FILES.getlist('thumbnails')
            for thumbnail in thumbnails:
                t = Thumbnail(entry = reply, name = thumbnail.name, thumbnail = thumbnail)
                t.save()

            files = request.FILES.getlist('files')
            for file in files:
                f = File(entry = reply, name = file.name, file = file)
                f.save()

            # 게시판 정보를 업데이트한다.
            b = reply.board
            b.newest_entry = reply.id
            b.newest_time = reply.time_created
            b.count_entry += 1
            b.save()

            return HttpResponseRedirect(reverse('yighub:home'))
    else:
        form = EntryForm(initial = {'board' : parent.board}) # board 빼고 보내기

    board_list = get_board_list(board)
    b = parent.board

    return render(request, 'yighub/reply.html', 
        {'user' : u,
        'public_dict' : PublicBoardDict, 
        'board' : board,
        'board_list' : board_list,
        'current_board' : b,
        'form' : form, 'parent' : entry_id}, 
        ) 

def recommend(request, board, entry_id):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id) 
    except Entry.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    u = request.session['user']
    if u in e.recommendation.all():
        messages.error(request, 'You already recommend this')
        return render(request, 'yighub/error.html', )
    e.recommendation.add(u)
    e.count_recommendation += 1
    e.save()

    return redirect('yighub:read', board = board, entry_id = entry_id)

def delete_recommend(request, board, entry_id):
    
    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id) 
    except Entry.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]
    
    u = request.session['user']
    if u in e.recommendation.all():
        e.count_recommendation -= 1
        e.recommendation.remove(u)
        e.save()
        return redirect('yighub:read', board = board, entry_id = entry_id)
    else:
        messages.error(request, 'You have not recommended this')
        return render(request, 'yighub/error.html', )

def comment(request, board, entry_id):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    if request.method == 'POST':
        e = Entry.objects.get(pk = entry_id)
        try:
            newest_comment = Comment.objects.order_by('-arrangement')[0]
        except IndexError:
            arrangement = 0
        else:
            arrangement = (newest_comment.arrangement/1000 + 1) * 1000
        c = Comment(entry = e,
                    content = request.POST['content'],
                    creator = request.session['user'],
                    time_created = timezone.now(),
                    arrangement = arrangement,
                    )
        c.save()
        e.count_comment += 1
        e.save()

        return redirect('yighub:read', board = board, entry_id = entry_id) # HttpResponseRedirect(reverse('yighub.views.read', args = (entry_id)))
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )

def reply_comment(request, board, entry_id):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    if request.method == 'POST':
        e = Entry.objects.get(pk = entry_id)
        u = request.session['user']

        parent = Comment.objects.get(pk = int(request.POST['comment_id'])) # int error ?
        current_depth = parent.depth + 1
        current_arrangement = parent.arrangement + 1

        p = request.POST['comment_id']
        scope = Comment.objects.filter(entry = e).filter(arrangement__gte = current_arrangement).filter(arrangement__lt = (parent.arrangement/1000 + 1) * 1000)

        while True:
            try:
                q = scope.filter(parent = p).order_by('arrangement')[0] 
            except IndexError:
                break
            else:
                current_arrangement = q.arrangement + 1
                p = q.pk

        to_update = Comment.objects.filter(arrangement__gte = current_arrangement).filter(arrangement__lt = (current_arrangement/1000 + 1) * 1000 )
        for c in to_update:
            c.arrangement += 1
            c.save()

        reply_comment = Comment(entry = e,
                                content = request.POST['content'], 
                                creater = u, 
                                time_created = timezone.now(),
                                arrangement = current_arrangement,
                                depth = current_depth,
                                parent = request.POST['comment_id'],
                                )                                              
        reply_comment.save()

        return HttpResponseRedirect(reverse('yighub:read', board = board, entry_id = entry_id))
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )

def recommend_comment(request, board, entry_id, comment_id):

    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id) 
        c = Comment.objects.get(pk = comment_id)
    except Entry.DoesNotExist, Comment.DoesNotExist: # comma로 묶는게 어떤 의미인가?
        raise Http404    

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    u = request.session['user']
    if u in c.recommendation.all():
        messages.error(request, 'You already recommend this')
        return render(request, 'yighub/error.html', context_instance = RequestContext(request))
    c.recommendation.add(u)
    c.count_recommendation += 1
    c.save()

    return redirect('yighub:read', board = board, entry_id = entry_id)

def delete_comment(request, board, entry_id, comment_id):
    
    # board 분류
    exist, Board, Entry, Comment, Thumbnail, File, EntryForm = classify(board)
    if exist == False:
        raise Http404

    try:
        e = Entry.objects.get(pk = entry_id)
        c = Comment.objects.get(pk = comment_id)
    except Entry.DoesNotExist, Comment.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, board, e.board, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.session['user'] == c.creator:
        e.count_comment -= 1
        e.save()
        c.delete()

    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )
        #return render(request, 'yighub/error.html', {'error' : 'invalid approach'})
    return redirect('yighub:read', board=board, entry_id=entry_id)


def join(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                User.objects.get(user_id = request.POST['user_id'])
            except User.DoesNotExist:
                if request.POST['password'] == request.POST['password_check']:
                    regex = re.compile(r'\d{3}-\d{4}-\d{4}')
                    if not request.POST['phone_number'] or regex.match(request.POST['phone_number']):

                        f = form.save(commit = False)
                        f.password = hashers.make_password(request.POST['password'])
                        f.date_joined = timezone.now()
                        f.last_login = timezone.now()
                        f.level = 'pre'
                        

                        f.profile = request.FILES['profile'] if 'profile' in request.FILES else None
                        f.avatar = request.FILES['avatar'] if 'avatar' in request.FILES else None
                        
                        f.save()

                        u = User.objects.get(user_id = request.POST['user_id'])
                        request.session['user_id'] = u.user_id
                        request.session['user'] = u

                        return redirect('yighub:home', )
                    else:
                        messages.error(request, 'phone number must be a form of "010-1234-1234"')
                else:
                    messages.error(request, 'please check your password.')
            else:
                    messages.error(request, 'already used id. please change your id.')
    else:
        form = UserForm()

    return render(request, 'yighub/join.html', {'public_dict' : PublicBoardDict, 'form' : form}, context_instance = RequestContext(request))

def edit_profile(request, first_login = False):

    try:
        u = User.objects.get(user_id = request.session['user_id'])
    except User.DoesNotExist:
        raise Http404

    if request.method == 'POST':

        if u.user_id != request.POST['user_id']:
            try:
                User.objects.get(user_id = request.POST['user_id'])
            except User.DoesNotExist:
                pass
            else:
                messages.error(request, 'already used id. please change your id.')
                form = UserForm(request.POST, )
                return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )

        if not first_login:
            if hashers.check_password(request.POST['password'], u.password):
                pass
            else:
                messages.error(request, 'please enter your old password.')
                form = UserForm(request.POST, )
                return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )

            if request.POST['new_password']:
                if request.POST['new_password'] == request.POST['password_check']:
                    pass
                else:
                    messages.error(request, 'please check your new password.')
                    form = UserForm(request.POST, )
                    return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )
        else:
            if request.POST['password'] == request.POST['password_check']:
                pass
            else:
                messages.error(request, 'please check your password.')
                form = UserForm(request.POST, )
                return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )

        regex = re.compile(r'\d{3}-\d{4}-\d{4}')
        if not regex.match(request.POST['phone_number']):
            messages.error(request, 'phone number must be a form of "010-1234-1234"')
            form = UserForm(request.POST, )
            return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )

        form = UserForm(request.POST, request.FILES, instance = u)
        if form.is_valid():

            f = form.save(commit = False)

            if not first_login:
                if request.POST['new_password']:
                    f.password = hashers.make_password(request.POST['new_password'])
                # else:
                #     f.password = hashers.make_password(request.POST['password'])
            else:
                f.password = hashers.make_password(request.POST['password'])
            f.profile = request.FILES['profile'] if 'profile' in request.FILES else u.profile
            f.avatar = request.FILES['avatar'] if 'avatar' in request.FILES else u.avatar

            f.save()

            u = User.objects.get(user_id = request.POST['user_id'])
            request.session['user_id'] = u.user_id
            request.session['user'] = u

            return redirect('yighub:home', )
    else:
        form = UserForm(instance = u, )

    return render(request, 'yighub/edit_profile.html', {'user':u, 'public_dict' : PublicBoardDict, 'form' : form, 'first_login' : first_login}, )

def delete_profile(request):
    pass

def login(request):
    request.session.set_test_cookie()
    return render(request, 'yighub/login.html', {'public_dict' : PublicBoardDict})
    
def login_check(request):
    try:
        u = User.objects.get(user_id = request.POST['user_id'])
    except User.DoesNotExist:
        messages.error(request, 'incorrect user id')
        return render(request, 'yighub/login.html', {'public_dict' : PublicBoardDict})

    if request.session.test_cookie_worked():

        if u.password == '':
            u.password = hashers.make_password(request.POST['password'])
            u.save()
            request.session['user_id'] = u.user_id      
            request.session['user'] = u      
            return redirect('yighub:first_login',)

        if hashers.check_password(request.POST['password'], u.password):
            request.session['user_id'] = u.user_id
            request.session['user'] = u

            return HttpResponseRedirect(reverse('yighub:home'))
        else:
            messages.error(request, 'password does not correct') # send message 
            return render(request, 'yighub/login.html', {'public_dict' : PublicBoardDict})
    else:
        # send message about cookie
        messages.error(request, 'please enable cookie')
        return render(request, 'yighub/login.html', {'public_dict' : PublicBoardDict})

def logout(request):
    request.session.flush() # exact functionality of flush method? after flush, home_for_visitor is presenting?
    return HttpResponseRedirect(reverse('yighub:home'))

def send(request):
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():

            s = form.save(commit = False)
            s.sender = request.session['user']
            s.file_name = request.FILES['file'].name
            s.save()

            return redirect('yighub.views.receive', )
    else:
        form = LetterForm()

    return render(request, 'yighub/send.html', {'form' : form}, context_instance = RequestContext(request))
 
         
def letters(request):
    u = request.POST['user']
    letters = Letter.objects.filter(receiver = u)

    # 페이지 넘기기 설정하기

    return render(request, 'yighub/letters.html', {'letters' : letters, })

def receive(request, letter_id): 

    if check_permission(request):
        pass

    try:
        l = Letter.objects.get(pk = letter_id)
    except Letter.DoesNotExist:
        raise Http404
    
    u = request.POST['user']
    
    if l.receiver == u:
        l.read = True
        l.save()
        return render(request, 'yighub/receive.html', {'letter' : l})
    else:
        messages.error(request, 'Not You')
        return render(request, 'yighub/error.html', context_instance = RequestContext(request))

def memo(request, page = 1):
    
    permission = check_permission(request, 'memo')
    if permission[0] == False:
        return permission[1] 
    u = request.session['user']
    
    bulletin_list = get_board_list('bulletin')
    taskforce_list = get_board_list('taskforce')

    current_page = int(page)
    page_size = 20
    no = (current_page - 1) * page_size # 그 앞 페이지 마지막 글까지 개수

    count_entry = Memo.objects.count()
    memo_list = Memo.objects.all().order_by('-pk')[no : (no + page_size)] # filter(board = board_number)

    # 첫 페이지와 끝 페이지 설정
    first_page = 1
    last_page = (count_entry - 1)/page_size + 1

    # 페이지 리스트 만들기
    # if current_page < 5:
    if current_page < 4:
        start_page = 1
    else:
        # start_page = current_page - 4
        start_page = current_page - 3

    # if current_page > last_page - 5:
    if current_page > last_page - 4:
        end_page = last_page
    elif current_page < 4:
        end_page = 7
    else:
        # end_page = current_page + 4
        end_page = current_page + 3

    page_list = range(start_page, end_page + 1)

    # 이전 페이지, 다음 페이지 설정
    prev_page = current_page - 5
    next_page = current_page + 5

    # 맨 첫 페이지나 맨 끝 페이지일 때 고려
    if current_page > last_page - 5:
        next_page = 0
        last_page = 0
    if current_page <= 5:
        prev_page = 0
        first_page = 0

    p = {'memo_list' : memo_list,
            'current_page' : current_page,
            'page_list' : page_list,
            'first_page' : first_page,
            'last_page' : last_page,
            'prev_page' : prev_page,
            'next_page' : next_page,
            }

    return render(request, 'yighub/memo.html',
        {'user': u, 'public_dict' : PublicBoardDict, 
        'bulletin_list' : bulletin_list, 
        'taskforce_list' : taskforce_list, 'page': p})



def create_memo(request):
    if request.method == 'POST':
        m = Memo(memo = request.POST['memo'],
                 creator = request.session['user'],
                 time_created = timezone.now(),
                )
        m.save()
        
        return redirect('yighub:home', ) # HttpResponseRedirect(reverse('yighub.views.read', args = (entry_id)))
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', context_instance = RequestContext(request))

def delete_memo(request, memo_id):

    try:
        m = Memo.objects.get(pk = memo_id)
    except Memo.DoesNotExist:
        raise Http404

    if request.session['user'] == m.creator:
        m.delete()

    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )
        #return render(request, 'yighub/error.html', {'error' : 'invalid approach'})
    return HttpResponseRedirect(reverse('yighub:home', ))

from django.core.files import File as FileWrapper
from django.utils.encoding import smart_str
import os
def download(request, file_id):
    
    f = File.objects.get(pk = file_id)
    
    path = f.file.path
    filetype, encoding = mimetypes.guess_type(path)
    fw = FileWrapper(open(path,'r'))

    response = HttpResponse(fw)
    response['Content-Type'] = filetype
    response['Content-Encoding'] = encoding
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(path))
    
    f.hit += 1
    f.save()
    
    #if type is None:
    #    type = 'application/octet-stream'
     #response['Content-Type'] = filetype
     #response['Content-Encoding'] = encoding
#    encoded_name = f.file.name.encode(encoding = 'UTF-8')
    #fp.close를 하면 안된다?
    return response

def download_letter(request, letter_id):
    pass

def albums(request, page = 1):
    
    board = 'albums'

    # 권한 검사
    permission = check_permission(request, board, )
    if permission[0] == False:
        return permission[1]
    u = request.session['user']
    
    page_size = 20
    current_page = int(page) if page != '0' else 1
    no = (current_page - 1) * page_size # 그 앞 페이지 마지막 글까지 개수

    count_album = Album.objects.count()
    album_list = Album.objects.order_by('-newest_time')[no : (no + page_size)]

    albums = []
    for album in album_list:
        try:
            albums += [{'album':album, 'thumbnail':album.photos.all()[0]}]
        except:
            albums += [{'album':album, 'thumbnail':None}]

    # 첫 페이지와 끝 페이지 설정
    first_page = 1
    last_page = (count_album - 1)/page_size + 1

    # 페이지 리스트 만들기
    if current_page < 5:
        start_page = 1
    else:
        start_page = current_page - 4

    if current_page > last_page - 5:
        end_page = last_page
    else:
        end_page = current_page + 4

    page_list = range(start_page, end_page + 1)

    # 이전 페이지, 다음 페이지 설정
    prev_page = current_page - 5
    next_page = current_page + 5

    # 맨 첫 페이지나 맨 끝 페이지일 때 고려
    if current_page > last_page - 5:
        next_page = 0
        last_page = 0
    if current_page <= 5:
        prev_page = 0
        first_page = 0

    p = {'album_list' : album_list,
            'current_page' : current_page,
            'page_list' : page_list,
            'first_page' : first_page,
            'last_page' : last_page,
            'prev_page' : prev_page,
            'next_page' : next_page,
            }


    return render(request, 'yighub/albums.html', {'user':u, 'public_dict' : PublicBoardDict, 'albums':albums, 'page':p})

def photos(request, album_id):
    
    board = 'albums'

    # 권한 검사
    permission = check_permission(request, board, )
    if permission[0] == False:
        return permission[1]
    u = request.session['user']
    
    album = Album.objects.get(pk = album_id)
    album.count_view += 1
    album.save()
    photos = album.photos.all()
    # template과 model의 분리를 위해 여기서 처리해야 하지만, 일단 이번엔 template에서 시도해본다. 되긴 된다. 
    #for p in photos:
    #    p.recommendations = p.recommendation.all()
    #    p.comment_list = p.comments.all()

    return render(request, 'yighub/photos.html', {'user':u, 'public_dict' : PublicBoardDict, 'album':album, 'photos':photos, })

def create_album(request,):
    
    # 권한 검사
    permission = check_permission(request, 'albums')
    if permission[0] == False:
        return permission[1]

    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():

            a = form.save(commit = False)            
            a.permission_reading = 'pre'
            a.permission_writing = 'pre'
            a.save()

            return redirect('yighub:albums', page = 1)
    else:
        form = AlbumForm()

    u = request.session['user']

    return render(request, 'yighub/create_album.html', {'user' : u, 'public_dict' : PublicBoardDict, 'form' : form})

def edit_album(request,):
    pass

def create_photos(request, album_id):

    try:
        a = Album.objects.get(pk = album_id)
    except Album.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, 'albums', a, mode = 'writing')
    if permission[0] == False:
        return permission[1]
    u = request.session['user']

    if request.method == 'POST':
            
            # 글을 저장한다.
        for k in range(int(request.POST['size'])):
            if 'photo_'+str(k) in request.FILES:
                p = Photo()
                p.album = a
                p.photo = request.FILES['photo_'+str(k)]
                p.description = request.POST['description_'+str(k)]
                p.photographer = request.session['user']
                p.time_created = timezone.now()
                p.time_last_modified = timezone.now()
                p.save()
                # 게시판 정보를 업데이트한다.
                a.count_photo += 1
                a.newest_time = p.time_last_modified
                a.save()
        
        return redirect('yighub:photos', album_id = album_id)
    else:
        form = PhotoForm()

    return render(request, 'yighub/create_photos.html', 
        {'user' : u, 'public_dict' : PublicBoardDict, 'album' : a, 'form' : form, })


def edit_photo(request, album_id, photo_id):
    pass
def delete_photo(request, album_id, photo_id):
    try:
        p = Photo.objects.get(pk = photo_id)
    except Photo.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, 'albums', p.album, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.session['user'] == p.photographer:
        
        # 게시판 정보를 업데이트한다.
        a = p.album
        a.count_entry -= 1
        if p.id == a.newest_entry:
            if a.count_entry > 1: 
                prev_entry = a.photos.order_by('-arrangement')[1] # edit과 reply를 포함하면 time_last_modified로.
                a.newest_entry = prev_entry.id
                a.newest_time = prev_entry.time_last_modified
            else: # 게시판에 글이 하나 남았을 때
                a.newest_entry = None
                a.newest_time = None
        a.save()

        p.delete()
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )
        #return render(request, 'yighub/error.html', {'error' : 'invalid approach'})
    return redirect('yighub:photos', album_id=album_id)

def recommend_photo(request, album_id, photo_id):

    # 권한 검사
    permission = check_permission(request, 'albums', get_object_or_404(Album, pk=album_id), mode = 'writing')
    if permission[0] == False:
        return permission[1]

    try:
        p = Photo.objects.get(pk = photo_id) 
    except Photo.DoesNotExist:
        raise Http404

    u = request.session['user']
    if u in p.recommendation.all():
        messages.error(request, 'You already recommend this')
        return render(request, 'yighub/error.html', )
    p.recommendation.add(u)
    p.count_recommendation += 1
    p.save()

    return redirect('yighub:photos', album_id = album_id)

def delete_recommend_photo(request, album_id, photo_id):

    # 권한 검사
    permission = check_permission(request, 'albums', get_object_or_404(Album, pk=album_id), mode = 'writing')
    if permission[0] == False:
        return permission[1]
      
    try:
        p = Photo.objects.get(pk = photo_id) 
    except Photo.DoesNotExist:
        raise Http404

    u = request.session['user']
    if u in p.recommendation.all():
        p.count_recommendation -= 1
        p.recommendation.remove(u)
        p.save()
        return redirect('yighub:photos', album_id = album_id)
    else:
        messages.error(request, 'You have not recommended this')
        return render(request, 'yighub/error.html', )


def comment_photo(request, album_id, photo_id):
    
    if request.method == 'POST':
        p = get_object_or_404(Photo, pk = photo_id)
        try:
            newest_comment = PhotoComment.objects.order_by('-arrangement')[0]
        except IndexError:
            arrangement = 0
        else:
            arrangement = (newest_comment.arrangement/1000 + 1) * 1000
        c = PhotoComment(photo = p,
                    content = request.POST['content'],
                    creator = request.session['user'],
                    time_created = timezone.now(),
                    arrangement = arrangement,
                    )
        c.save()

        return redirect('yighub:photos', album_id = album_id) 
    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )

def delete_comment_photo(request, album_id, photo_id, comment_id):
    
    try:
        p = Photo.objects.get(pk = photo_id)
        c = PhotoComment.objects.get(pk = comment_id)
    except Photo.DoesNotExist, PhotoComment.DoesNotExist:
        raise Http404

    # 권한 검사
    permission = check_permission(request, 'albums', p.album, mode = 'writing')
    if permission[0] == False:
        return permission[1]

    if request.session['user'] == c.creator:
        c.delete()
        return redirect('yighub:photos', album_id = album_id)

    else:
        messages.error(request, 'invalid approach')
        return render(request, 'yighub/error.html', )

def reply_comment_photo(request, album_id, photo_id, comment_id):
    pass
def recommend_comment_photo(request, album_id, photo_id, comment_id):
    pass

def transform(request,):

    transformation.transform_user()

    transformation.transform_board('data', 'Bulletin')
    transformation.transform_comment('data', 'Bulletin')

    transformation.transform_board('column', 'Bulletin')
    transformation.transform_comment('column', 'Bulletin')

    transformation.transform_board('portfolio', 'Bulletin')
    transformation.transform_comment('portfolio', 'Bulletin')

    transformation.transform_board('analysis', 'Bulletin')
    transformation.transform_comment('analysis', 'Bulletin')

    transformation.transform_board('m_notice', 'Bulletin')
    transformation.transform_comment('m_notice', 'Bulletin')

    transformation.transform_board('board', 'Bulletin')
    transformation.transform_comment('board', 'Bulletin')

    transformation.transform_board('tf', 'Taskforce')
    transformation.transform_comment('tf', 'Taskforce')

    transformation.transform_board('Research', 'Public')
    transformation.transform_comment('Research', 'Public')

    transformation.transform_board('fund', 'Public')
    transformation.transform_comment('fund', 'Public')

    transformation.transform_photos()

    transformation.transform_memo()
    return HttpResponse("Success!")

