from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.generic import  ListView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Semester, Course, Section, SectionCapacities
import datetime
import pytz
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

def index(request):
    template = loader.get_template('getcrndetails/index.html')
    semesters_all = Semester.objects.all().order_by('phase2_end_date')

    unaware = datetime.datetime.today()
    timezone = pytz.timezone("America/New_York")  # .json timestamps from eastern time
    today = timezone.localize(unaware)

    semesters_current = semesters_all.filter(phase1_start_date__lt=today, phase2_end_date__gt=today).order_by('phase2_end_date')

    context = {
        'semesters_all': semesters_all,
        'semesters_current': semesters_current
    }
    return HttpResponse(template.render(context, request))

# TODO: filter by semester is jank and might fail if semester_id not in url path kwargs
class CourseSearchResultsView(ListView):
    model = Course
    template_name = 'getcrndetails/course_search_results.html'

    def get_queryset(self):
        #print(self.kwargs['semester_id'])
        semester_id = str(self.kwargs['semester_id'])
        query = self.request.GET.get('q')
        object_list = Course.objects.filter(
            course_str__icontains=query, semester=semester_id
        ).order_by('course_str')
        return object_list

class CRNSearchResultsView(ListView):
    model = Section
    template_name = 'getcrndetails/crn_search_results.html'

    def get_queryset(self):
        semester_id = str(self.kwargs['semester_id'])
        query = self.request.GET.get('q')
        object_list = Section.objects.filter(
            crn=query, semester=semester_id
        ).order_by('crn')
        return object_list

def semester(request, semester_id):
    # get latest section capacity matching crn
    semester = Semester.objects.get(semester_str=semester_id)
    courses = Course.objects.filter(semester=semester_id)
    sections = Section.objects.filter(semester=semester_id)

    context = {
        'semester': semester,
    }
    template = loader.get_template('getcrndetails/semester.html')
    return HttpResponse(template.render(context, request))

def semester_subject(request, semester_id, course_subject):
    return HttpResponse(f"semester: {semester_id} subject: {course_subject}")

def semester_subject_number(request, semester_id, course_subject, course_number):
    semester = Semester.objects.get(semester_str=semester_id)

    course_str = course_subject + ' ' + course_number
    courses = Course.objects.filter(semester=semester_id, course_str=course_str)
    course = courses.first()
    sections = Section.objects.filter(semester=semester_id, course=course).order_by('code')

    context = {
        'semester': semester,
        'course': course,
        'sections': sections
    }
    template = loader.get_template('getcrndetails/course.html')
    return HttpResponse(template.render(context, request))

def semester_crn(request, semester_id, crn, course_subject='optional', course_number='optional'):
    # get latest section capacity matching crn
    semester = Semester.objects.get(semester_str=semester_id)
    section = Section.objects.filter(semester=semester_id).get(crn=crn)
    latest_section_capacities = SectionCapacities.objects.filter(section_crn=crn).order_by('-get_date')

    context = {
        'semester': semester,
        'section': section,
        'latest_section_capacities': latest_section_capacities,
    }
    template = loader.get_template('getcrndetails/section.html')
    return HttpResponse(template.render(context, request))

class get_capacities_by_crn(APIView):
    permission_classes = [AllowAny]

    queryset = SectionCapacities.objects.none()

    def post(self, request, *args, **kwargs):
        semester_id = str(kwargs['semester_id'])

        crn_list = request.data.getlist('crns')
        crn_limit = 200
        section_capacities = {}
        for crn in crn_list:
            #print(crn)
            try:
                section = Section.objects.filter(semester=semester_id, crn=crn).first()
                #print('section', section)
                try:
                    section_caps = SectionCapacities.objects.filter(section_crn=section.crn).order_by('get_date').first()
                    #section_caps = SectionCapacities.objects.filter(section_crn=section)
                    #print('section caps', section_caps)
                    section_caps_list = section_caps.capacities_as_list()
                    #print('section caps list', section_caps_list)
                except:
                    #print('no section_caps found')
                    section_caps_list = None
            except:
                section_caps_list = None

            section_capacities[crn] = section_caps_list
            crn_limit = crn_limit - 1
            if (crn_limit <= 0):
                break

        return JsonResponse(section_capacities)

class get_capacities_history_by_crn(APIView):
    permission_classes = [AllowAny]

    queryset = SectionCapacities.objects.none()

    def post(self, request, *args, **kwargs):
        semester_id = str(kwargs['semester_id'])

        crn_list = request.data.getlist('crns')
        from_timestamp = datetime.datetime.fromisoformat(request.data.get('from_timestamp'))
        to_timestamp = datetime.datetime.fromisoformat(request.data.get('to_timestamp'))
        print(from_timestamp, to_timestamp)
        crn_limit = 200
        section_capacities = {}
        for crn in crn_list:
            #print(crn)
            try:
                section = Section.objects.filter(semester=semester_id, crn=crn).first()
                print('section', section)
                try:
                    section_caps_set = SectionCapacities.objects.filter(get_date__range=[from_timestamp, to_timestamp],
                                                                        section_crn=section.crn).order_by('get_date')
                    #section_caps = SectionCapacities.objects.filter(section_crn=section)
                    print('section caps_set', section_caps_set)
                    section_caps_2Darray = []
                    for section_caps in section_caps_set:
                        print("aaadsfasdf")
                        print(section_caps.capacities_as_list())
                        section_caps_2Darray.append(section_caps.capacities_as_list())
                except:
                    #print('no section_caps found')
                    section_caps_2Darray = None
            except:
                section_caps_2Darray = None

            section_capacities[crn] = section_caps_2Darray
            crn_limit = crn_limit - 1
            if (crn_limit <= 0):
                break

        return JsonResponse(section_capacities)