
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views


from ps_auth.forms import (PSAuthenticationForm,
                           PSUserCreationForm,
                           VerifiedEmail,
                           ForgotPasswordForm)


class PSRegisterView(CreateView):
    form_class = PSUserCreationForm
    template_name = "ps_auth/register.html"
    success_url = reverse_lazy("ps_auth:register")

    def form_valid(self, form) -> HttpResponse:
        redirect_response = super().form_valid(form)

        if self.success_url == self.request.path:
            verified_user = VerifiedEmail.objects.get(
                email__iexact=self.object.email)

            return self.render_to_response({'your_name': verified_user.first_name})

        else:
            return redirect_response


class PSLoginView(auth_views.LoginView):
    form_class = PSAuthenticationForm
    template_name = "ps_auth/login.html"
    # redirect_authenticated_user = True


class PSLogoutView(auth_views.LogoutView):
    pass


class ForgotPasswordView(auth_views.PasswordResetView):

    form_class = ForgotPasswordForm
    template_name = 'ps_auth/forgot_pass.html'
    success_url = reverse_lazy("ps_auth:forgotpassword")

    def form_valid(self, form) -> HttpResponse:
        # redirect_response = super().form_valid(form)
        redirect_response = HttpResponseRedirect(self.get_success_url())

        if self.success_url == self.request.path:
            return self.render_to_response({})

        else:
            return redirect_response

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['client_ip'] = self.get_client_ip
        kwargs['from_email'] = self.from_email

        return kwargs

    @property
    def get_client_ip(self):

        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = self.request.META.get('REMOTE_ADDR')

        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        else:
            return remote_addr
