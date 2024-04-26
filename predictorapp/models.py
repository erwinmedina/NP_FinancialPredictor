from mongoengine import Document, StringField
# Create your models here.

class OrganizationLite(Document):
    name = StringField(max_length=100)
    ein = StringField(max_length=15)

    def __str__(self):
        return self.name