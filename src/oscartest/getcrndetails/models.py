from django.db import models

# Create your models here.
from django.db.models import UniqueConstraint

class Semester(models.Model):
    semester_str = models.CharField(primary_key=True, max_length=200)
    semester_str_readable = models.CharField(max_length=200)

    phase1_start_date = models.DateTimeField('start of Phase 1 registration', blank=True, null=True)
    phase1_end_date = models.DateTimeField('end of Phase 1 registration', blank=True, null=True)

    phase2_start_date = models.DateTimeField('start of Phase 2 registration', blank=True, null=True)
    phase2_end_date = models.DateTimeField('end of Phase 2 registration', blank=True, null=True)

    def __str__(self):
        return self.semester_str

class Course(models.Model):
    course_str = models.CharField(primary_key=True, max_length=50)

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.semester) + '/' + self.course_str

    def course_str_as_list(self):
        return self.course_str.split(' ')

class Section(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    crn = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    active=models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.course) + ':' + str(self.code)+ ':' + str(self.crn)

class SectionCapacities(models.Model):
    section_crn = models.ForeignKey(Section, on_delete=models.CASCADE)

    seats_capacity = models.IntegerField(default=0)
    seats_actual = models.IntegerField(default=0)
    seats_remaining = models.IntegerField(default=0)
    seats_waitlist_capacity = models.IntegerField(default=0)
    seats_waitlist_actual = models.IntegerField(default=0)
    seats_waitlist_remaining = models.IntegerField(default=0)

    def capacities_as_dict(self):
        return {
            'seats_capacity': self.seats_capacity,
            'seats_actual': self.seats_actual,
            'seats_remaining': self.seats_remaining,
            'seats_waitlist_capacity': self.seats_waitlist_capacity,
            'seats_waitlist_actual': self.seats_waitlist_actual,
            'seats_waitlist_remaining': self.seats_waitlist_remaining,
            'get_date': self.get_date
        }

    def capacities_as_list(self):
        caps_list = [0]*7   # [list, declaration] not working here ;/
        caps_list[0] = self.seats_capacity
        caps_list[1] = self.seats_actual
        caps_list[2] = self.seats_remaining
        caps_list[3] = self.seats_waitlist_capacity
        caps_list[4] = self.seats_waitlist_actual
        caps_list[5] = self.seats_waitlist_remaining
        caps_list[6] = self.get_date
        return caps_list

    get_date = models.DateTimeField()

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['section_crn', 'get_date'], name='unique_section_date')
        ]

    def __str__(self):
        return str(self.section_crn) + ' date: ' + str(self.get_date) + \
               ' seats: ' + str(self.seats_capacity) + ',' + str(self.seats_actual) + ',' \
    + str(self.seats_remaining) + ',' + ' waitlist: ' + str(self.seats_waitlist_capacity) + ',' \
    + str(self.seats_waitlist_actual) + ',' + str(self.seats_waitlist_remaining)
