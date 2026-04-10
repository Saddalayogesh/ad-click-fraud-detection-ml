from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class predict_ad_click_fraud_detection(models.Model):

    Fid= models.CharField(max_length=3000)
    IPAddress= models.CharField(max_length=3000)
    App_Name= models.CharField(max_length=3000)
    Device= models.CharField(max_length=3000)
    OS= models.CharField(max_length=3000)
    Channel= models.CharField(max_length=3000)
    Click_time= models.CharField(max_length=3000)
    Time_to_click= models.CharField(max_length=3000)
    Session_duration= models.CharField(max_length=3000)
    Mouse_movement= models.CharField(max_length=3000)
    IP_frequency= models.CharField(max_length=3000)
    Referrer_missing= models.CharField(max_length=3000)
    Scroll_depth= models.CharField(max_length=3000)
    Time_on_page= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class csvdatasets(models.Model):

    Fid= models.CharField(max_length=3000)
    IPAddress= models.CharField(max_length=3000)
    App_Name= models.CharField(max_length=3000)
    Device= models.CharField(max_length=3000)
    OS= models.CharField(max_length=3000)
    Channel= models.CharField(max_length=3000)
    Click_time= models.CharField(max_length=3000)
    Time_to_click= models.CharField(max_length=3000)
    Session_duration= models.CharField(max_length=3000)
    Mouse_movement= models.CharField(max_length=3000)
    IP_frequency= models.CharField(max_length=3000)
    Referrer_missing= models.CharField(max_length=3000)
    Scroll_depth= models.CharField(max_length=3000)
    Time_on_page= models.CharField(max_length=3000)



class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



