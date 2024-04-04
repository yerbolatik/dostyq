from django.urls import reverse
import shortuuid

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from itertools import chain

from core.forms import GroupForm
from core.models import GroupPost, Post, Comment, ReplyComment, Friend, FriendRequest, Notification, ChatMessage, GroupChatMessage, GroupChat, Group
from userauths.models import User, Profile


# Notification Keys
noti_new_like = "New Like"
noti_new_follower = "New Follower"
noti_friend_request = "Friend Request"
noti_new_comment = "New Comment"
noti_comment_liked = "Comment Liked"
noti_comment_replied = "Comment Replied"
noti_friend_request_accepted = "Friend Request Accepted"


# Index Functions
@login_required
def index(request):
    posts = Post.objects.filter(
        active=True, visibility="Everyone").order_by("-id")
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        "posts": posts
    }
    return render(request, 'core/index.html', context)


@login_required
def post_detail(request, slug):
    post = Post.objects.get(slug=slug, active=True, visibility="Everyone")
    context = {
        "post": post
    }
    return render(request, 'core/post_detail.html', context)


@csrf_exempt
def create_post(request):

    if request.method == "POST":
        title = request.POST.get("post-caption")
        visibility = request.POST.get("visibility")
        image = request.FILES.get("post-thumbnail")

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()

            return JsonResponse({"post": {
                "title": post.title,
                "image": post.image.url,
                "full_name": post.user.profile.full_name,
                "profile_image": post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id,
            }})

        elif title:
            post = Post(
                title=title,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()

            return JsonResponse({"post": {
                "title": post.title,
                "full_name": post.user.profile.full_name,
                "profile_image": post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id,
            }})

        elif image:
            post = Post(
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            post.save()

            return JsonResponse({"post": {
                "image": post.image.url,
                "full_name": post.user.profile.full_name,
                "profile_image": post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id,
            }})

    return JsonResponse({"data": "sent"})


# Group Functions
def groups(request):
    user = request.user
    user_groups = Group.objects.filter(members=user)

    if user_groups.exists():
        only_me_groups = user_groups.filter(visibility="Only me")
        everyone_groups = user_groups.filter(visibility="Everyone")
        all_everyone_groups = Group.objects.filter(
            active=True, visibility="Everyone")
        groups = list(
            chain(only_me_groups, everyone_groups, all_everyone_groups))
    else:
        groups = Group.objects.filter(
            active=True, visibility="Everyone").order_by("-id")

    unique_groups = set(groups)

    max_members = max(unique_groups, key=lambda group: group.members.all(
    ).count()).members.all().count() if unique_groups else 0

    context = {
        "groups": unique_groups,
        "max_members": max_members
    }
    return render(request, 'core/groups.html', context)


def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST.get("group-caption")
            description = request.POST.get("group-description")
            image = request.FILES.get("group-thumbnail")
            visibility = request.POST.get("group-visibility")

            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            slug = slugify(name) + '-' + str(uniqueid.lower())

            group = Group(
                user=request.user,
                name=name,
                description=description,
                image=image,
                slug=slug,
                visibility=visibility
            )
            group.save()
            group.members.add(request.user)
            return redirect('core:group-index', slug=group.slug)
    else:
        form = GroupForm()
    return render(request, 'core/create-group.html', {'form': form})


def group_index(request, slug):
    group = Group.objects.get(slug=slug, active=True)
    group_posts = GroupPost.objects.filter(
        active=True, visibility="Everyone").order_by("-id")
    paginator = Paginator(group_posts, 3)
    page_number = request.GET.get('page')
    group_posts = paginator.get_page(page_number)
    context = {
        "group": group,
        "group_posts": group_posts
    }
    return render(request, 'core/group-index.html', context)


@csrf_exempt
def create_group_post(request):
    if request.method == "POST":
        group_id = request.POST.get("group_id")
        title = request.POST.get("group-post-caption")
        visibility = request.POST.get("group-post-visibility")
        image = request.FILES.get("group-post-thumbnail")

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        group = Group.objects.get(id=group_id)

        if title and image:
            group_post = GroupPost(
                group=group,
                title=title,
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            group_post.save()

            return JsonResponse({"post": {
                "title": group_post.title,
                "image": group_post.image.url,
                "full_name": group_post.user.profile.full_name,
                "profile_image": group_post.user.profile.image.url,
                "date": timesince(group_post.date),
                "id": group_post.id,
            }})

        elif title:
            group_post = GroupPost(
                title=title,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            group_post.save()

            return JsonResponse({"post": {
                "title": group_post.title,
                "full_name": group_post.user.profile.full_name,
                "profile_image": group_post.user.profile.image.url,
                "date": timesince(group_post.date),
                "id": group_post.id,
            }})

        elif image:
            group_post = GroupPost(
                visibility=visibility,
                image=image,
                user=request.user,
                slug=slugify(title) + '-' + str(uniqueid.lower())
            )
            group_post.save()

            return JsonResponse({"post": {
                "image": group_post.image.url,
                "full_name": group_post.user.profile.full_name,
                "profile_image": group_post.user.profile.image.url,
                "date": timesince(group_post.date),
                "id": group_post.id,
            }})

    return JsonResponse({"data": "sent"})


def join_group(request, slug):
    group = Group.objects.get(slug=slug, active=True, visibility="Everyone")
    member = request.user

    if request.method == "POST":
        group.members.add(member)
        return HttpResponseRedirect(reverse('core:group-index', args=[slug]))

    context = {
        "group": group
    }
    return render(request, 'core/group-index.html', context)


def send_notification(user, sender, post, comment, notification_type):
    notification = Notification.objects.create(
        user=user,
        sender=sender,
        post=post,
        comment=comment,
        notification_type=notification_type,
    )
    return notification


def update_notification_status(request):
    id = request.GET['id']
    notification = Notification.objects.get(id=id)

    notification.is_read = True
    notification.save()

    data = {
        "bool": notification.is_read,
    }
    return JsonResponse({"data": data})


def mark_as_read_all(request):
    if request.method == "POST":
        user = request.user
        notifications = Notification.objects.filter(user=user, is_read=False)
        notifications.update(is_read=True)

        return JsonResponse({"success": "All notifications marked as read."})
    else:
        return JsonResponse({"error": "Invalid request method."})


def like_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    user = request.user
    bool = False

    if user in post.likes.all():
        post.likes.remove(user)
        bool = False
    else:
        post.likes.add(user)
        bool = True

        if post.user != request.user:
            send_notification(post.user, user, post, None, noti_new_like)

    data = {
        "bool": bool,
        "likes": post.likes.all().count()
    }
    return JsonResponse({"data": data})


def comment_on_post(request):
    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post=post,
        comment=comment,
        user=user,
    )

    if new_comment.user != post.user:
        send_notification(post.user, user, post, new_comment, noti_new_comment)

    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image": new_comment.user.profile.image.url,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "post_id": new_comment.post.id,
        "comment_count": comment_count + int(1),
    }

    return JsonResponse({"data": data})


def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True

        if comment.user != user:
            send_notification(comment.user, user, comment.post,
                              comment, noti_comment_liked)

    data = {
        "bool": bool,
        "likes": comment.likes.all().count()
    }
    return JsonResponse({"data": data})


def reply_comment(request):
    id = request.GET['id']
    reply = request.GET['reply']

    comment = Comment.objects.get(id=id)
    user = request.user

    new_reply = ReplyComment.objects.create(
        reply=reply,
        comment=comment,
        user=user,
    )

    data = {
        "bool": True,
        "reply": new_reply.reply,
        "profile_image": new_reply.user.profile.image.url,
        "date": timesince(new_reply.date),
        "reply_id": new_reply.id,
        "post_id": new_reply.comment.post.id,
    }

    if comment.user != user:
        send_notification(comment.user, user, comment.post,
                          comment, noti_comment_replied)

    return JsonResponse({"data": data})


def delete_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    comment.delete()

    data = {
        "bool": True
    }
    return JsonResponse({"data": data})


def delete_reply(request):
    id = request.GET['id']
    reply = ReplyComment.objects.get(id=id)
    reply.delete()

    data = {
        "bool": True
    }
    return JsonResponse({"data": data})


# Friends actions
def add_friend(request):
    sender = request.user
    receiver_id = request.GET['id']
    bool = False

    if sender.id == int(receiver_id):
        return JsonResponse({"error": "You cannot send a friend request to yourself"})

    receiver = User.objects.get(id=receiver_id)

    try:
        friend_request = FriendRequest.objects.get(
            sender=sender, receiver=receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({"error": "Cancelled", "bool": bool})
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True

        send_notification(receiver, sender, None, None, noti_friend_request)

        return JsonResponse({"success": "Sent", "bool": bool})


def unfriend(request):
    sender = request.user
    friend_id = request.GET['id']
    bool = False

    if sender.id == int(friend_id):
        return JsonResponse({"error": "You cannot unfriend yourself"})

    my_friend = User.objects.get(id=friend_id)

    if my_friend in sender.profile.friends.all():
        sender.profile.friends.remove(my_friend)
        my_friend.profile.friends.remove(sender)
        bool = True
        return JsonResponse({"success": "Unfriend successfull.", "bool": bool})


def accept_friend_request(request):
    id = request.GET['id']

    receiver = request.user
    sender = User.objects.get(id=id)

    friend_request = FriendRequest.objects.filter(
        receiver=receiver, sender=sender).first()

    receiver.profile.friends.add(sender)
    sender.profile.friends.add(receiver)

    friend_request.delete()

    send_notification(sender, receiver, None, None,
                      noti_friend_request_accepted)

    data = {
        "message": "Accepted",
        "bool": True,
    }
    return JsonResponse({"data": data})


def reject_friend_request(request):
    id = request.GET['id']

    receiver = request.user
    sender = User.objects.get(id=id)

    friend_request = FriendRequest.objects.filter(
        receiver=receiver, sender=sender).first()
    friend_request.delete()

    data = {
        "message": "Rejected",
        "bool": True,
    }
    return JsonResponse({"data": data})


def block_user(request):
    id = request.GET['id']
    user = request.user
    friend = User.objects.get(id=id)

    if user.id == friend.id:
        return JsonResponse({"error": "You cannot block yourself"})

    if friend in user.profile.friends.all():
        user.profile.blocked.add(friend)
        user.profile.friends.remove(friend)
        friend.profile.friends.remove(user)
    else:
        return JsonResponse({"error": "You cannot block someone that is not your friend"})

    return JsonResponse({"success": "User blocked"})

# Messanger actions


@login_required
def inbox(request):
    user_id = request.user
    chat_message = ChatMessage.objects.filter(
        id__in=Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) |
                Q(receiver__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef("id"), receiver=user_id) |
                        Q(receiver=OuterRef("id"), sender=user_id)
                    ).order_by("-id")[:1].values_list("id", flat=True)
                )
            ).values_list("last_msg", flat=True).order_by("-id")
        )
    ).order_by("-id")

    context = {
        "chat_message": chat_message,
    }
    return render(request, "chat/inbox.html", context)


def inbox_detail(request, username):
    user_id = request.user
    message_list = ChatMessage.objects.filter(
        id__in=Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) |
                Q(receiver__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef("id"), receiver=user_id) |
                        Q(receiver=OuterRef("id"), sender=user_id)
                    ).order_by("-id")[:1].values_list("id", flat=True)
                )
            ).values_list("last_msg", flat=True).order_by("-id")
        )
    ).order_by("-id")

    sender = request.user
    receiver = User.objects.get(username=username)
    receiver_details = User.objects.get(username=username)

    message_detail = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(
            receiver=sender, sender=receiver)
    ).order_by("date")

    message_detail.update(is_read=True)

    if message_detail:
        r = message_detail.first()
        receiver = User.objects.get(username=r.receiver)
    else:
        receiver = User.objects.get(username=username)

    context = {
        "message_list": message_list,
        "sender": sender,
        "receiver": receiver,
        "receiver_details": receiver_details,
        "message_detail": message_detail,
    }
    return render(request, "chat/inbox_detail.html", context)


@login_required
def group_inbox(request):
    groupchat = GroupChat.objects.filter(
        members__in=User.objects.filter(pk=request.user.pk), active=True)
    print("groupchat =============", groupchat)
    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/group_inbox.html', context)


@login_required
def group_inbox_detail(request, slug):
    groupchat_list = GroupChat.objects.filter(
        members__in=User.objects.filter(pk=request.user.pk), active=True)
    groupchat = GroupChat.objects.get(slug=slug, active=True)
    group_messages = GroupChatMessage.objects.filter(
        groupchat=groupchat).order_by("id")

    if request.user not in groupchat.members.all():
        return redirect("core:join_group_chat_page", groupchat.slug)

    context = {
        'groupchat': groupchat,
        'group_name': groupchat.slug,
        'group_messages': group_messages,
        'groupchat_list': groupchat_list,
    }
    return render(request, 'chat/group_inbox_detail.html', context)


def join_group_chat_page(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    context = {
        'groupchat': groupchat,
    }
    return render(request, 'chat/join_group_chat_page.html', context)


def join_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        return redirect("core:group_inbox_detail", groupchat.slug)

    groupchat.members.add(request.user)
    return redirect("core:group_inbox_detail", groupchat.slug)


def leave_group_chat(request, slug):
    groupchat = GroupChat.objects.get(slug=slug, active=True)

    if request.user in groupchat.members.all():
        groupchat.members.remove(request.user)
        return redirect("core:join_group_chat_page", groupchat.slug)

    return redirect("core:join_group_chat_page", groupchat.slug)


def search_users(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(
            email__icontains=query) | User.objects.filter(full_name__icontains=query)

        users_data = []
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                profile_image = profile.image.url
                full_name = profile.full_name
            except Profile.DoesNotExist:
                profile_image = None
                full_name = None

            user_data = {
                'username': user.username,
                'full_name': full_name,
                'email': user.email,
                'profile_image': profile_image,
            }
            users_data.append(user_data)
    else:
        users_data = []
    return JsonResponse({'users': users_data})


def games(request):
    return render(request, 'games/all_games.html')


def stack_brick(request):
    return render(request, 'games/stack_brick.html')


def snake(request):
    return render(request, 'games/snake.html')


def load_more_posts(request):
    all_posts = Post.objects.filter(
        active=True, visibility="Everyone").order_by('-date')

    # Paginate the posts
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    posts_data = []
    for post in page_obj:
        post_data = {
            'title': post.title,
            'profile_image': post.user.profile.image.url,
            'full_name': post.user.profile.full_name,
            'image_url': post.image.url if post.image else None,
            'video': post.video.url if post.video else None,
            'id': post.id,
            'id': post.id,
            'likes': post.likes.count(),
            'slug': post.slug,
            'views': post.views,
            'date': timesince(post.date),
        }
        posts_data.append(post_data)

    return JsonResponse({'posts': posts_data})


def photos(request):
    photos = Post.objects.filter(
        active=True, visibility="Everyone").order_by("-id")
    posts = Post.objects.filter(
        active=True, visibility="Everyone").order_by("-id")

    context = {
        "photos": photos,
        "posts": posts,

    }
    return render(request, 'core/photos.html', context)
