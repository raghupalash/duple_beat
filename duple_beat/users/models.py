#django imports

# from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.gis.db import models

#third party imports 
# from django_resized import ResizedImageField
from PIL import Image

#internal imports
from .labels import *
from .validators import *

# Create your models here.
class Manager(BaseUserManager):
    def create_user(self, email, username, password=None): 
        if not email or not username:
            raise ValueError("Users must have an email and username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username, 
            password=password,
            )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):


    # main
    name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=60, unique=True) #verbose_name="email"
    username = models.CharField(max_length=60, unique=True)
    image = models.ImageField(default="default-profile.png", upload_to="profile_pics", blank=True)
    
    # contact info
    phones = models.JSONField(default=list, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    about = models.CharField(max_length=280, blank=True, null=True)
    location = models.PointField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    # additional info
    genre = models.ManyToManyField(Genre, related_name='users')
    job = models.ManyToManyField(Job, blank=True, related_name="users")
    instrument = models.ManyToManyField(Instrument, blank=True, related_name="users")
    # budget = models.JSONField(default=list, validators=[validate_budget])
    budget_from = models.BigIntegerField(null=True)
    budget_to = models.BigIntegerField(null=True)

    # Social Media
    instagram = models.CharField(max_length=60, blank=True, null=True)
    twitter = models.CharField(max_length=60, blank=True, null=True)
    facebook = models.CharField(max_length=60, blank=True, null=True)
    tiktok = models.CharField(max_length=60, blank=True, null=True)
    youtube = models.CharField(max_length=60, blank=True, null=True)
    soundcloud = models.CharField(max_length=60, blank=True, null=True)
    spotify = models.CharField(max_length=60, blank=True, null=True)
    tidal = models.CharField(max_length=60, blank=True, null=True)
    deezer = models.CharField(max_length=60, blank=True, null=True)

    # REQUIRED
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    # class Meta:
    #     ordering = ['field_name']

    # def __str__(self):
        # return f"{self.field_name} {self.field_name}"

    def has_perm(self, perm,  obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if self.image:
        #     img = Image.open(self.image.path)

        #     if img.height != img.width:
        #         size = abs(img.height - img.width) // 2

        #         if img.height > img.width:
        #             area = (0, size, (img.height - (2 * size)), img.height - size)
                    
        #         else:
        #             area = (size, 0, img.width - size, (img.width - (2 * size)))
                
        #         crop = img.crop(area)
        #         crop.save(self.image.path)
            
        #     if self.image.size > 5485760: # 5MB
        #         self.image.delete()
        #         self.image = 'default-profile.png'
        #         self.save()

#Sets default job name for user when created or when user deletes job
def SetDefaultName(sender, instance, created, **kwargs):
    if created or not instance.job.all():
        job = Job.objects.get_or_create(job = "Artist")[0]
        instance.job.add(job)
post_save.connect(SetDefaultName, sender=User)
