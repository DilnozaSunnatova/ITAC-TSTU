from django.db import models
from django.contrib.auth.base_user import  BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Speakers(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='speakers')
    position = models.CharField(max_length=200)
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name


class SectionDay(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Agenda(models.Model):
    day = models.IntegerField()
    description = models.TextField()
    section = models.ForeignKey(SectionDay,on_delete=models.CASCADE)

class Sponsor(models.Model):
    img = models.ImageField(upload_to='sponsor')

class Section(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo')

    def __str__(self) -> str:
        return self.name


class ConferenseSection(models.Model):
    description = models.TextField()
    section = models.ForeignKey(Section,on_delete=models.CASCADE)


class Home(models.Model):
    day = models.IntegerField()
    speakers_count = models.IntegerField()
    session_count = models.IntegerField()
    description = models.TextField()
    speakers = models.ForeignKey(Speakers,on_delete=models.CASCADE)

class Direction(models.Model):
    cordinator_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    map_street = models.TextField()
    latitude = models.FloatField(null=True) 
    longitude = models.FloatField(null=True)

    



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    affiliation = models.CharField(max_length=255)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Paper(models.Model):
    title = models.CharField(max_length=255)
    section = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255)
    file = models.FileField(upload_to='papers/', blank=True, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title



class PhoneManager(BaseUserManager):
    use_in_migrations = True

    def normalize_phone(self, phone):
     
        return phone.strip()

    def _create_user(self, phone, email, password=None, **extra_fields):
        
        if not phone:
            raise ValueError("Telefon raqami kiritilishi shart")
        email = self.normalize_email(email)
        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, email=email ,**extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser bo'lishi uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser bo'lishi uchun is_superuser=True bo'lishi kerak.")

        return self._create_user(phone, email, password, **extra_fields)

@deconstructible
class UnicodePhoneValidator(validators.RegexValidator):
    regex = r"^998[0-9]{9}"
    message = "Noto'g'ri raqam"



class User(AbstractUser):
    class UserAuthStatus(models.TextChoices):
        NEW = 'new', 'Yangi'
        APPROVED = 'approved', 'Tasdiqlangan'

    class GenderStatus(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
    phone_validator = UnicodePhoneValidator()
    phone = models.CharField(max_length=20,unique= True, validators=[phone_validator])
    username = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = PhoneManager()
    status = models.CharField(max_length=50,choices=UserAuthStatus.choices, default='new')

    code = models.CharField(max_length=4,null=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(
        max_length=200,
        choices=GenderStatus.choices
    )
    # birth_date = models.DateField(null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    confirm_password = models.CharField(max_length=10)
    affiliation = models.CharField(max_length=100)



    def __str__(self) -> str:
        return str(self.first_name)         



