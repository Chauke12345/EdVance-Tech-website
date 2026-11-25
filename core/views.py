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

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
            form = EnquiryForm()
    else:
        form = EnquiryForm()

    return render(request, 'core/contact.html', {
        'form': form,
        'submitted': submitted,
    })
