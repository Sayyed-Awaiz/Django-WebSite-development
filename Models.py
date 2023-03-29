from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from functools import partial
from .storage import OverwriteStorage


# Create your models here.
class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
      full_name=models.CharField(max_length=20,default=None,null=True)
      father_or_husband_name = models.CharField(max_length=20, default=None,null=True)
      dob = models.DateField(default=None,null=True)
      mobile_no = models.IntegerField(default=None, null=True)
      city = models.CharField(max_length=12, default=None,null=True)
      state = models.CharField(max_length=20, default=None,null=True)
      country = models.CharField(max_length=20, default=None,null=True)
      password2 = models.CharField(max_length=20, default=None,null=True)


      def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()    

# def upload1(instance , filename):
#     img_extension = os.path.splitext(filename)[1]
#     img_save_path = "{}/{}" .format(instance.user.username, filename)
#     return img_save_path

def img_name(instance , filename, imgname):
  imgname = imgname
  return os.path.join("{}/{}".format(instance.user.username, imgname))
  
def upload1(imgname):  
  return partial(img_name, imgname=imgname)








class DMIT(models.Model):  
  user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
  l1l=models.ImageField(default=None, upload_to=upload1('l1l.png'), storage=OverwriteStorage())
  l1c=models.ImageField(default=None, upload_to=upload1('l1c.png'), storage=OverwriteStorage())
  l1r=models.ImageField(default=None, upload_to=upload1('l1r.png'), storage=OverwriteStorage())

  
  l2l=models.ImageField(default=None, upload_to=upload1('l2l.png'), storage=OverwriteStorage())
  l2c=models.ImageField(default=None, upload_to=upload1('l2c.png'), storage=OverwriteStorage())
  l2r=models.ImageField(default=None, upload_to=upload1('l2r.png'), storage=OverwriteStorage())

  

  l3l=models.ImageField(default=None, upload_to=upload1('l3l.png'), storage=OverwriteStorage())
  l3c=models.ImageField(default=None, upload_to=upload1('l3c.png'), storage=OverwriteStorage())
  l3r=models.ImageField(default=None, upload_to=upload1('l3r.png'), storage=OverwriteStorage())



  l4l=models.ImageField(default=None, upload_to=upload1('l4l.png'), storage=OverwriteStorage())
  l4c=models.ImageField(default=None, upload_to=upload1('l4c.png'), storage=OverwriteStorage())
  l4r=models.ImageField(default=None, upload_to=upload1('l4r.png'), storage=OverwriteStorage())

  

  l5l=models.ImageField(default=None, upload_to=upload1('l5l.png'), storage=OverwriteStorage())
  l5c=models.ImageField(default=None, upload_to=upload1('l5c.png'), storage=OverwriteStorage())
  l5r=models.ImageField(default=None, upload_to=upload1('l5r.png'), storage=OverwriteStorage())

  

  r1l=models.ImageField(default=None, upload_to=upload1('r1l.png'), storage=OverwriteStorage())
  r1c=models.ImageField(default=None, upload_to=upload1('r1c.png'), storage=OverwriteStorage())
  r1r=models.ImageField(default=None, upload_to=upload1('r1r.png'), storage=OverwriteStorage())
  


  r2l=models.ImageField(default=None, upload_to=upload1('r2l.png'), storage=OverwriteStorage())
  r2c=models.ImageField(default=None, upload_to=upload1('r2c.png'), storage=OverwriteStorage())
  r2r=models.ImageField(default=None, upload_to=upload1('r2r.png'), storage=OverwriteStorage())

  
  r3l=models.ImageField(default=None, upload_to=upload1('r3l.png'), storage=OverwriteStorage())
  r3c=models.ImageField(default=None, upload_to=upload1('r3c.png'), storage=OverwriteStorage())
  r3r=models.ImageField(default=None, upload_to=upload1('r3r.png'), storage=OverwriteStorage())


  r4l=models.ImageField(default=None, upload_to=upload1('r4l.png'), storage=OverwriteStorage())
  r4c=models.ImageField(default=None, upload_to=upload1('r4c.png'), storage=OverwriteStorage())
  r4r=models.ImageField(default=None, upload_to=upload1('r4r.png'), storage=OverwriteStorage())



  r5l=models.ImageField(default=None, upload_to=upload1('r5l.png'), storage=OverwriteStorage())
  r5c=models.ImageField(default=None, upload_to=upload1('r5c.png'), storage=OverwriteStorage())
  r5r=models.ImageField(default=None, upload_to=upload1('r5r.png'), storage=OverwriteStorage())

  confirm = models.CharField(max_length=8, default=None)

  
  # print(Profile.username)
  def __str__(self):
        return self.user.username
# @receiver(post_save, sender=DMIT)
# def update_user_dmit(sender, instance, created, **kwargs):
#     if created:
#         dmit.objects.create(dmit=instance)
#     instance.dmit.save()


class DMITVAL(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
      
    l1=models.CharField(max_length=2, default=None)
    lrc1=models.IntegerField(default=None)


    l2=models.CharField(max_length=2, default=None)
    lrc2=models.IntegerField(default=None)

    l3=models.CharField(max_length=2, default=None)
    lrc3=models.IntegerField(default=None)

    l4=models.CharField(max_length=2, default=None)
    lrc4=models.IntegerField(default=None)


    l5=models.CharField(max_length=2, default=None)
    lrc5=models.IntegerField(default=None)

    r1=models.CharField(max_length=2, default=None)
    rrc1=models.IntegerField(default=None)

    r2=models.CharField(max_length=2, default=None)
    rrc2=models.IntegerField(default=None)

    r3=models.CharField(max_length=2, default=None)
    rrc3=models.IntegerField(default=None)

    r4=models.CharField(max_length=2, default=None)
    rrc4=models.IntegerField(default=None)

    r5=models.CharField(max_length=2, default=None)
    rrc5=models.IntegerField(default=None)
    latd=models.IntegerField(default=None)
    ratd=models.IntegerField(default=None)
    def __str__(self):
        return self.user.username
  
class ListofUsers(models.Model):
     username = models.CharField(max_length=100)

class Appointment(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
  appointment_date =models.DateField(default=None,null=True)
  appointment_slot=models.CharField(max_length=20,default=None,null=True)
  def __str__(self):
        return self.user.username



