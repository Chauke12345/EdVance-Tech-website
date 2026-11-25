from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Contract, DigitalSignature


@login_required
def contract_list(request):
    if request.user.is_staff:
        contracts = Contract.objects.select_related(
            "client", "project", "quotation"
        ).all()
    else:
        contracts = Contract.objects.filter(
            client=request.user
        ).select_related("project", "quotation")

    return render(
        request,
        "contracts/contract_list.html",
        {"contracts": contracts}
    )


@login_required
def contract_detail(request, contract_id):
    contract = get_object_or_404(
        Contract.objects.select_related("client", "project", "quotation"),
        pk=contract_id
    )

    if not request.user.is_staff and contract.client_id != request.user.id:
        return HttpResponseForbidden("You cannot access this contract.")

    if contract.status == "Sent":
        contract.status = "Viewed"
        contract.viewed_at = timezone.now()
        contract.save(update_fields=["status", "viewed_at", "updated_at"])

    if request.method == "POST":
        if request.user.is_staff or contract.client_id != request.user.id:
            return HttpResponseForbidden("Only the client can sign this contract.")

        if contract.status not in ["Sent", "Viewed"]:
            return HttpResponseForbidden("This contract is not available for signing.")

        if contract.valid_until and contract.valid_until < timezone.localdate():
            return HttpResponseForbidden("This contract has expired.")

        signer_name = request.POST.get("signer_full_name", "").strip()
        typed_signature = request.POST.get("typed_signature", "").strip()
        accepted = request.POST.get("accept_terms") == "on"

        if not signer_name or not typed_signature or not accepted:
            return render(
                request,
                "contracts/contract_detail.html",
                {
                    "contract": contract,
                    "error": "Enter your full name, type your signature and confirm acceptance."
                }
            )

        if DigitalSignature.objects.filter(contract=contract).exists():
            return HttpResponseForbidden("This contract has already been signed.")

        with transaction.atomic():
            DigitalSignature.objects.create(
                contract=contract,
                signer=request.user,
                signer_full_name=signer_name,
                acceptance_statement=(
                    "I confirm that I have reviewed this contract, "
                    "understand its terms and agree to be bound by it."
                ),
                typed_signature=typed_signature,
                contract_version=contract.template_version,
                contract_snapshot=contract.content,
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT", "")
            )

            contract.status = "Signed"
            contract.signed_at = timezone.now()
            contract.save(update_fields=["status", "signed_at", "updated_at"])

        return redirect("contract_detail", contract_id=contract.pk)

    signature = getattr(contract, "digital_signature", None)

    return render(
        request,
        "contracts/contract_detail.html",
        {
            "contract": contract,
            "signature": signature
        }
    )
