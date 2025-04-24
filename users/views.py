
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_decode
from orders.models import Order


from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = _('Активация аккаунта')
            from_email = f'{settings.DEFAULT_FROM_EMAIL}'
            to_email = [user.email]

            text_content = _('Пожалуйста, активируйте ваш аккаунт, перейдя по ссылке.')
            html_content = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'site_name': current_site.name,
                'protocol': 'https' if request.is_secure() else 'http',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, _('Пожалуйста, подтвердите ваш email для завершения регистрации.'))
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Ваш email успешно подтвержден. Теперь вы можете войти в систему.'))
        return redirect('login')
    else:
        messages.error(request, _('Ссылка активации недействительна!'))
        return redirect('login')
    
    
def user_login(request):
    if request.user.is_authenticated:
        return redirect('pizza_list')
        
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, _('Вы успешно вошли в систему.'))
                return redirect('product_list')
            else:
                messages.error(request, _('Ваш аккаунт не активирован. Пожалуйста, проверьте вашу почту для активации.'))
        else:
            messages.error(request, _('Неверный email или пароль.'))
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, _('Вы вышли из системы.'))
    return redirect('pizza_list')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён.')
            return redirect('edit_profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def profile(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, _('Вы вышли из системы.'))
    return redirect('product_list')