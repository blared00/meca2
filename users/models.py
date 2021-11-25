from datetime import datetime, timedelta
import jwt
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from meca import settings
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """Кастомный пользователь дез username."""

    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )
    middle_name = models.CharField(_("Отчество"), max_length=150, blank=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Фамилия имя и отчество пользователя.
        """
        return f"{self.last_name} {self.first_name} {self.middle_name})"

    def get_short_name(self):
        """
        Имя пользователя.
        """
        return self.first_name

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.timestamp()
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
