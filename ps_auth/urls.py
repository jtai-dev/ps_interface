from django.urls import path

from ps_auth import views

app_name = 'ps_auth'

urlpatterns = [
    path("login/", view=views.PSLoginView.as_view(), name='login'),
    path("logout/", view=views.PSLogoutView.as_view(), name='logout'),
    path("register/", view=views.PSRegisterView.as_view(), name='register'),
    path("forgotpass/", view=views.ForgotPasswordView.as_view(), name='forgotpassword')
]
