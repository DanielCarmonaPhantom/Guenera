from django.contrib import admin

# Register your models here.
from .models import WorkTable, Class, Announcements, InscriptionWorktable, InscriptionsClass, EnrolledStudents

admin.site.register(WorkTable)
admin.site.register(Class)
admin.site.register(Announcements)
admin.site.register(InscriptionWorktable)
admin.site.register(InscriptionsClass)
admin.site.register(EnrolledStudents)

