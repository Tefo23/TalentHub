from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # <--- ADD THIS IMPORT
from .forms import RegisterForm, LoginForm, ContactForm
from .services import register_user
from profiles.forms import EmployerProfileForm, CandidateProfileForm
from profiles.models import Profile  # <--- ADD THIS IMPORT
from profiles.models import CandidateProfile
from jobs.models import Job, Application
from profiles.views import edit_candidate_profile
from django.core.mail import send_mail
# ==========================
# Public Pages
# ==========================

def home(request):
    return render(request, "public/home.html")


def public_job_list(request):
  # Fetch active/open jobs only
  jobs = (
      Job.objects.filter(status="open")
      .select_related("employer", "employer__profile")
      .order_by("-created_at")
  )

  # Search Filter
  query = request.GET.get("q")
  if query:
    jobs = jobs.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(requirements__icontains=query)
    )

  # Location Filter
  location = request.GET.get("location")
  if location:
    jobs = jobs.filter(location__icontains=location)

  # Employment Type Filter
  employment_type = request.GET.get("employment_type")
  if employment_type:
    jobs = jobs.filter(employment_type=employment_type)

  context = {
      "jobs": jobs,
      "job_count": jobs.count(),
  }
  return render(request, "public/jobs.html", context)


def about_view(request):
    return render(request, "public/about.html")


def contact_us(request):
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      contact_msg = form.save()

      # Optional: Send email notification to site admin
      try:
        subject = f"[TalentHub Contact] {contact_msg.subject}"
        message_body = (
            f"New Contact Message from {contact_msg.name}"
            f" ({contact_msg.email}):\n\n{contact_msg.message}"
        )
        send_mail(
            subject=subject,
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,  # Keeps page working even if email server isn't set up yet
        )
      except Exception:
        pass

      messages.success(
          request,
          "Thank you for contacting us! We have received your message and will get back to you shortly.",
      )
      return redirect("contact_us")
    else:
      messages.error(
          request, "Please fill out all fields correctly before submitting."
      )
  else:
    # Pre-fill name and email if user is logged in
    initial_data = {}
    if request.user.is_authenticated:
      initial_data["name"] = (
          request.user.get_full_name() or request.user.username
      )
      initial_data["email"] = request.user.email
    form = ContactForm(initial=initial_data)

  return render(request, "public/contact.html", {"form": form})

# ==========================
# Authentication
# ==========================

def login_view(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            role = user.profile.role

            if role == "job_seeker":
                return redirect("candidate_dashboard")

            return redirect("employer_dashboard")

    else:

        form = LoginForm()

    return render(
        request,
        "public/login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    logout(request)
    return redirect("home")


# ==========================
# Registration
# ==========================

def register_choice(request):
    return render(
        request,
        "public/register_choice.html"
    )


def register(request, role):

    role = role.lower()

    if role not in ["job-seeker", "employer"]:
        return redirect("register_choice")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user, dashboard = register_user(
                form,
                role.replace("-", "_")
            )

            login(request, user)

            return redirect(dashboard)

    else:

        form = RegisterForm()

    return render(
        request,
        "public/register.html",
        {
            "form": form,
            "role": role.replace("-", " ").title(),
            "page_title": (
                f"Create {role.replace('-', ' ').title()} Account"
            ),
            "button_text": "Create Account",
        }
    )


# ==========================
# Dashboards
# ==========================

@login_required
def candidate_dashboard(request):
  candidate_profile = get_object_or_404(
      CandidateProfile, profile__user=request.user
  )

  applications = Application.objects.filter(
      candidate=candidate_profile
  ).select_related('job')

  return render(
      request,
      "dashboard/candidate/dashboard.html",
      {
          "applications": applications,
      },
  )
  
@login_required
def MyApplications(request):
  candidate_profile = get_object_or_404(
      CandidateProfile, profile__user=request.user
  )

  applications = Application.objects.filter(
      candidate=candidate_profile
  ).select_related('job')

  return render(
      request,
      "dashboard/candidate/applications.html",
      {
          "applications": applications,
      },
  )
@login_required
def delete_application(request, application_id):
  application = get_object_or_404(
      Application,
      id=application_id,
      candidate__profile__user=request.user,
  )

  if request.method == 'POST':
    # Backend check: allow deletion only if pending or submitted
    if application.status in ['pending', 'submitted']:
      job_title = application.job.title
      application.delete()
      messages.success(
          request, f"Application for '{job_title}' withdrawn successfully."
      )
    else:
      messages.error(
          request,
          'You cannot withdraw an application that has already been reviewed'
          ' or processed.',
      )

  return redirect('candidate_dashboard')

@login_required
def view_application(request, application_id):
    # Retrieve application ensuring it belongs to the logged-in candidate
    application = get_object_or_404(
        Application, 
        id=application_id, 
        candidate__profile__user=request.user
    )
    
    context = {
        'application': application,
        'job': application.job,
    }
    return render(request, 'dashboard/candidate/view_application.html', context)

@login_required
def job_list(request):
  # Exclude drafts so candidates only see active/open postings
  jobs = (
      Job.objects.filter(status="open")
      .select_related("employer")
      .order_by("-created_at")
  )

  # Keyword Search (title, description, requirements)
  query = request.GET.get("q")
  if query:
    jobs = jobs.filter(
        Q(title__icontains=query)
        | Q(description__icontains=query)
        | Q(requirements__icontains=query)
    )

  # Location Filter
  location = request.GET.get("location")
  if location:
    jobs = jobs.filter(location__icontains=location)

  # Employment Type Filter
  employment_type = request.GET.get("employment_type")
  if employment_type:
    jobs = jobs.filter(employment_type=employment_type)

  context = {
      "jobs": jobs,
  }
  return render(request, "dashboard/candidate/job_list.html", context)


@login_required
def employer_dashboard(request):
    # Get the EmployerProfile instance for the active user
    profile = request.user.profile.employer
    
    # Query using the profile instance
    jobs = Job.objects.filter(employer=profile).order_by("-id")

    context = {
        "jobs": jobs,
        "job_count": jobs.count(),
    }
    return render(request, "dashboard/employer/dashboard.html", context)

@login_required
def employer_company_profile(request):

    employer = request.user.profile.employer

    if request.method == "POST":

        form = EmployerProfileForm(
            request.POST,
            request.FILES,
            instance=employer
        )

        if form.is_valid():

            form.save()

            return redirect("employer_company_profile")

    else:

        form = EmployerProfileForm(
            instance=employer
        )

    return render(
        request,
        "dashboard/employer/company_profile.html",
        {
            "form": form,
            "employer": employer,
        }
    )
def account_post_job(request):
    return render(request, 'dashboard/employer/post_job.html')