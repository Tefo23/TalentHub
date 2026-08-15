from django.urls import path
from . import views

urlpatterns = [
    # ==========================
    # Public Pages
    # ==========================
    path("", views.home, name="home"),
    path("jobs/", views.public_job_list, name="public_job_list"),
    path("contacts/", views.contact_us, name="contact_us"),
    path("about/", views.about_view, name="about"),

    # ==========================
    # Authentication
    # ==========================
    path(
    "login/",
    views.login_view,
    name="login"
),
    path("logout/", views.logout_view, name="logout"),

 # ==========================
# Registration
# ==========================

path("register/", views.register_choice, name="register_choice"),

path(
    "register/<str:role>/",
    views.register,
    name="register",
),

    # ==========================
    # Dashboards
    # ==========================
    path(
        "candidate/dashboard/",
        views.candidate_dashboard,
        name="candidate_dashboard",
    ),
    path(
        "employer/dashboard/",
        views.employer_dashboard,
        name="employer_dashboard",
    ),
path(
    "employer/company-profile/",
    views.employer_company_profile,
    name="employer_company_profile",
),
path(
    "candidate/job-list/",
    views.job_list,
    name="job_list",
),
path(
    "candidate/applications/",
    views.MyApplications,
    name="MyApplications",
),
 path(
        'candidate/profile/edit/',
        views.edit_candidate_profile,
        name='edit_candidate_profile',
    ),
path(
        "candidate/application/<int:application_id>/delete/",
        views.delete_application,
        name="delete_application",
    ),
path(
        'candidate/application/<int:application_id>/', 
        views.view_application, 
        name='view_application'
    ),
]