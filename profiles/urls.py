# profiles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing routes ...
    path(
        'candidate/profile/edit/',
        views.edit_candidate_profile,
        name='edit_candidate_profile',
    ),
]