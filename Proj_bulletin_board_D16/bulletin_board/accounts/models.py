from django.contrib.auth.models import User
from django.db import models

#Коды подтверждения (code_Confirm)
class ConfirmCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now_add=True)
