from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
"""
Flexible and customizable way of handle user creation
"""
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager for the creation of regular users
    """

    def create_user(self, username, email, password=None,**extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(),email=email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    """
    Create and save a SuperUser with the given username, email and password ensuring
    access to Django admin interface
    """

    def create_superuser(self, username, email, password = None,**extra_fields):
        
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(username, password, email, **extra_fields)
    

class CustomUser(AbstractUser):
    """
    You can add fields that you want in your form not included in AbstractUser
    e.g gender = models.CharField(max_length=10)
    """
    USER_TYPE_CHOICES = (
        ('student','Student'),
        ('facilitator','Facilitator'),
        ('teamlead','Teamlead')
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required 150 caracters or fewer.Letters,digits and spaces only.',
        validators=[],
        error_messages={'unique':'A user with that username already exists',
        },
        )
    
    def is_facilitator(self):
        return self.user_type == 'facilitator'
    
    def is_student(self):
        return self.user_type =='student'
    
    def is_teamlead(self):
        return self.user_type == 'teamlead'
    
    objects = CustomUserManager()

    



