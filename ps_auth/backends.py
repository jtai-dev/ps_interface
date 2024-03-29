from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class PSDualAuthBackend(ModelBackend):
    """This allows for dual authentitcation with email and username"""

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):

        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if (username is None and email is None) or password is None:
            return

        else:

            if email:
                try:
                    user = UserModel._default_manager.get_by_email(email)

                except UserModel.DoesNotExist:
                    UserModel().set_password(password)

            elif username:

                try:
                    user = UserModel._default_manager.get_by_natural_key(username)

                except UserModel.DoesNotExist:
                    UserModel().set_password(password)

            else:
                user = None

            if (
                user is not None
                and user.check_password(password)
                and self.user_can_authenticate(user)
            ):
                return user
