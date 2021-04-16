from django.contrib.gis.db import models

# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=60)

    def __str__(self):
        return self.genre

class Job(models.Model):
    job = models.CharField(max_length=60, null=True)
    def __str__(self):
        return self.job

class Instrument(models.Model):
    instrument = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.instrument
