from django.core.management.base import BaseCommand
import urllib.request, json
import datetime

#from src.oscartest.getcrndetails.management.commands.scraper.refresh_capacities import refresh_capacities
from getcrndetails.models import Semester, Section, Course

class Command(BaseCommand):
    help = 'get crns for current semesters'

    # print(datetime.date.today())
    current_semesters = Semester.objects.exclude(registration_end_date__lt=datetime.date.today(),
                                                      registration_start_date__gt=datetime.date.today())

    print(current_semesters)

    def handle(self, *args, **options):

        for Semester in self.current_semesters:
            print(Semester)

            # all courses
            semester_courses = Course.objects.filter(semester=Semester).order_by('course_str')
            semester_sections = Section.objects.filter(semester=Semester)

            for course in semester_courses:
                print(course)

                course_sections = Section.objects