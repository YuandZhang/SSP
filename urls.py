from . import  views
from django.urls import path,include,re_path
urlpatterns = [
    path('selectProjects/',views.selectProjects),
path('selectProjectsByConditions/',views.selectProjectsByConditions),



]
