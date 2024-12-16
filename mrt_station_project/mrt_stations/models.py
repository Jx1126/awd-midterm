from django.db import models

class MRTStation(models.Model):
  name = models.CharField(max_length=100)
  stop_id = models.CharField(max_length=10, unque = True)
  line = models.CharField(max_length=10)
  no = models.IntegerField()
  lng = models.FloatField()
  lat = models.FloatField()
  subzone_no = models.IntegerField()
  subzone_n = models.CharField(max_length=100)
  subzone_c = models.CharField(max_length=20)
  pln_area_n = models.CharField(max_length=100)
  pln_area_c = models.CharField(max_length=10)
  region_n = models.CharField(max_length=100)
  region_c = models.CharField(max_length=10)

  def __str__(self):
    return self.name