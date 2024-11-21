from djongo import models
from bson.objectid import ObjectId
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)