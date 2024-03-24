from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='feed'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),

    # Chat
    path('core/inbox/', views.inbox, name='inbox'),
    path('core/inbox/<username>/', views.inbox_detail, name='inbox_detail'),

    # Search
    path('search/', views.search_users, name='search_users'),


    # Ajax URLs
    path('create-post/', views.create_post, name='create-post'),
    path('like-post/', views.like_post, name='like-post'),
    path('comment-post/', views.comment_on_post, name='comment-post'),
    path('like-comment/', views.like_comment, name='like-comment'),
    path('reply-comment/', views.reply_comment, name='reply-comment'),
    path('delete-comment/', views.delete_comment, name='delete-comment'),
    path('delete-reply/', views.delete_reply, name='delete-reply'),
    path('add-friend/', views.add_friend, name='add-friend'),
    path('unfriend/', views.unfriend, name='unfriend'),
    path('accept-friend-request/', views.accept_friend_request,
         name='accept-friend-request'),
    path('reject-friend-request/', views.reject_friend_request,
         name='reject-friend-request'),
    path('block-user/', views.block_user, name='block-user'),
    path('update-notification/', views.update_notification_status,
         name='update-notification'),
    path('mark-as-read-all/', views.mark_as_read_all, name='mark-as-read-all'),
]
