from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Менеджер для перекрытой модели пользователя"""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        # check password validation
        if password is not None:
            try:
                validate_password(password)
            except ValidationError as e:
                raise ValueError({"password": str(e.messages[0])})
        else:
            raise ValueError({"password": "Password can't be set!"})

        user = self.model(
            phone=phone,
            password=password,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        return self._create_user(phone, password, **extra_fields)

    @classmethod
    def normalize_phone(cls, phone):
        # TODO: сделать нормализацию phone
        "+{code} number"

        new_phone = phone or ""

        return new_phone


class User(AbstractBaseUser, PermissionsMixin):
    """Базовая модель пользователя полностью переопределенная"""

    phone = models.CharField(_("phone number"), max_length=12, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)

    contacts = models.ManyToManyField(
        "self",
        verbose_name="User contacts",
        symmetrical=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name[0].upper()}."
        return self.phone

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
