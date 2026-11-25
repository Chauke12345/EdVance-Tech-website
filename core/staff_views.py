from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.models import Enquiry
from client_portal.models import ProjectRequest
from client_portal.quotation_models import Quotation
from contracts.models import Contract


@staff_member_required(login_url="/portal/login/")
def staff_dashboard(request):
    context = {
        "total_clients": User.objects.filter(is_staff=False).count(),
        "new_enquiries": Enquiry.objects.filter(is_reviewed=False).count(),
        "total_enquiries": Enquiry.objects.count(),
        "total_projects": ProjectRequest.objects.count(),
        "active_projects": ProjectRequest.objects.filter(status="In progress").count(),
        "pending_projects": ProjectRequest.objects.filter(
            status__in=["Submitted", "Under review"]
        ).count(),
        "pending_quotations": Quotation.objects.filter(status="Sent").count(),
        "pending_contracts": Contract.objects.filter(status__in=["Sent", "Viewed"]).count(),
    }
    return render(request, "core/staff_dashboard.html", context)


@staff_member_required(login_url="/portal/login/")
def staff_enquiry_list(request):
    enquiries = Enquiry.objects.all()
    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if search:
        enquiries = enquiries.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(service__icontains=search)
            | Q(message__icontains=search)
        )

    if status == "new":
        enquiries = enquiries.filter(is_reviewed=False)
    elif status == "reviewed":
        enquiries = enquiries.filter(is_reviewed=True)
    else:
        status = "all"

    context = {
        "enquiries": enquiries,
        "search": search,
        "selected_status": status,
        "total_enquiries": Enquiry.objects.count(),
        "new_enquiries": Enquiry.objects.filter(is_reviewed=False).count(),
        "reviewed_enquiries": Enquiry.objects.filter(is_reviewed=True).count(),
    }
    return render(request, "core/staff_enquiry_list.html", context)


@staff_member_required(login_url="/portal/login/")
def staff_enquiry_detail(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    return render(
        request,
        "core/staff_enquiry_detail.html",
        {"enquiry": enquiry},
    )


@staff_member_required(login_url="/portal/login/")
@require_POST
def staff_enquiry_review(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    enquiry.is_reviewed = not enquiry.is_reviewed
    enquiry.save(update_fields=["is_reviewed"])

    if enquiry.is_reviewed:
        messages.success(request, "Enquiry marked as reviewed.")
    else:
        messages.success(request, "Enquiry returned to new status.")

    return redirect("staff_enquiry_detail", enquiry_id=enquiry.pk)

# ==========================================================
# CLIENT ACCOUNT MANAGEMENT
# ==========================================================

from django.core.paginator import Paginator


@staff_member_required(login_url="/portal/login/")
def staff_client_list(request):
    clients = User.objects.filter(is_staff=False).order_by("-date_joined")

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if search:
        clients = clients.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

    if status == "active":
        clients = clients.filter(is_active=True)
    elif status == "inactive":
        clients = clients.filter(is_active=False)
    else:
        status = "all"

    paginator = Paginator(clients, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "total_clients": User.objects.filter(is_staff=False).count(),
        "active_clients": User.objects.filter(
            is_staff=False, is_active=True
        ).count(),
        "inactive_clients": User.objects.filter(
            is_staff=False, is_active=False
        ).count(),
    }

    return render(request, "core/staff_client_list.html", context)


@staff_member_required(login_url="/portal/login/")
def staff_client_detail(request, client_id):
    client = get_object_or_404(
        User,
        pk=client_id,
        is_staff=False
    )

    projects = ProjectRequest.objects.filter(
        client=client
    ).order_by("-created_at")

    quotations = Quotation.objects.filter(
        project__client=client
    ).select_related("project").order_by("-created_at")

    context = {
        "client": client,
        "projects": projects,
        "quotations": quotations,
        "total_projects": projects.count(),
        "total_quotations": quotations.count(),
    }

    return render(request, "core/staff_client_detail.html", context)

# ==========================================================
# STAFF QUOTATION MANAGEMENT
# ==========================================================

from django.utils import timezone
from core.forms import StaffQuotationForm


@staff_member_required(login_url="/portal/login/")
def staff_quotation_list(request):
    quotations = Quotation.objects.select_related(
        "project", "project__client"
    ).all()

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if search:
        quotations = quotations.filter(
            Q(project__project_title__icontains=search)
            | Q(project__client__username__icontains=search)
            | Q(project__client__first_name__icontains=search)
            | Q(project__client__last_name__icontains=search)
            | Q(project__client__email__icontains=search)
        )

    valid_statuses = [choice[0] for choice in Quotation.STATUS_CHOICES]
    if status in valid_statuses:
        quotations = quotations.filter(status=status)
    else:
        status = "all"

    paginator = Paginator(quotations, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "total_quotations": Quotation.objects.count(),
        "draft_quotations": Quotation.objects.filter(status="Draft").count(),
        "sent_quotations": Quotation.objects.filter(status="Sent").count(),
        "accepted_quotations": Quotation.objects.filter(status="Accepted").count(),
        "declined_quotations": Quotation.objects.filter(status="Declined").count(),
        "expired_quotations": Quotation.objects.filter(status="Expired").count(),
        "status_choices": Quotation.STATUS_CHOICES,
    }

    return render(request, "core/staff_quotation_list.html", context)


@staff_member_required(login_url="/portal/login/")
def staff_quotation_create(request):
    if request.method == "POST":
        form = StaffQuotationForm(request.POST)
        if form.is_valid():
            quotation = form.save(commit=False)
            quotation.status = "Draft"
            quotation.save()
            messages.success(
                request,
                f"Quotation {quotation.reference_number} created as a draft."
            )
            return redirect("staff_quotation_detail", quotation_id=quotation.pk)
    else:
        form = StaffQuotationForm()

    return render(
        request,
        "core/staff_quotation_form.html",
        {"form": form, "page_heading": "Create Quotation"},
    )


@staff_member_required(login_url="/portal/login/")
def staff_quotation_detail(request, quotation_id):
    quotation = get_object_or_404(
        Quotation.objects.select_related("project", "project__client"),
        pk=quotation_id,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "send":
            if quotation.status != "Draft":
                messages.error(
                    request,
                    "Only draft quotations can be sent."
                )
                return redirect(
                    "staff_quotation_detail",
                    quotation_id=quotation.pk,
                )

            if quotation.valid_until and quotation.valid_until < timezone.localdate():
                messages.error(
                    request,
                    "This quotation's validity date has passed. Update it before sending."
                )
                return redirect(
                    "staff_quotation_detail",
                    quotation_id=quotation.pk,
                )

            quotation.status = "Sent"
            quotation.save(update_fields=["status", "updated_at"])

            project = quotation.project
            if project.status in ["Submitted", "Under review"]:
                project.status = "Quotation sent"
                project.save(update_fields=["status"])

            messages.success(
                request,
                "Quotation sent to the client's portal successfully."
            )
            return redirect(
                "staff_quotation_detail",
                quotation_id=quotation.pk,
            )

        if action == "save":
            if quotation.status != "Draft":
                messages.error(
                    request,
                    "Only draft quotations can be edited."
                )
                return redirect(
                    "staff_quotation_detail",
                    quotation_id=quotation.pk,
                )

            form = StaffQuotationForm(request.POST, instance=quotation)
            if form.is_valid():
                form.save()
                messages.success(request, "Draft quotation updated.")
                return redirect(
                    "staff_quotation_detail",
                    quotation_id=quotation.pk,
                )
        else:
            messages.error(request, "Invalid quotation action.")
            return redirect(
                "staff_quotation_detail",
                quotation_id=quotation.pk,
            )
    else:
        form = StaffQuotationForm(instance=quotation)

    return render(
        request,
        "core/staff_quotation_detail.html",
        {
            "quotation": quotation,
            "form": form,
        },
    )

# ==========================================================
# STAFF PROJECT MANAGEMENT
# ==========================================================

@staff_member_required(login_url="/portal/login/")
def staff_project_list(request):
    projects = ProjectRequest.objects.select_related("client").all()

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    if search:
        projects = projects.filter(
            Q(project_title__icontains=search)
            | Q(business_name__icontains=search)
            | Q(service__icontains=search)
            | Q(client__username__icontains=search)
            | Q(client__first_name__icontains=search)
            | Q(client__last_name__icontains=search)
            | Q(client__email__icontains=search)
        )

    valid_statuses = [choice[0] for choice in ProjectRequest.STATUS_CHOICES]

    if status in valid_statuses:
        projects = projects.filter(status=status)
    else:
        status = "all"

    paginator = Paginator(projects, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "status_choices": ProjectRequest.STATUS_CHOICES,
        "total_projects": ProjectRequest.objects.count(),
        "submitted_projects": ProjectRequest.objects.filter(status="Submitted").count(),
        "under_review_projects": ProjectRequest.objects.filter(status="Under review").count(),
        "quotation_sent_projects": ProjectRequest.objects.filter(status="Quotation sent").count(),
        "active_projects": ProjectRequest.objects.filter(status="In progress").count(),
        "completed_projects": ProjectRequest.objects.filter(status="Completed").count(),
        "declined_projects": ProjectRequest.objects.filter(status="Declined").count(),
    }

    return render(request, "core/staff_project_list.html", context)


@staff_member_required(login_url="/portal/login/")
def staff_project_detail(request, project_id):
    project = get_object_or_404(
        ProjectRequest.objects.select_related("client"),
        pk=project_id,
    )

    if request.method == "POST":
        new_status = request.POST.get("status", "").strip()
        valid_statuses = dict(ProjectRequest.STATUS_CHOICES)

        if new_status not in valid_statuses:
            messages.error(request, "Please select a valid project status.")
        elif new_status == project.status:
            messages.info(request, "The project is already in that status.")
        else:
            old_status = project.status
            project.status = new_status
            project.save(update_fields=["status"])

            messages.success(
                request,
                f"Project status updated from {old_status} to {new_status}."
            )

        return redirect("staff_project_detail", project_id=project.pk)

    quotations = Quotation.objects.filter(
        project=project
    ).order_by("-created_at")

    context = {
        "project": project,
        "quotations": quotations,
        "status_choices": ProjectRequest.STATUS_CHOICES,
    }

    return render(request, "core/staff_project_detail.html", context)

