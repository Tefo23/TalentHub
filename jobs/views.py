# jobs/views.py
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from profiles.models import EmployerProfile
from profiles.models import CandidateProfile
from profiles.models import Profile  # <--- ADD THIS IMPORT
from django.contrib import messages  # <--- ADD THIS IMPORT
User = get_user_model()

@login_required
def toggle_job_status(request, job_id, new_status):
  # Fetch job belonging to employer profile
  job = get_object_or_404(Job, id=job_id, employer=request.user.profile.employer)

  if new_status in ["draft", "open", "closed"]:
    job.status = new_status
    job.save()

  return redirect("employer_dashboard")


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, status="open")
    
    # Query via profile__user instead of user directly
    candidate_profile = get_object_or_404(CandidateProfile, profile__user=request.user)

    # Check if candidate has already applied
    if Application.objects.filter(job=job, candidate=candidate_profile).exists():
        messages.warning(request, "You have already applied for this job.")
        #return redirect("candidate_dashboard")

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = candidate_profile
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect("candidate_dashboard")
        else:
            messages.error(request, "Please fill out all required fields properly.")
    else:
        form = ApplicationForm()

    return render(
        request, 
        "dashboard/candidate/apply.html", 
        {"form": form, "job": job}
    )


@login_required
def candidate_dashboard(request):
  candidate_profile = get_object_or_404(
      CandidateProfile, profile__user=request.user
  )

  applications = Application.objects.filter(
      candidate=candidate_profile
  ).select_related('job')

  # --- DEBUG PRINT TO TERMINAL ---
  print("\n================ DEBUG CANDIDATE DASHBOARD ================")
  print(f"Logged-in User: {request.user.username}")
  print(f"Candidate Profile ID: {candidate_profile.id}")
  print(f"Applications Query Count: {applications.count()}")
  print("============================================================\n")

  return render(
      request,
      "dashboard/candidate/dashboard.html",
      {
          "applications": applications,
      },
  )



@login_required
def edit_job(request, job_id):  # Line 8
    # All code inside this function MUST be indented by 4 spaces:
    job = get_object_or_404(Job, id=job_id, employer=request.user.profile.employer)
    
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("employer_dashboard")
    else:
        form = JobForm(instance=job)

    return render(
        request, 
        "dashboard/employer/edit_job.html", 
        {"form": form, "job": job}
    )


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user.profile.employer)
    
    if request.method == "POST":
        job.delete()
        return redirect("employer_dashboard")

    return render(
        request, 
        "dashboard/employer/delete_job.html", 
        {"job": job}
    )



@login_required
def post_job(request):
  employer_profile = request.user.profile.employer

  if request.method == "POST":
    form = JobForm(request.POST)
    if form.is_valid():
      job = form.save(commit=False)
      job.employer = employer_profile
      job.save()
      messages.success(request, "Job posted successfully!")
      return redirect("employer_dashboard")
    else:
      # Extract actual errors per field and render them in the message
      for field, errors in form.errors.items():
        field_name = form.fields[field].label or field.replace("_", " ").title() if field in form.fields else ""
        for error in errors:
          if field_name:
            messages.error(request, f"{field_name}: {error}")
          else:
            messages.error(request, f"{error}")
  else:
    form = JobForm()

  return render(request, "dashboard/employer/post_job.html", {"form": form})
  

@login_required
def employer_dashboard(request):
    # Fetch all jobs posted by the currently logged-in employer
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at') # assumes created_at field exists
    
    context = {
        'jobs': jobs,
        'job_count': jobs.count(),
    }
    return render(request, 'dashboard/employer/dashboard.html', context)
@login_required
def view_job_applicants(request, job_id):
    # Ensure employer owns the job posting
    job = get_object_or_404(Job, id=job_id, employer__user=request.user)
    applications = job.applications.select_related("candidate__user").all()

    return render(
        request,
        "dashboard/employer/job_applicants.html",
        {"job": job, "applications": applications},
    )

@login_required
def employer_applications(request):
  # Get EmployerProfile using profile__user
  employer_profile = get_object_or_404(
      EmployerProfile, profile__user=request.user
  )

  # Fetch jobs for filter dropdown
  employer_jobs = Job.objects.filter(employer=employer_profile).order_by(
      "-created_at"
  )

  # Query applications matching employer's jobs
  applications = (
      Application.objects.filter(job__employer=employer_profile)
      .select_related(
          "job",
          "candidate",
          "candidate__profile",
          "candidate__profile__user",
      )
      .order_by("-applied_at")
  )

  # Filter by Job Posting
  job_id = request.GET.get("job")
  if job_id:
    applications = applications.filter(job_id=job_id)

  # Filter by Application Status
  status_filter = request.GET.get("status")
  if status_filter:
    applications = applications.filter(status=status_filter)

  # Search Candidate Name / Headline
  search_query = request.GET.get("q")
  if search_query:
    applications = applications.filter(
        Q(candidate__profile__user__username__icontains=search_query)
        | Q(
            candidate__profile__user__first_name__icontains=search_query
        )
        | Q(candidate__profile__user__last_name__icontains=search_query)
        | Q(candidate__headline__icontains=search_query)
    )

  context = {
      "applications": applications,
      "employer_jobs": employer_jobs,
      "application_count": applications.count(),
  }
  return render(
      request, "dashboard/employer/applications_list.html", context
  )
  
@login_required
def review_candidate(request, application_id):
  employer_profile = get_object_or_404(EmployerProfile, profile__user=request.user)

  # Security check: Ensure application belongs to a job posted by this employer
  application = get_object_or_404(
      Application.objects.select_related(
          "job",
          "candidate",
          "candidate__profile",
          "candidate__profile__user",
      ),
      id=application_id,
      job__employer=employer_profile,
  )

  candidate = application.candidate

  # Handle status updates via POST
  if request.method == "POST":
    new_status = request.POST.get("status")
    valid_statuses = ["pending", "reviewed", "accepted", "rejected"]

    if new_status in valid_statuses:
      application.status = new_status
      application.save()
      messages.success(
          request,
          f"Application status updated to '{application.get_status_display()}' successfully!",
      )
      return redirect("review_candidate", application_id=application.id)
    else:
      messages.error(request, "Invalid status choice selected.")

  context = {
      "application": application,
      "job": application.job,
      "candidate": candidate,
  }
  return render(
      request, "dashboard/employer/review_candidate.html", context
  )