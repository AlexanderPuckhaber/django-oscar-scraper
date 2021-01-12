from django.core.management.base import BaseCommand
import urllib.request, json
import datetime
from django.utils import timezone
import pytz
import json


#from src.oscartest.getcrndetails.management.commands.scraper.refresh_capacities import refresh_capacities
from getcrndetails.management.commands.scraper.get_capacities import generate_capacities_dict
from getcrndetails.models import Semester, Section, Course, SectionCapacities

class Command(BaseCommand):
    help = 'import section capacities from json\nUsage: type .json filename'

    def add_arguments(self, parser):
        parser.add_argument('semester', nargs=1, type=str)
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        semester_str = options['semester'][0]
        semester = Semester.objects.get(semester_str=semester_str)
        print(semester)

        sections = Section.objects.filter(semester=semester.semester_str)

        json_filename = options['filename'][0]
        print(json_filename)

        timezone = pytz.timezone("America/New_York")  # .json timestamps from eastern time

        # earliest and latest timestamps, used to select sectioncapacities later
        earliest_timestamp = datetime.datetime.now(tz=timezone)
        latest_timestamp = datetime.datetime.now(tz=timezone)

        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)

            createsectioncapacities=[]

            for crn in data.keys():
                capacities_dict = generate_capacities_dict(data[crn])
                #print(crn, data[crn], capacities_dict)

                # how timestamp was created at moment of get request:
                # d = datetime.utcnow()
                # unixtime = calendar.timegm(d.utctimetuple())
                # capacities['timestamp'] = unixtime

                # this appears to be the correct conversion
                unaware = datetime.datetime.fromtimestamp(capacities_dict['timestamp'])
                dtime = timezone.localize(unaware)
                #print(dtime)

                # update earliest and latest timestamps found
                if (dtime < earliest_timestamp):
                    earliest_timestamp = dtime
                if (dtime > latest_timestamp):
                    latest_timestamp = dtime

                try:
                    section = sections.get(crn=crn)

                    new_section_capacities = SectionCapacities(
                        section_crn = section,

                        seats_capacity = capacities_dict['seats_capacity'],
                        seats_actual = capacities_dict['seats_actual'],
                        seats_remaining = capacities_dict['seats_remaining'],
                        seats_waitlist_capacity = capacities_dict['waitlist_capacity'],
                        seats_waitlist_actual = capacities_dict['waitlist_actual'],
                        seats_waitlist_remaining = capacities_dict['waitlist_remaining'],

                        get_date = dtime
                    )

                    createsectioncapacities.append(new_section_capacities)

                    #print('new_section_capacities:', new_section_capacities)
                except:
                    print('section does not exist for crn:', crn)

            # find which sectioncapacities already exist
            existing_sectioncapacities = SectionCapacities.objects.filter(get_date__range=[earliest_timestamp, latest_timestamp])

            final_create = []
            for new_section_caps in createsectioncapacities:
                if existing_sectioncapacities.filter(section_crn=new_section_caps.section_crn, get_date=new_section_caps.get_date).exists():
                    pass
                else:
                    final_create.append(new_section_caps)

            print('adding', final_create)

            # create new sectioncapacities
            msg = SectionCapacities.objects.bulk_create(final_create)
            #print('create new sections', msg)