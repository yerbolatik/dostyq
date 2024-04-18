from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='feed'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('groups/', views.groups, name='groups'),
    path('create-group/', views.create_group, name='create-group'),
    path('group-index/<slug:slug>/', views.group_index, name='group-index'),
    path('join-group/<slug:slug>/', views.join_group, name='join-group'),
    path('unfollow-group/<slug:slug>/',
         views.unfollow_group, name='unfollow-group'),
    path('photos/', views.photos, name='photos'),

    # Chat
    path('core/inbox/', views.inbox, name='inbox'),
    path('core/inbox/<username>/', views.inbox_detail, name='inbox_detail'),

    # Group Chat
    path("core/group-inbox/", views.group_inbox, name="group_inbox"),
    path("core/create-groupchat/", views.create_groupchat, name="create-groupchat"),
    path("core/group-inbox/<slug:slug>/",
         views.group_inbox_detail, name="group_inbox_detail"),

    # Join & leave Group Chat
    path("core/join-group-page/<slug:slug>/",
         views.join_group_chat_page, name="join_group_chat_page"),
    path("core/join-group/<slug:slug>/",
         views.join_group_chat, name="join_group"),
    path("core/leave-group/<slug:slug>/",
         views.leave_group_chat, name="leave_group_chat"),

    # Search
    path('search/', views.search_users, name='search_users'),

    # Games
    path("all-games/", views.games, name="games"),
    path("stack_brick/", views.stack_brick, name="stack_brick"),
    path("snake/", views.snake, name="snake"),

    # Load more post
    path('load_more_posts/', views.load_more_posts, name='load_more_posts'),




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

    path('create-group-post/', views.create_group_post, name='create-group-post'),

]
