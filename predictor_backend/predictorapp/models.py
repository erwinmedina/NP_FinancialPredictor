from django.db import models
from mongoengine import Document, StringField
# Create your models here.

from django.db import models

# class FinancialRecord(models.Model):
#     category = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     description = models.TextField()

#     def __str__(self):
#         return f"{self.category} - {self.amount} - {self.date}"

class OrganizationLite(Document):
    name = StringField(max_length=100)
    ein = StringField(max_length=15)

    def __str__(self):
        return self.name