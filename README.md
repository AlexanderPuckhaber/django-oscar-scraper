# django-oscar-scraper

Database for web-scraped class registration data from [oscar.gatech.edu](https://oscar.gatech.edu)

Currently has simple frontend with search by course name (eg. "AE 1601") and by CRN#

Web scraping still needs to be automated -- right now, it is run manually from [src/oscartest/getcrndetails/management/commands](https://github.com/AlexanderPuckhaber/django-oscar-scraper/tree/main/src/oscartest/getcrndetails/management/commands)

Supports two POST requests for data, see [src/oscartest/getcrndetails/views.py](https://github.com/AlexanderPuckhaber/django-oscar-scraper/blob/main/src/oscartest/getcrndetails/views.py)


