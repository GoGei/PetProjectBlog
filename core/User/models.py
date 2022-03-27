from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from core.Utils.Mixins.models import CrmMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(CrmMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.label

    @property
    def label(self):
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return self.email or self.id


class Patient(CrmMixin):
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    address = models.CharField(max_length=1024)

    class Meta:
        db_table = 'patient'

    def __str__(self):
        return self.label

    @property
    def label(self):
        string = f'Patient: {self.user.label}'
        return string


class Doctor(CrmMixin):
    TAX_RATE = 13
    ROUND_RATE = 2

    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    speciality = models.ForeignKey('Speciality.Speciality', on_delete=models.PROTECT, db_index=True)
    price = models.PositiveIntegerField()
    salary_percent = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.label

    @property
    def label(self):
        string = f'Doctor ({self.speciality.label}): {self.user.label}'
        return string

    @property
    def indexed_tax(self):
        return round(1 / self.TAX_RATE * 100, self.ROUND_RATE)

    def salary_formula(self, appointments):
        salary = self.price * self.salary_percent * appointments * (1 - self.indexed_tax)
        return round(salary, self.ROUND_RATE)

    def month_appointments(self, month=None, year=None):
        appointments = self.appointment_set.active().filter(date__month=month, date__year=year).all()
        return appointments

    def current_salary(self, month=None):
        month = month or timezone.now().month
        year = timezone.now().year
        appointments = self.month_appointments(month, year).count()
        salary = self.salary_formula(appointments)
        return salary
