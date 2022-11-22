from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyAccountManager(BaseUserManager):
    def create_user(self, email,password=None, **extra_fields
                    ):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class User(AbstractBaseUser):
    first_name=models.CharField(max_length=16,null=True)
    last_name=models.CharField(max_length=16, null=True)
    GENDER_CHOICES=(
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    )
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.email)


    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser

User = settings.AUTH_USER_MODEL

class Identification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location=models.CharField(max_length=50, null=True)  
    id_number=models.IntegerField(unique=True)

class Detail(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    electricity_bill=models.DecimalField(max_digits=10, decimal_places=2, null=True) 
    water_bill=models.DecimalField(max_digits=10, decimal_places=2, null=True)
    loan_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True)