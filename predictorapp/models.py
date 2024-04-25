from django.db import models
from mongoengine import Document, StringField
# Create your models here.

from django.db import models

class OrganizationLite(Document):
    name = StringField(max_length=100)
    ein = StringField(max_length=15)

    def __str__(self):
        return self.name