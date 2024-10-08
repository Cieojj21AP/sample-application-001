from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
import uuid
from django.utils import timezone

class CustomUserManager(UserManager):
    use_in_migrations = True
 
    def _create_user(self, email, username, password, **extra_fields):
        # create_user と create_superuser の共通処理
        if not email:
            raise ValueError('email must be set')
        if not username:
            raise ValueError('username must be set')
 
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
 
        return user
 
    def create_user(self, username, email=None, password=None, **extra_fields):
 
        if not email:
            raise ValueError('email must be set')
        if not username:
            raise ValueError('username must be set')
 
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
 
        return self._create_user(email, username, password, **extra_fields)
 
    def create_superuser(self, username, email=None, password=None, **extra_fields):
 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
 
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
 
        return self._create_user(email, username, password, **extra_fields)
    
class CustomUser(AbstractUser):
    objects = CustomUserManager()

    # カスタムユーザーのフィールド
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zipcode = models.IntegerField('郵便番号', null=False, default='1000000')
    address1 = models.CharField('住所1', null=False, default='YourCity', max_length=50)
    address2 = models.CharField('住所2', null=True, max_length=50)
    joinedDate = models.DateTimeField('入会日',default=timezone.now)
 
    def __str__(self):
        return self.email
    
class SubscriptionCustomer(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username