import pytz
from django.core.management.base import BaseCommand
import urllib.request, json
import datetime

#from src.oscartest.getcrndetails.management.commands.scraper.refresh_capacities import refresh_capacities
from getcrndetails.models import Semester, Section, Course

class Command(BaseCommand):
    help = 'get crns for current semesters'

    # print(datetime.date.today())
    unaware = datetime.datetime.today()
    timezone = pytz.timezone("America/New_York")  # .json timestamps from eastern time
    today = timezone.localize(unaware)

    # only get semesters where we are between start of phase 1 and end of phase 2 registration
    current_semesters = Semester.objects.filter(phase1_start_date__lt=today,
                                                phase2_end_date__gt=today)

    # can also exclude semesters when we are in between phases, as no one should be registering then
    # (sections may still be created, though)
    current_semesters.exclude(phase1_end_date__lt=today, phase2_start_date__gt=today)

    print(current_semesters)

    def handle(self, *args, **options):

        for current_semester in self.current_semesters:
            print(current_semester)

            crnmap = {}
            courselist = []

            # get latest json of classes and crns
            url = 'https://jasonpark.me/gt-schedule-crawler/'
            with urllib.request.urlopen(url + current_semester.semester_str + '.json') as url:
                data = json.loads(url.read().decode())
                #print(data)

                for course in data['courses']:
                    #print(course)
                    courselist.append(course)
                    # print(data['courses'][course])
                    for course_deets in data['courses'][course]:
                        # print("COURSE DEETS")
                        # print(course_deets)
                        if type(course_deets) is dict:
                            for entry in course_deets:
                                crn = course_deets[entry][0]
                                #print('crn:', crn)

                                crnmap[crn] = {
                                    'course': course,
                                    'code': entry
                                }

                querycourses = Course.objects.all()
                createcourses = []
                updatecourses = []

                for course in courselist:
                    newcourse = Course(
                                semester=current_semester,
                                course_str=course,
                                active=True
                            )
                    if querycourses.filter(course_str=course).exists():
                        #print(course, 'already in queryset, will update')
                        updatecourses.append(newcourse)
                    else:
                        #print(course, 'not in queryset, will create')
                        createcourses.append(newcourse)

                # create new courses
                msg = Course.objects.bulk_create(createcourses)
                print('create new courses', msg)

                # mark inactives
                inactivecourses = querycourses.exclude(pk__in=courselist)
                print('inactivecourses', inactivecourses)
                inactivecourses.update(active=False)

                querysections = Section.objects.all()
                createsections = []
                updatesections = []

                for crn in crnmap.keys():
                    newsection = Section(
                        semester=current_semester,
                        crn=crn,
                        active=True,
                        course=querycourses.get(course_str=crnmap[crn]['course']),
                        code=crnmap[crn]['code']
                    )
                    if querysections.filter(crn=crn).exists():
                        #print(crn, 'already in queryset, will update')
                        updatesections.append(newsection)
                    else:
                        #print(crn, 'not in queryset, will create')
                        createsections.append(newsection)

                # create new sections
                msg = Section.objects.bulk_create(createsections)
                print('create new sections', msg)

                # update sections
                msg = Section.objects.bulk_update(updatesections, ['code'])
                print('update sections field=code', msg)

                # mark inactives
                inactivesections = querysections.exclude(pk__in=crnmap.keys())
                print('inactivesections', inactivesections)
                inactivesections.update(active=False)

# need to make a new command for this...
def scrape_all_crn():
    pass

    # need to reconfigure refresh_capacities to read crns from Section objects...

    # get section capacities and create sectioncapacities objects...
    # maybe also create view in views.py to show latest section capacities by semester/crn ;)
    # then maybe add graphing... or a command to update capacities from the old .json data (need to input dates tho)
    # finally, do api to serve .json of capacities, or smaller .jsons for post requests of up to 100 crns

    #refresh_capacities('202102.json', '202102_jan4_capacities.json')