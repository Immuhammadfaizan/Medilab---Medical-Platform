from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(email, password, **extra_fields)


# User Model
class User(AbstractUser):
    username = None 
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, unique=True, null=False, default="example@example.com")
    bio = models.TextField(default='Hello there! I am using SkillHub', null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  
    
    objects = UserManager()  

    def __str__(self):
        return self.email 


# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description available")
    department_image = models.ImageField(null=True, default='')

    def __str__(self):
        return self.name


# Doctor Model
class Doctor(models.Model):
    name = models.CharField(max_length=100)  
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='doctors'
    )
    bio = models.TextField(default="No description available")
    doctor_image = models.ImageField(null=True, default='')

    def __str__(self):
        return self.name
    
    
# Appointment Model
class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, null=False, default="example@example.com")
    phone = models.CharField(max_length=20)
    date = models.DateField()
    
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE) 
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE
        )  
    
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with {self.doctor.name} - {self.name} ({self.date})"


# Contact Message Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, null=False, default="example@example.com")
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
