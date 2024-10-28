from django.urls import path
from customauth.views import (
    RegisterView, CustomLoginView, RegisterDoneView, 
    CustomLogoutView, CustomChangeView, MyProfileDV,
    UpdateProfile, PasswordCV)
from django.contrib.auth import views as auth_views

app_name = 'customauth'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('register/done/', RegisterDoneView.as_view(), name="register_done"),
    path('password/change/', PasswordCV.as_view(), name='password_change'),
    path('logged_out/', CustomLogoutView.as_view(), name="logout"),
    path('update/', CustomChangeView.as_view(), name='account_update'),
    path('profile/<str:nickname>/', MyProfileDV.as_view(), name='my_profile'),
    path('profile/edit/<str:nickname>/', UpdateProfile.as_view(), name='update_profile'),

    # Password Reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_complete"),
]