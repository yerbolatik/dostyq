from core.models import FriendRequest, Notification, ChatMessage
from userauths.models import User
from django.db.models import OuterRef, Subquery
from django.db.models import Q, Count, Sum, F, FloatField


def my_context_processor(request):
    unread_messages = []
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
        unread_message_count = ChatMessage.objects.filter(
            receiver=request.user, is_read=False).count()
        unread_messages = ChatMessage.objects.filter(
            receiver=request.user, is_read=False)
    else:
        unread_count = 0
        unread_message_count = 0

    try:
        user_id = request.user

        chat_message = ChatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever=user_id, is_read=False) |
                    Q(reciever__sender=user_id, is_read=False)
                ).distinct().annotate(
                    last_msg=Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef("id"), reciever=user_id, is_read=False) |
                            Q(reciever=OuterRef("id"),
                              sender=user_id, is_read=False)
                        ).order_by("-id")[:1].values_list("id", flat=True)
                    )
                ).values_list("last_msg", flat=True).order_by("-id")
            )
        ).order_by("-id")
    except:
        chat_message = None

    return {
        "friend_request": friend_request,
        "notification": notification,
        "unread_count": unread_count,
        "unread_message_count": unread_message_count,
        "chat_message": chat_message,
        "unread_messages": unread_messages,
    }
