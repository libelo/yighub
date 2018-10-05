from django.conf.urls import url
from . import views

app_name = 'yighub'
urlpatterns = [
    url(r'^$', views.home),
    url(r'^home/$', views.home, name='home'),

    url(r'^join/$', views.join, name='join'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.edit_profile, name='edit_profile'),
    url(r'^first_login/$', views.edit_profile, {'first_login':True}, name='first_login'),


    url(r'^letter/list/$', views.letters),
    url(r'^letter/send/$', views.send),
    url(r'^letter/receive/(?P<letter_id>\d+)/$', views.receive),

    url(r'^memo/create/$', views.create_memo, name='create_memo'),
    url(r'^memo/(?P<memo_id>\d+)/delete/$', views.delete_memo, name='delete_memo'),
    url(r'^memo/(?P<page>\d+)/$', views.memo, name='memo'),

    url(r'^news/(?P<page>\d+)/$', views.all_news, name='all_news'),    

    url(r'^search/(?P<board_id>\d+)/(?P<keyword>.+)/(?P<page>\d+)$', views.search, name='search'),
    url(r'^search_albums/(?P<keyword>.+)/(?P<page>\d+)/$', views.search_albums, name='search_albums'),

    # url(r'^man_won_bbang/$', views.man_won_bbang, name='man_won_bbang'),

    # url(r'^transform/user/$', 'transform_user'),
    # url(r'^transform/data/$', 'transform_data'),
    # url(r'^transform/column/$', 'transform_column'),
    # url(r'^transform/portfolio/$', 'transform_portfolio'),
    # url(r'^transform/analysis/$', 'transform_analysis'),
    # url(r'^transform/notice/$', 'transform_notice'),
    # url(r'^transform/board/$', 'transform_board'),
    # url(r'^transform/tf/$', 'transform_tf'),
    # url(r'^transform/research/$', 'transform_research'),
    # url(r'^transform/fund/$', 'transform_fund'),
    # url(r'^transform/photos/$', 'transform_photos'),
    # url(r'^transform/memo/$', 'transform_memo'),

    url(r'^taskforce/create/$', views.create_taskforce, name='create_taskforce'), # can make taskforce board 
    url(r'^taskforce/(?P<taskforce_id>\d+)/edit/$', views.edit_taskforce, name='edit_taskforce'),    
    url(r'^taskforce/archive/$', views.taskforce_archive, name='taskforce_archive'),

    url(r'^albums/page/(?P<page>\d+)/$', views.albums, name='albums'),
    url(r'^albums/(?P<album_id>\d+)/photos/$', views.photos, name='photos'),
    url(r'^albums/create/$', views.create_album, name='create_album'),
    url(r'^albums/(?P<album_id>\d+)/photos/create/$', views.create_photos, name='create_photos'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/edit/$', views.edit_photo, name='edit_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/delete/$', views.delete_photo, name='delete_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/recommend/$', views.recommend_photo, name='recommend_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/recommend/delete/$', views.delete_recommend_photo, name='delete_recommend_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/$', views.comment_photo, name='comment_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', views.delete_comment_photo, name='delete_comment_photo'),    
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', views.reply_comment_photo, name='reply_comment_photo'),
    url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', views.recommend_comment_photo, name='recommed_comment_photo'),
    
    
    url(r'^(?P<board>\w+)/news/(?P<page>\d+)/$', views.news, name='news'), # newest entries in member boards. every links to boards should be with page ( even 1)
    url(r'^(?P<board>\w+)/(?P<board_id>\d+)/page/(?P<page>\d+)/$', views.listing, name='listing'), # every member board is with page.
    url(r'^(?P<board>\w+)/(?P<board_id>\d+)/entry/create/$', views.create, name='create_in_board'), # to create entry in specific member board. include 'entry' to specify that it is about entry. and compatible with non-specific creation of board entry. views.pleasegive t a name.
    url(r'^(?P<board>\w+)/entry/create/$', views.create, name='create'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/$', views.read, name='read'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/reply/$', views.reply, name='reply'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/recommend/$', views.recommend, name='recommend'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/recommend/delete/$', views.delete_recommend, name='delete_recommend'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/$', views.comment, name='comment'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', views.delete_comment, name='delete_comment'),    
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', views.reply_comment, name='reply_comment'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', views.recommend_comment, name='recommend_comment'),
    #url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/delete/$', views.recommend_comment, name='recommend_comment')

    #도메인 이름 변경
    url(r'^Introduction/$', views.Introduction.as_view(), name="Public_Introduction"),
    url(r'^TopBar/$', views.TopBar_for_Visitor.as_view(), name="TopBar_for_Visitor")
]