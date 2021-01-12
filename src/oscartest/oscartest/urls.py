"""oscartest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from getcrndetails import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # index
    path('', views.index, name='index'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [

    path('swagger-ui/', TemplateView.as_view(
                template_name='getcrndetails/swagger-ui.html',
                extra_context={'schema_url':'/oscartest/static/openapi-schema.yml'}
            ), name='swagger-ui'),

    # crn search results
    path('<str:semester_id>/crn_search/', views.CRNSearchResultsView.as_view(), name='crn_search_results'),
    # course search results
    path('<str:semester_id>/course_search/', views.CourseSearchResultsView.as_view(), name='course_search_results'),
    # semester
    path('<str:semester_id>/', views.semester, name='semester'),
    # aaa
    path('<str:semester_id>/<str:course_subject>/<str:course_number>/<int:crn>/', views.semester_crn,
         name='semester-subject-number'),
    # semester / crn
    # ex. 202102/28145
    re_path(r'(?P<semester_id>[0-9]+)/(?P<crn>[0-9]+)/$', views.semester_crn, name='semester-crn'),
    # semester/subject
    # ex. 202102/AE
    path('<str:semester_id>/<str:course_subject>/', views.semester_subject, name='semester-subject'),
    # semester/subject/number
    # ex. 202102/AE/1601
    path('<str:semester_id>/<str:course_subject>/<str:course_number>/', views.semester_subject_number, name='semester-subject-number'),


    path('<str:semester_id>/get_capacities_by_crn', views.get_capacities_by_crn.as_view(), name='get-capacities-by-crn'),

    path('<str:semester_id>/get_capacities_history_by_crn', views.get_capacities_history_by_crn.as_view(), name='get-capacities-history-by-crn'),


    # https://www.django-rest-framework.org/#installation
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
