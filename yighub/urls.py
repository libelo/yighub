from django.conf.urls import patterns, include, url

urlpatterns = patterns('yighub.views',
    url(r'^$', 'home'),
    url(r'^home/$', 'home', name='home'),

    url(r'^join/$', 'join', name='join'),
    url(r'^login/$', 'login', name='login'),
    url(r'^login_check/$', 'login_check', name='login_check'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^profile/$', 'edit_profile', name='edit_profile'),

    url(r'^letter/list/$', 'letters'),
    url(r'^letter/send/$', 'send'),
    url(r'^letter/receive/(?P<letter_id>\d+)/$', 'receive'),
    url(r'^letter/receive/(?P<letter_id>\d+)/download/$', 'download_letter'),

    url(r'^memo/create/$', 'create_memo', name='create_memo'),
    url(r'^memo/(?P<memo_id>\d+)/delete/$', 'delete_memo', name='delete_memo'),
    url(r'^memo/(?P<page>\d+)/$', 'memo', name='memo'),

    url(r'^download/(?P<file_id>\d+)/$', 'download', name='download'),

    url(r'^taskforce/create/$', 'create_taskforce', name='create_taskforce'), # can make taskforce board 

    url(r'^albums/$', 'albums', {'page' : 1}, name='albums'),
    url(r'^albums/page/(?P<page>\d+)/$', 'albums'),
    url(r'^albums/(?P<album_id>\d+)/photos/$', 'photos', name='photos'),
    #url(r'^albums/create/$', 'create_album', name='create_album'),
    #url(r'^albums/(?P<album_id>\d+)/photos/create/$', 'create_photos', name='create_photos'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/edit/$', 'edit_photo', name='edit_photo'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/delete/$', 'delete_photo', name='delete_photo'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/recommend/$', 'recommed_photo', name='recommend_photo'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/$', 'comment_photo', name='comment_photo'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/(?P<comment_id>\d+)/reply$', 'reply_comment_photo', name='reply_comment_photo'),
    #url(r'^albums/(?P<album_id>\d+)/photos/(?P<photo_id>\d+)/comment/(?P<comment_id>\d+)/recommend$', 'recommend_comment_photo', name='recommed_comment_photo'),
    
    
    url(r'^(?P<board>\w+)/news/(?P<page>\d+)/$', 'news', name='news'), # newest entries in member boards. every links to boards should be with page ( even 1)
    url(r'^(?P<board>\w+)/(?P<board_id>\d+)/page/(?P<page>\d+)/$', 'listing', name='listing'), # every member board is with page.
    url(r'^(?P<board>\w+)/(?P<board_id>\d+)/entry/create/$', 'create', name='create_in_board'), # to create entry in specific member board. include 'entry' to specify that it is about entry. and compatible with non-specific creation of board entry. please give it a name.
    url(r'^(?P<board>\w+)/entry/create/$', 'create', name='create'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/$', 'read', name='read'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/edit/$', 'edit', name='edit'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/reply/$', 'reply', name='reply'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/recommend/$', 'recommend', name='recommend'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/$', 'comment', name='comment'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', 'delete_comment', name='delete_comment'),    
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', 'reply_comment', name='reply_comment'),
    url(r'^(?P<board>\w+)/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', 'recommend_comment', name='recommend_comment'),
)

    # url(r'^boards/news/(?P<page>\d+)/$', news, {'board' : 'bulletin'}, name='news_bulletin') # newest entries in member boards. every links to boards should be with page ( even 1)
    # url(r'^boards/(?P<board_id>\d+)/(?P<page>\d+)/$', listing, {'board' : 'bulletin'}, name='listing_bulletin') # every member board is with page.
    # url(r'^boards/(?P<board_id>\d+)/entry/create/$', create, {'board' : 'bulletin'}, name='create_specific_bulletin') # to create entry in specific member board. include 'entry' to specify that it is about entry. and compatible with non-specific creation of board entry. please give it a name.
    # url(r'^boards/entry/create/$', create, {'board' : 'bulletin'}, name='create_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/$', read, {'board' : 'bulletin'}, name='read_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/edit/$', edit, {'board' : 'bulletin'}, name='edit_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/reply/$', reply, {'board' : 'bulletin'}, name='reply_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/recommend/$', recommend, {'board' : 'bulletin'}, name='recommend_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/comment/$', comment, {'board' : 'bulletin'}, name='comment_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', reply_comment, {'board' : 'bulletin'}, name='reply_comment_bulletin')
    # url(r'^boards/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', recommend_comment, {'board' : 'bulletin'}, , name='recommend_comment_bulletin')

    # url(r'^taskforce/news/(?P<page>\d+)/$', news, {'board' : 'taskforce'}, name='news_taskforce') 
    # url(r'^taskforce/create/$', create, {'board' : 'taskforce'}, name='create_board_taskforce') # can make taskforce board 
    # url(r'^taskforce/(?P<board_id>\d+)/(?P<page>\d+)/$', listing, {'board' : 'taskforce'}, name='listing_taskforce') 
    # url(r'^taskforce/(?P<board_id>\d+)/entry/create/$', create, {'board' : 'taskforce'}, name='create_specific_taskforce') 
    # url(r'^taskforce/entry/create/$', create, {'board' : 'taskforce'}, name='create_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/$', read, {'board' : 'taskforce'}, name='read_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/edit/$', edit, {'board' : 'taskforce'}, name='edit_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/reply/$', reply, {'board' : 'taskforce'}, name='reply_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/recommend/$', recommend, {'board' : 'taskforce'}, name='recommend_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/comment/$', comment, {'board' : 'taskforce'}, name='comment_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', reply_comment, {'board' : 'taskforce'}, name='reply_comment_taskforce')
    # url(r'^taskforce/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', recommend_comment, {'board' : 'taskforce'}, , name='recommend_comment_taskforce')

    # # public doesn't have news
    # url(r'^public/(?P<board_id>\d+)/(?P<page>\d+)/$', listing, {'board' : 'public'}, name='listing_public') # pages are most useless but ok.
    # url(r'^public/(?P<board_id>\d+)/entry/create/$', create, {'board' : 'public'}, name='create_specific_public') 
    # url(r'^public/entry/create/$', create, {'board' : 'public'}, name='create_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/$', read, {'board' : 'public'}, name='read_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/edit/$', edit, {'board' : 'public'}, name='edit_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/reply/$', reply, {'board' : 'public'}, name='reply_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/recommend/$', recommend, {'board' : 'public'}, name='recommend_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/comment/$', comment, {'board' : 'public'}, name='comment_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/reply/$', reply_comment, {'board' : 'public'}, name='reply_comment_public')
    # url(r'^public/entry/(?P<entry_id>\d+)/comment/(?P<comment_id>\d+)/recommend/$', recommend_comment, {'board' : 'public'}, , name='recommend_comment_public')
