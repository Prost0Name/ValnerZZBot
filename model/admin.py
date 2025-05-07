from tortoise import fields, models

class AdminPassword(models.Model):
    id = fields.IntField(pk=True)
    password = fields.CharField(max_length=128)

    class Meta:
        table = "admin_password" 