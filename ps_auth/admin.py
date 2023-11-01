

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from ps_auth.models import (PSUser, 
                            VerifiedEmail)

from ps_auth.forms import (PSUserChangeForm, 
                           PSUserCreationForm, 
                           PSAuthenticationForm)


class PSUserAdmin(BaseUserAdmin):

    form = PSUserChangeForm
    add_form = PSUserCreationForm

    list_display = ("username", "email", "is_admin",)
    list_filter = ("is_admin", "is_superuser", "is_active", "groups",)

    search_fields = ("username", "email",)
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)

    readonly_fields = ('last_login', 'date_created',)

    fieldsets = (
        (None, {"fields": ("username", "email", "password",)}),
        ("Account Updates", {"fields": ("last_login", "date_created",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_admin",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        })
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


# Register your models here.
admin.site.register(PSUser, PSUserAdmin)
admin.site.register(VerifiedEmail)
admin.site.login_form = PSAuthenticationForm