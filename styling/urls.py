from django.urls import path
from .views import submit_photos,get_styling_with_photos

urlpatterns=[
    path('photos/add/',submit_photos),
    path('photos/get/',get_styling_with_photos),
]