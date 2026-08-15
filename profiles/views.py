# profiles/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CandidateProfileForm
from .models import CandidateProfile


@login_required
def edit_candidate_profile(request):
  # Get candidate profile belonging to the logged-in user
  candidate_profile = get_object_or_404(
      CandidateProfile, profile__user=request.user
  )

  if request.method == 'POST':
    form = CandidateProfileForm(request.POST, instance=candidate_profile)
    if form.is_valid():
      form.save()
      messages.success(request, 'Profile updated successfully!')
      return redirect('edit_candidate_profile')
    else:
      for field, errors in form.errors.items():
        field_name = (
            form.fields[field].label or field.replace('_', ' ').title()
            if field in form.fields
            else ''
        )
        for error in errors:
          messages.error(
              request, f'{field_name}: {error}' if field_name else f'{error}'
          )
  else:
    form = CandidateProfileForm(instance=candidate_profile)

  return render(
      request,
      'dashboard/candidate/edit_profile.html',
      {'form': form, 'candidate': candidate_profile},
  )