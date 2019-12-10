from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from .models import User
from django.contrib.auth.models import Group
from tasks import celey_send_mail
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from planeks_auth.tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.groups.set([Group.objects.get(name='Пользователи')])
            current_site = get_current_site(request)
            celey_send_mail(user, current_site, form)
            return HttpResponse('На вашу почту отправлено письмо со ссылкой на подтверждение электронной почты.')
    else:
        form = SignupForm()
    return render(request, 'planeks_auth/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Спасибо, что подтвердили электронный адрес. Теперь вы можете зарегистрироваться.')
    else:
        return HttpResponse('Не подходящая ссылка активации.')
