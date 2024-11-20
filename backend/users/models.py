from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=300)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_picture/default.png",
        blank=True,
        null=True,
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    def get_picture(self):
        try:
            return self.profile_picture.url
        except:
            no_picture = settings.MEDIA_URL + "profile_picture/default.png"
            return no_picture
