from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.pk, filename)

class User(AbstractUser):

    SEX = [
        (1, 'Не указан'),
        (2, 'Женский'),
        (3, 'Мужской')
    ]

    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    sex = models.PositiveSmallIntegerField(_('Пол'), choices=SEX, blank=False, default=1)
    user_avatar = models.ImageField(_('Аватар'), upload_to=user_directory_path, blank=True)
    bio = models.TextField(_('Биография'), blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email