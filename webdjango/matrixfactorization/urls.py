from django.urls import path

from . import views
app_name = 'matrixfactorrization'
urlpatterns = [
    path('recommend/',views.recommend,name='recommend')
]