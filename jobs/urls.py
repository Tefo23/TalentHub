# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Employer routes
    path("employer/post-job/", views.post_job, name="post_job"),
    path("employer/edit-job/<int:job_id>/", views.edit_job, name="edit_job"),
    path("employer/delete-job/<int:job_id>/", views.delete_job, name="delete_job"),
    path("employer/job/<int:job_id>/applicants/", views.view_job_applicants, name="view_job_applicants"),
	path(
        "employer/job/<int:job_id>/status/<str:new_status>/",
        views.toggle_job_status,
        name="toggle_job_status",
    ),
	path(
        'employer/applications/',
        views.employer_applications,
        name='employer_applications',
    ),
	path(
        'employer/application/<int:application_id>/review/',
        views.review_candidate,
        name='review_candidate',
    ),

    # Candidate routes
    path("job/<int:job_id>/apply/", views.apply_for_job, name="apply_for_job"),
    path("candidate/dashboard/", views.candidate_dashboard, name="candidate_dashboard"),
	path("candidate/apply/", views.apply_for_job, name="apply_for_job"),
]