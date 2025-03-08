from tortoise import fields, models


#当对模型进行更改时，可以运行以下命令来更新数据库：
#docker-compose exec backend aerich migrate
#docker-compose exec backend aerich upgrade
class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"