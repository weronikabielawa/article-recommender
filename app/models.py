from django.db import models


class ResultsModel(models.Model):
    propozycja_1 = models.IntegerField()
    propozycja_2 = models.IntegerField()
    propozycja_3 = models.IntegerField()
