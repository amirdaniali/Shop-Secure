from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50,blank=False)
    phone = models.CharField(max_length=20, blank=False)

    user_permissions = models.CharField(max_length=20, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        email_username = self.full_name.split(' ')[0] + self.email.split("@")[0]
        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username # temporary fix have to revise
        if self.username == '' or self.username == None:
            self.username = email_username # temporary fix have to revise
        
        super(User,self).save(*args, **kwargs)

class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image', default="default/default-user.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=50,blank=False)
    about = models.CharField(max_length=999,blank=True, null=True)
    gender = models.CharField(max_length=20,blank=True, null=True)
    country = models.CharField(max_length=20,blank=True, null=True)
    state = models.CharField(max_length=20,blank=True, null=True)
    city = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=20,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    pid = ShortUUIDField(unique = True, length=10, max_length = 20, alphabet='abcdefghijk')


    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)


    def save(self, *args, **kwargs):
        if self.full_name == '' or self.full_name == None:
            self.full_name = self.user.full_name 

        
        super(Profile,self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, ** kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, ** kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
