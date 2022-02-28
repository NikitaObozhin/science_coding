from urllib import request
from django.contrib import admin
from .models import Courses, Lessons

class CoursesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

admin.site.register(Courses, CoursesAdmin)
admin.site.register(Lessons)

