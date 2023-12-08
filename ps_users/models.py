
from django.db import models
from ps_auth.models import PSUser


class PSUserProfile(models.Model):

    user = models.OneToOneField(PSUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    # Requires Pillow
    profile_pic = models.ImageField(blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def handle(self):
        return f"@{self.user.username}"

    @property
    def email(self):
        return self.user.email
