from django.shortcuts import render
from .forms import EnquiryForm


def home(request):
    return render(request, 'core/home.html')


def packages(request):
    return render(request, 'core/packages.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    submitted = False

    package_mapping = {
        'Starter Website': 'Business website',
        'Business Website': 'Business website',
        'E-commerce Website': 'E-commerce',
        'Custom Business Solutions': 'Business system',
    }

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
            form = EnquiryForm()
    else:
        selected_package = request.GET.get('package', '')
        selected_service = package_mapping.get(selected_package, '')

        form = EnquiryForm(initial={
            'service': selected_service
        })

    return render(request, 'core/contact.html', {
        'form': form,
        'submitted': submitted,
    })