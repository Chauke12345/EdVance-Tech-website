from .models import Message


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {"unread_message_count": 0}

    unread = Message.objects.filter(
        is_read=False
    ).exclude(sender=request.user)

    if request.user.is_staff:
        count = unread.filter(
            conversation__client__isnull=False
        ).count()
    else:
        count = unread.filter(
            conversation__client=request.user
        ).count()

    return {"unread_message_count": count}
