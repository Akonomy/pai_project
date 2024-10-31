from django.db import models

# Create your models here.


class Sensor(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[("input", "Input"), ("output", "Output")])
    mode = models.CharField(max_length=10, choices=[("digital", "Digital"), ("analog", "Analog")], default="digital")
    status = models.CharField(max_length=10, choices=[("on", "On"), ("off", "Off")], default="off")
    value = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
