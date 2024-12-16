from django.db import models

class MRTStation(models.Model):
  name = models.CharField(max_length=100)
  stop_id = models.CharField(max_length=10, unque = True)
  line = models.CharField(max_length=10)
  number = models.IntegerField()
  longtitude = models.FloatField()
  latitude = models.FloatField()
  subzone_number = models.IntegerField()
  subzone_name = models.CharField(max_length=100)
  subzone_code = models.CharField(max_length=20)
  pln_area_name = models.CharField(max_length=100)
  pln_area_code = models.CharField(max_length=10)
  region_name = models.CharField(max_length=100)
  region_code = models.CharField(max_length=10)

  def __str__(self):
    return self.name