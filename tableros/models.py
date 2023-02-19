from django.db import models
from users.models import User


class WorkTable(models.Model):
    worktable_name = models.CharField(max_length=200)
    imagen = models.ImageField('Imagen', upload_to='worktables/', max_length=255, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
