from django.db import models

class PortHoldings(models.Model):
    nameFund = models.CharField(max_length=30)
    numHoldings = models.DecimalField(max_digits=30, decimal_places=20)
    institution = models.CharField(max_length=30)

