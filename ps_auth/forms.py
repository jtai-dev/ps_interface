from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from ps_auth.models import PSUser, VerifiedEmail


UserModel = get_user_model()


# Admin forms
class PSUserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.BaseUserCreationForm.Meta):
        model = UserModel
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not VerifiedEmail.objects.filter(email__iexact=email).exists():

            self.add_error(
                "email",
                ValidationError(
                    "Email is not verified. Please contact your supervisor.",
                    code="unverified_email",
                ),
            )
        else:
            return email


class PSUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel


class PSAuthenticationForm(auth_forms.AuthenticationForm):

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"autofocus": True}),
        label="Username or Email",
    )

    def clean(self):

        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        _username = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        _email = UserModel._meta.get_field(UserModel.EMAIL_FIELD)

        if username_or_email is not None and password:
            try:
                user = PSUser.objects.get(email=username_or_email)
                self.username_field = _email

            except PSUser.DoesNotExist:
                user = None

            if user is None and not self.username_is_email:
                try:
                    user = PSUser.objects.get(username=username_or_email)
                    self.username_field = _username

                except PSUser.DoesNotExist:
                    user = None

            if user is not None:

                if (
                    self.username_field is _email
                    and self.username_field is not _username
                ):
                    self.user_cache = authenticate(
                        self.request, email=username_or_email, password=password
                    )

                elif (
                    self.username_field is _username
                    and self.username_field is not _email
                ):

                    self.user_cache = authenticate(
                        self.request, username=username_or_email, password=password
                    )

                else:
                    # This case is unlikely since either email and username had
                    # to be found. Closing this if statement just in case.
                    self.username_field = (
                        _email if self.username_is_email else _username
                    )
                    raise self.get_invalid_login_error()

                if self.user_cache is None:
                    raise self.get_invalid_login_error()
                else:
                    self.confirm_login_allowed(self.user_cache)

            else:
                self.username_field = _email if self.username_is_email else _username
                raise self.get_invalid_login_error()

        return self.cleaned_data

    @property
    def username_is_email(self):
        """Username field can also be email field"""
        try:
            validate_email(self.cleaned_data.get("username"))

        except ValidationError:
            return False

        return True


class ForgotPasswordForm(auth_forms.PasswordResetForm):

    def __init__(self, *args, **kwargs):
        self.client_ip = kwargs.pop("client_ip", None)
        self.from_email = kwargs.pop("from_email", None)
        super().__init__(*args, **kwargs)

    def get_users(self, email):
        """Called during super().save()"""
        # Limit password reset to non superusers.
        for user in super().get_users(email):
            if not user.is_superuser:
                yield user

            else:
                self.send_email_warning(
                    email,
                    subject_template_name="ps_auth/password_reset_sus_subject.html",
                    email_template_name="ps_auth/password_reset_sus_email.html",
                )

    def send_email_warning(self, email, subject_template_name, email_template_name):
        context = {
            "email_address": email,
            "ip_address": self.client_ip,
        }
        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email=self.from_email,
            to_email=email,
        )
