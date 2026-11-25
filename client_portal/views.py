from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import ClientRegistrationForm, ProjectRequestForm
from .models import ProjectRequest


def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_dashboard')
    else:
        form = ClientRegistrationForm()

    return render(request, 'client_portal/register.html', {
        'form': form
    })


@login_required
def dashboard(request):
    from contracts.models import Contract

    projects = ProjectRequest.objects.filter(
        client=request.user
    )

    contracts = Contract.objects.filter(
        client=request.user
    ).select_related("project").order_by("-created_at")

    context = {
        "projects": projects,
        "total_projects": projects.count(),
        "awaiting_review": projects.filter(
            status__in=["Submitted", "Under review"]
        ).count(),
        "in_progress": projects.filter(
            status="In progress"
        ).count(),
        "completed_projects": projects.filter(
            status="Completed"
        ).count(),
        "contracts": contracts,
        "total_contracts": contracts.count(),
        "pending_contracts": contracts.filter(
            status__in=["Sent", "Viewed"]
        ).count(),
        "signed_contracts": contracts.filter(
            status="Signed"
        ).count(),
    }

    return render(request, "client_portal/dashboard.html", context)

@login_required
def project_submit(request):
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            return redirect('client_dashboard')
    else:
        form = ProjectRequestForm()

    return render(request, 'client_portal/project_submit.html', {
        'form': form
    })



@login_required
def my_quotations(request):
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from .quotation_models import Quotation

    quotations = Quotation.objects.filter(
        project__client=request.user
    ).exclude(status='Draft').select_related('project')

    if request.method == 'POST':
        quotation_id = request.POST.get('quotation_id')
        action = request.POST.get('action')

        quotation = get_object_or_404(
            Quotation,
            pk=quotation_id,
            project__client=request.user,
            status='Sent'
        )

        if action == 'accept':
            quotation.status = 'Accepted'
            quotation.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Quotation accepted successfully.')

        elif action == 'decline':
            quotation.status = 'Declined'
            quotation.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Quotation declined.')

        else:
            messages.error(request, 'Invalid quotation action.')

        return redirect('my_quotations')

    return render(request, 'client_portal/quotations.html', {
        'quotations': quotations,
    })


from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Conversation, Message


@login_required
def message_inbox(request):
    if request.user.is_staff:
        conversations = Conversation.objects.select_related(
            "client", "project"
        ).all()
        available_projects = ProjectRequest.objects.select_related(
            "client"
        ).all()
    else:
        conversations = Conversation.objects.filter(
            client=request.user
        ).select_related("client", "project")
        available_projects = ProjectRequest.objects.filter(
            client=request.user
        )

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        subject = request.POST.get("subject", "").strip()

        if request.user.is_staff:
            project = get_object_or_404(ProjectRequest, pk=project_id)
        else:
            project = get_object_or_404(
                ProjectRequest,
                pk=project_id,
                client=request.user
            )

        if not subject:
            messages.error(request, "Please enter a conversation subject.")
        else:
            conversation = Conversation.objects.create(
                project=project,
                client=project.client,
                subject=subject
            )
            return redirect(
                "conversation_detail",
                conversation_id=conversation.pk
            )

    for conversation in conversations:
        conversation.unread_count = conversation.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()

    return render(request, "client_portal/message_inbox.html", {
        "conversations": conversations,
        "available_projects": available_projects,
    })


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.select_related("client", "project"),
        pk=conversation_id
    )

    if not request.user.is_staff and conversation.client_id != request.user.id:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot access this conversation.")

    if request.method == "POST":
        body = request.POST.get("body", "").strip()

        if body:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=body
            )
            conversation.save(update_fields=["updated_at"])
            return redirect(
                "conversation_detail",
                conversation_id=conversation.pk
            )
        messages.error(request, "Please enter a message.")

    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(
        is_read=True,
        read_at=timezone.now()
    )

    conversation_messages = conversation.messages.select_related(
        "sender"
    ).all()

    return render(request, "client_portal/conversation_detail.html", {
        "conversation": conversation,
        "conversation_messages": conversation_messages,
    })

from django.http import JsonResponse, HttpResponseForbidden

@login_required
def conversation_updates(request, conversation_id):
    conversation = get_object_or_404(
        Conversation.objects.select_related("client", "project"),
        pk=conversation_id
    )

    if not request.user.is_staff and conversation.client_id != request.user.id:
        return HttpResponseForbidden("You do not have permission to view this conversation.")

    # Mark incoming messages as read while this conversation is open.
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(
        is_read=True,
        read_at=timezone.now()
    )

    try:
        last_id = int(request.GET.get("after", 0))
    except (TypeError, ValueError):
        last_id = 0

    new_messages = Message.objects.filter(
        conversation=conversation,
        id__gt=last_id
    ).select_related("sender").order_by("created_at")

    messages_data = [
        {
            "id": message.id,
            "sender_id": message.sender_id,
            "sender_name": message.sender.get_full_name() or message.sender.username,
            "body": message.body,
            "created_at": message.created_at.strftime("%d %b %Y, %H:%M"),
            "is_read": message.is_read,
        }
        for message in new_messages
    ]

    read_ids = list(
        Message.objects.filter(
            conversation=conversation,
            sender=request.user,
            is_read=True
        ).values_list("id", flat=True)
    )

    unread = Message.objects.filter(is_read=False).exclude(sender=request.user)

    if request.user.is_staff:
        unread_count = unread.count()
    else:
        unread_count = unread.filter(conversation__client=request.user).count()

    return JsonResponse({
        "messages": messages_data,
        "read_ids": read_ids,
        "unread_count": unread_count,
    })


@login_required
def notification_count(request):
    unread = Message.objects.filter(is_read=False).exclude(sender=request.user)

    if request.user.is_staff:
        count = unread.count()
    else:
        count = unread.filter(conversation__client=request.user).count()

    return JsonResponse({"unread_count": count})

