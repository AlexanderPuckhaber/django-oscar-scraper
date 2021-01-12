import json
import urllib3
from get_capacities import get_capacities, generate_capacities_dict, generate_capacities_list
import time

urllib3_http = urllib3.PoolManager()

def request_wrapper(crn, urllib3_http):
    response = get_capacities(crn, urllib3_http)

    if response is None:
        print('response for crn', crn, 'returned None')
        raise Exception('failed')
    return response

def refresh_capacities(courses_json, capacities_json):
    with open(courses_json) as f:
        data = json.load(f)

    try:
        f = open(capacities_json)
        try:
            capacities_map = json.load(f)
        except:
            capacities_map = {}
    except IOError:
        capacities_map = {}

    allDone = False

    num_tries = 10

    try:
        while not allDone and num_tries > 0:
            allDone = True
            num_tries = num_tries - 1

            for course in data['courses']:
                print(course)
                #print(data['courses'][course])
                for course_deets in data['courses'][course]:
                    #print("COURSE DEETS")
                    #print(course_deets)
                    if type(course_deets) is dict:
                        for entry in course_deets:
                            crn = course_deets[entry][0]

                            if crn not in capacities_map.keys():
                                allDone = False
                                time.sleep(0.5)

                                try:
                                    resp = request_wrapper(crn, urllib3_http)
                                except:
                                    resp = None
                                    print("resp = None crn:", crn)
                                    time.sleep(60)

                                if resp is not None:
                                    capacities = generate_capacities_list(resp)
                                    capacities_map[crn] = capacities
                                    print(course, entry, "crn:", crn, capacities)

                            else:
                                print(course, entry, 'crn:', crn, 'skipped', capacities_map[crn])
    except KeyboardInterrupt:
        print(" Ctrl-C")
    print("writing to file")
    # write to file
    with open(capacities_json, 'w+') as f:
        json.dump(capacities_map, f)