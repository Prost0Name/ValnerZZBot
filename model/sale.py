from tortoise import fields, models

class Sale(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    author_signature = fields.CharField(max_length=128, null=True)
    user_id = fields.CharField(max_length=32)
    amount = fields.IntField()

    class Meta:
        table = "sales" 