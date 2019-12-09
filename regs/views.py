from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import strip_tags
from django.core import mail
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import *
from .forms import *

def is_authed(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You are not logged in, please log in.')
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper


def is_admin(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper

def is_not_authed(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, f'{request.user.username}, You are already logged in.')
            return redirect('home')
        return func(request, *args, **kwargs)
    return wrapper


def homepage(request):
    return render(request, 'regs/home.html')

def about(request):
    return render(request, 'regs/about.html')

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            con = form.save(commit = False)
            con.user = request.user
            con.save()
            messages.success(request, f'{request.user.username}, Your Contact form has been submitted.')
            return redirect('home')
    return render(request, 'regs/contact.html', {'form' : form})

@login_required
def reg(request):
    form = RegistrationForm()
    registration = Registration.objects.filter(user = request.user)
    if registration:
        form = RegistrationForm(instance = registration.first())
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance = registration.first())
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.save()
            messages.success(request, "We've Received your request, An email with the invitation will be sent once a moderator approves your request. Thank You")
            return redirect('home')
    context = {'reg' : bool(registration), 'form' : form}
    return render(request, 'regs/registration.html', context)

@is_admin
def reg_check(request, pk):
    registration = get_object_or_404(Registration, pk = pk)
    shorten_link = 'http://bit.ly/2PugMau'
    invite_link = 'https://join.slack.com/t/arabcodecommunity/shared_invite/enQtODY1OTg4ODYwNTgzLTg5YWM4ZDA1Y2JjNGM4Y2Q1ZmQ4YjU1NDBlOTFlYThlOGU0MjkzZDViOWFjMjRjNDNhZDY1MWEzYTFiY2FjNjQ'
    if request.method == 'POST' and 'approve' in request.POST:
        subject = 'Registration Approved'
        html_message = render_to_string('regs/reg-app.html', {'user': registration.user.username, 'invite_link' : invite_link, 'shorten_link' : shorten_link})
        plain_message = strip_tags(html_message)
        from_email = 'ACC <arabcodingcommunity@gmail.com>'
        to = registration.email
        user_email = registration.user.email
        if to == user_email:
            to = user_email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently = False)
        else:
            mail.send_mail(subject, plain_message, from_email, [to, user_email], html_message=html_message, fail_silently = False)
        registration.status = 'approved'
        registration.save()
        return redirect('dashboard')
    if request.method == 'POST' and 'rejected' in request.POST:
        subject = 'Registration Rejected'
        html_message = render_to_string('regs/reg-dec.html', {'user': registration.user.username})
        plain_message = strip_tags(html_message)
        from_email = 'ACC <arabcodingcommunity@gmail.com>'
        to = registration.email
        user_email = registration.user.email
        if to == user_email:
            to = user_email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently = False)
        else:
            mail.send_mail(subject, plain_message, from_email, [to, user_email], html_message=html_message, fail_silently = False)
        registration.status = 'rejected'
        registration.save()
        return redirect('dashboard')
    context = {}
    context['reg'] = registration
    return render(request, 'regs/reg-check.html', context)


@is_admin
def dashboard(request):
    registrations = Registration.objects.filter(status = 'pending')
    contacts = Contact.objects.filter(status = 'pending')
    context = {'regs' : registrations, 'cons' : contacts}
    return render(request, 'regs/dashboard.html', context)

@is_not_authed
def register_account(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    return render(request, 'regs/acc_reg.html', {'form' : form})

@is_admin
def check_con(request, pk):
    contact = get_object_or_404(Contact, pk = pk)
    context = {}
    context['contact'] = contact
    print(contact.status)
    return render(request, 'regs/con_check.html', context)
