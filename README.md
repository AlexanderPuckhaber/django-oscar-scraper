# django-oscar-scraper

Database for web-scraped class registration data from [oscar.gatech.edu](https://oscar.gatech.edu)

Currently has simple frontend with search by course name (eg. "AE 1601") and by CRN#

Web scraping still needs to be automated -- right now, it is run manually from [src/oscartest/getcrndetails/management/commands](https://github.com/AlexanderPuckhaber/django-oscar-scraper/tree/main/src/oscartest/getcrndetails/management/commands). 
But this is trivial -- just hit every CRN# once a day (takes about 3 hours). In the future, it might be worth trying to scrape a *subset* of the sections more frequently (only about 20% of sections are more than 3/4 full), which could potentially be done twice per hour.

Supports two POST requests for data, see [src/oscartest/getcrndetails/views.py](https://github.com/AlexanderPuckhaber/django-oscar-scraper/blob/main/src/oscartest/getcrndetails/views.py)

POST:
http://<base_url>/<semester_str>/get_capacities_by_crn
(eg. http://myawesomeserver.biz/202102/get_capacities_by_crn)

```
request.data = {
  'crns': [list, of, crn#s]
}

json(response) = {
  'crn': [seats_capacity, seats_actual, seats_remaining, seats_waitlist_capacity, seats_waitlist_actual, seats_waitlist_remaining, get_date]
}
```

Limit: 200 CRN#s  
seats and waitlist capacity, actual, and remaining are integers  
get_date is of the form ```str(datetime.datetime)```  
If no entry is found for a crn, the data for that crn is ```'crn': None```  

POST:  
http://<base_url>/<semester_str>/get_capacities_history_by_crn  
(eg. http://myawesomeserver.biz/202102/get_capacities_history_by_crn)  

```
request.data = {
  'crns': [list, of, crn#s],
  'from_timestamp': str(datetime.datetime),
  'to_timestamp': str(datetime.datetime)
}

json(response) = {
  'crn': [[seats_capacity, seats_actual, seats_remaining, seats_waitlist_capacity, seats_waitlist_actual, seats_waitlist_remaining, get_date], ]
}
```

Limit: 200 CRN#s  
seats and waitlist capacity, actual, and remaining are integers  
from_timestamp and to_timestamp should be of the form ```str(datetime.datetime)``` of a timezone-aware datetime  
the list is a 2D array of all entries for that section that were scraped between from_timestamp and to_timestamp  
get_date is of the form ```str(datetime.datetime)```  

