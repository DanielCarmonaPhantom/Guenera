import string
import random

from django.db import models
from users.models import User




from django.utils.text import slugify

class WorkTable(models.Model):
    worktable_name = models.CharField(max_length=70, blank=False)
    worktable_imagen = models.ImageField('Imagen', upload_to='worktables/', max_length=255, null=True, blank=True)
    worktable_slug = models.SlugField(null=False, blank=False, unique=False)

    worktable_invite_url = models.CharField(max_length=8, null=True, blank=False)
    worktable_invite_url_expiration = models.DateField(auto_now_add=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.worktable_slug = slugify(self.worktable_name)
        super(WorkTable, self).save(*args, **kwargs)


class Class(models.Model):
    class_name = models.CharField(max_length=70, blank=False)
    class_description = models.CharField(max_length=250)
    class_slug = models.SlugField(null=False, blank=False, unique=False)

    class_imagen = models.ImageField('Imagen', upload_to='worktables/', max_length=255, null=True, blank=True)

    WorkTable_id = models.ForeignKey(WorkTable, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.class_slug = slugify(self.class_name)
        super(Class, self).save(*args, **kwargs)


class Announcements(models.Model):
    announcement_text = models.CharField(max_length=250)
    announcement_slug = models.SlugField(null=False, blank=False, unique=False)
    announcement_class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    announcement_worktable_id = models.ForeignKey(WorkTable, on_delete=models.CASCADE)
    announcement_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement_username = models.CharField(max_length=70)

    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.announcement_slug = slugify(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16)))
        super(Announcements, self).save(*args, **kwargs)


class InscriptionWorktable(models.Model):
    inscription_worktable_id = models.ForeignKey(WorkTable, on_delete=models.CASCADE)
    inscription_user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class InscriptionsClass(models.Model):
    student_name = models.CharField(max_length=40, blank=True)
    student_username = models.CharField(max_length=40, blank=False)
    student_email = models.CharField(max_length=40, blank=False)

    application_status = models.CharField(max_length=10, blank=True, default='sent')

    student_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    

class EnrolledStudents(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)