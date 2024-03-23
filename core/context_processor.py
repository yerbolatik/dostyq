from core.models import FriendRequest, Notification, ChatMessage
from userauths.models import User
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField


def my_context_processor(request):
    try:
        friend_request = FriendRequest.objects.filter(
            receiver=request.user).order_by("-id")
    except:
        friend_request = None

    try:
        notification = Notification.objects.filter(
            user=request.user).order_by("-id")
    except:
        notification = None

    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user, is_read=False).count()
    else:
        unread_count = 0

    try:
        user_id = request.user

        chat_message = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id) |
                    Q(reciever__sender=user_id)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), reciever=user_id) |
                            Q(reciever=OuterRef('id'), sender=user_id)
                        ).order_by('-id')[:1].values_list('id', flat=True)
                    )
                ).values_list('last_msg', flat=True).order_by("-id")
            )
        ).order_by("-id")
    except:
        chat_message = None

    return {
        "friend_request": friend_request,
        "notification": notification,
        "unread_count": unread_count,
        "chat_message": chat_message,
    }
