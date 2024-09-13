from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    class Meta:
        table = "users"
        default_connection = "default"

    def __str__(self):
        return self.username
