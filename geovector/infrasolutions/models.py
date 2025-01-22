from django.contrib.gis.db import models

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.MultiPolygonField()
    
    def __str__(self):
        return self.name