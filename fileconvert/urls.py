from django.urls import path
from . import views

app_name = 'fileconvert'
urlpatterns = [
    # 
    path('convert/', views.index, name='convert'),

]