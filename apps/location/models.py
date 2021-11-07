from django.db import models


class Location(models.Model):
    
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return f"{self.lat}, {self.lon}"
