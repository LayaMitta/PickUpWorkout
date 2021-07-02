from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.urls import reverse
from django.core.validators import MaxValueValidator

class MyUser(AbstractUser):
	is_trainer=models.BooleanField(default=False)
	is_member=models.BooleanField(default=False)
	is_dietician=models.BooleanField(default=False)
	age=models.IntegerField(validators=[MaxValueValidator(70)],default=0)
	gender = models.CharField(max_length=255,default='M')
	workout=models.CharField(max_length=255)
	phone=models.IntegerField(validators=[MaxValueValidator(10)],default=0)

class Member(models.Model):
	user=models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True)
	health_issues=models.CharField(max_length=255,default="None")

class Dietician(models.Model):
	user=models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True)
	experience=models.IntegerField(validators=[MaxValueValidator(50)],default=0)
	rating=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
	fees=models.IntegerField(validators=[MaxValueValidator(9999999999)],default=0)
	category=models.CharField(max_length=255)
	available=models.CharField(max_length=255,default="1pm-2pm")

class Trainer(models.Model):
	user=models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True)
	experience=models.IntegerField(validators=[MaxValueValidator(50)],default=0)
	rating=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
	fees=models.IntegerField(validators=[MaxValueValidator(9999999999)],default=0)
	available=models.CharField(max_length=255,default="1pm-2pm")

class Slot(models.Model):
	user=models.OneToOneField(MyUser,on_delete=models.CASCADE,primary_key=True)
	t5=models.CharField(max_length=255,default=0)
	t6=models.CharField(max_length=255,default=0)
	t7=models.CharField(max_length=255,default=0)
	t8=models.CharField(max_length=255,default=0)
	t9=models.CharField(max_length=255,default=0)
	t10=models.CharField(max_length=255,default=0)
	t11=models.CharField(max_length=255,default=0)
	t12=models.CharField(max_length=255,default=0)
	t13=models.CharField(max_length=255,default=0)
	t14=models.CharField(max_length=255,default=0)
	t15=models.CharField(max_length=255,default=0)
	t16=models.CharField(max_length=255,default=0)
	t17=models.CharField(max_length=255,default=0)
	t18=models.CharField(max_length=255,default=0)
	t19=models.CharField(max_length=255,default=0)
	t20=models.CharField(max_length=255,default=0)
	t21=models.CharField(max_length=255,default=0)



	
	

