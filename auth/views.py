from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm, UserRegistrationForm


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'auth/login.html'


class LogoutUser(LogoutView):
    template_name = 'auth/logout.html'


class PasswordChangeUser(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "auth/password_change_form.html"


class PasswordChangeDoneUser(PasswordChangeDoneView):
    template_name = "auth/password_change_done.html"


class PasswordResetUser(PasswordResetView):
    email_template_name = "auth/password_reset_email.html"
    form_class = UserPasswordResetForm
    template_name = "auth/password_reset_form.html"


class PasswordResetDoneUser(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"

class PasswordResetConfirmUser(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")
    template_name = "auth/password_reset_confirm.html"

class PasswordResetCompleteUser(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html',{'form':form})


