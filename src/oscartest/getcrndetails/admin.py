from django.contrib import admin
from .models import Semester, Course, Section, SectionCapacities

# Register your models here.

admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionCapacities)