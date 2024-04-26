from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),# url-адреса регистрации пользователей
    path('login/', views.LoginUser.as_view(), name='login'),# url-адреса входа
    # path('login/', views.LoginUser.as_view(), name='login'),# url-адреса входа
    path('logout/', views.LogoutUser.as_view(), name='logout'),# url-адреса выхода
    path('password-change/', views.PasswordChangeUser.as_view(),
                            name='password_change'),# url-адреса смены пароля
    path('password-change/done/', views.PasswordChangeDoneUser.as_view(),
                            name='password_change_done'),# url-адреса смены пароля
    path('password-reset/', views.PasswordResetUser.as_view(),
                            name='password_reset'),# url-адреса сброса пароля
    path('password-reset/done/', views.PasswordResetDoneUser.as_view(),
                            name='password_reset_done'),# url-адреса сброса пароля
    path('password-reset/<uidb64>/<token>/', views.PasswordResetConfirmUser.as_view(),
                            name='password_reset_confirm'),# url-адреса сброса пароля
    path('password-reset/complete/', views.PasswordResetCompleteUser.as_view(),
                            name='password_reset_complete'),# url-адреса сброса пароля
]