from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User

"""Форма авторизации пользователей"""


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя пользователя',
        'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
        'class': 'form-control'}))


"""Форма по смене пароля пользователя"""


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль',
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'Старый пароль',
                                       'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Новый пароль',
                                        'class': 'form-control'}))
    new_password2 = forms.CharField(label='Новый пароль подтверждение',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Новый пароль подтверждение',
                                        'class': 'form-control'}))


"""Форма  по сбросу пароля по email"""


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Адрес электронной почты:',
                                 'class': 'form-control'}))


"""Форма по смене пароля пользователя после сброса"""


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Новый пароль',
                                        'class': 'form-control'}))
    new_password2 = forms.CharField(label='Новый пароль подтверждение',
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Новый пароль подтверждение',
                                        'class': 'form-control'}))


"""Форма по созданию нового пользователя с переопределением полей
   потому что отдельно widgest не работает в этом случае(баг в django)"""


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя пользователя',
        'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Пароль',
                                    'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Повторите пароль',
                                    'class': 'form-control'}))
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Адрес электронной почты:',
                                 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
